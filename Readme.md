# URL HTML Analyser

## How to Build and Run

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd htmlParser
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
3. **Run migrations:**
    ```bash
    python manage.py migrate
4. **Run the development server:**
    ```bash
    python manage.py runserver
5. **Open the application:**
    ```
    Open http://127.0.0.1:8000/ in your browser.

## Known Constraints And Assumptions

- HTML version detection is simplistic and may not cover all cases especially old ones.
- Login form detection is basic and may not work for all types of login forms.
- Pages are assumed to be in English to detect human language for Login form detection
- All URLs should be input starting with 'http://' or 'https://'