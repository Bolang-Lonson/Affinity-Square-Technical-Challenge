from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

from .forms import URLForm

# Create your views here.
def parse_url(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        error = ''
    except requests.RequestException as e:
        error = str(e)
    
    status_code = response.status_code
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Determine HTML version (simple heuristic based on doctype)
    soup.contents = list(filter(lambda substr: substr != '\n', soup.contents))
    # cleaning up contents
    doctype = soup.contents[0] if soup.contents and isinstance(soup.contents[0], str) else ''
    html4_strict = 'html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"'.replace(' ', '')
    html4_loose = 'html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/loose.dtd"'.replace(' ', '')

    match doctype.replace(' ', ''):
        case 'html':
            html_version = 'HTML5'

        case 'htmlPUBLIC"-//W3C//DTDHTML4.01//EN""http://www.w3.org/TR/html4/strict.dtd"':
            # doctype specification for html 4.01 page with strict on
            html_version = 'HTML4: Strict'

        case 'htmlPUBLIC"-//W3C//DTDHTML4.01//EN""http://www.w3.org/TR/html4/loose.dtd"':
            html_version = 'HTML4: Loose'

        case _:
            html_version = 'Unknown'

    
    # Page title
    page_title = soup.title.string if soup.title else 'No Title'

    # Number of headings by level
    num_headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

    # Number of internal and external links
    links = soup.find_all('a', href=True)
    num_links = {'internal': 0, 'external': 0}
    domain = requests.utils.urlparse(url).netloc

    for link in links:
        href = link['href']
        if domain in href or href.startswith('/'):
            num_links['internal'] += 1
        else:
            num_links['external'] += 1

    # Detect login form
    login_form = any(form for form in soup.find_all('form') if any(input['type'] in ['password'] for input in form.find_all('input', type=True)))
    # button with human written language of 'login', 'log in', 'log-in', 'signin', 'sign-in' and 'sign in'
    login_btn = any(button for button in soup.find_all('button') if button.text.strip().lower() in ['login', 'log in', 'log-in', 'signin', 'sign-in' and 'sign in'])
    # button might be in the form of input:submit
    submit_btn = any(submit for submit in soup.find_all('input', {'type': 'submit'}) if submit['value'].lower() in ['login', 'log in', 'log-in', 'signin', 'sign-in' and 'sign in'])

    result = {
        'html_version': html_version,
        'page_title': page_title,
        'num_headings': num_headings,
        'num_links': num_links,
        'has_login_form': login_form and (login_btn or submit_btn),
        'status_code': status_code,
        'error': error
    }

    return result


def index(request):
    form = URLForm()
    results = None

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            results = parse_url(url)

    return render(request, 'index.html', {'form': form, 'results': results})