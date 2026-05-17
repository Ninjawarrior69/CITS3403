# CITS3403 Group Project — BookWorm

## What is BookWorm?

BookWorm is a small reading-tracker web application that lets users search for
books, view book details, save books to reading shelves, and post short reviews.
The app is built with Flask (application factory pattern), uses SQLAlchemy for
persistence, and includes both unit tests and end-to-end Selenium tests to verify
behavior in a browser. It's intended as a demo project for learning full-stack
web development and automated testing.

## Team

| UWA ID   | Name              | GitHub username  |
| -------- | ----------------- | ---------------- |
| 22964473 | Devarsh Patel     | Ninjawarrior69   |
| 24084355 | Weiman Gao        | WeimanGao        |
| 24224028 | Celeste Petrovski | CelestePetrovski |

## Quickstart — Launch locally

These steps work on Linux, macOS and Windows (PowerShell/cmd). Python 3.10+
is required.

1. Create and activate a virtual environment

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (cmd.exe):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Initialize the database (optional — the app will create the schema automatically in tests)

```bash
python run.py setup-db
# or run the app and it will create the DB on first request
```

4. Run the development server

```bash
python run.py
```

5. Open the app in your browser at http://127.0.0.1:5000

Notes:

- The project uses environment configuration via `app/config.py`. For testing the
  Selenium suite, CSRF protection is disabled in the test config to simplify
  automation.

## Run tests

There are two test suites included: unit tests and Selenium end-to-end tests.

Unit tests:

```bash
python -m unittest tests.unit_tests -v
```

Selenium (end-to-end) tests:

- The Selenium tests require a Chromium-based browser. We use `webdriver-manager`
  to automatically install a matching ChromeDriver in CI and locally.
- To run the full Selenium suite headless:

```bash
python -m unittest discover -v tests -p "test_selenium_*.py"
```

- To see the browser while tests run (handy when debugging):

Linux / macOS / Windows (PowerShell):

```powershell
$env:SHOW_BROWSER=1; python -m unittest discover -v tests -p "test_selenium_*.py"
```

CI: The repository includes a GitHub Actions workflow at
[.github/workflows/selenium-tests.yml](.github/workflows/selenium-tests.yml) to
run the Selenium tests on push and pull requests.

## Files of interest

- `app/` — Flask application package (routes, models, templates, static files)
- `tests/` — Unit and Selenium tests (Selenium harness is in `tests/selenium_setup.py`)
- `requirements.txt` — pinned Python dependencies (includes `webdriver-manager`)

## Possible project ideas

If you extend this app, consider:

- Add social features: follow users, share reading lists, like reviews.
- Improve recommendations: integrate a simple collaborative-filtering or
  content-based recommender using book metadata.
- Add import/export: let users import reading lists from CSV and export their
  data for backup.
- Mobile-friendly UI: improve responsive layouts and add a progressive web app
  manifest.

---

If anything is unclear or you want a one-step script to set up and run the app,
tell me your OS and I can add a small platform-specific helper script.
