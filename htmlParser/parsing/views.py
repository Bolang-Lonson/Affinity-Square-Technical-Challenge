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
    except requests.RequestException as e:
        return {'error': str(e)}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Determine HTML version (simple heuristic based on doctype)
    doctype = soup.contents[0] if soup.contents and isinstance(soup.contents[0], str) else ''
    html_version = "HTML5" if "<!DOCTYPE html>" in doctype else "Unknown"

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

    result = {
        'html_version': html_version,
        'page_title': page_title,
        'num_headings': num_headings,
        'num_links': num_links,
        'has_login_form': login_form,
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