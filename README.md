# URL Shortener

A small Flask + SQLite web app that turns long URLs into short links, redirects visitors, and counts clicks.

## Features
- Shorten any http/https URL
- Optional custom alias (e.g. `/mylink`)
- Click tracking with a stats endpoint
- Simple web page plus a JSON API
- Input validation and duplicate alias protection

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Open http://127.0.0.1:5000

## API
| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/shorten` | Body: `{"url": "...", "alias": "optional"}` returns the short link |
| GET | `/<code>` | Redirects to the original URL and counts a click |
| GET | `/stats/<code>` | Returns the URL, click count, and created time |

Example:
```bash
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com", "alias": "gh"}'
```

## Project structure
```
url-shortener/
├── run.py
├── shortener/
│   ├── app.py      # routes
│   ├── db.py       # SQLite helper
│   └── utils.py    # code generation + validation
├── templates/index.html
├── tests/test_app.py
└── requirements.txt
```

## Run tests
```bash
pytest
```

## Ideas to extend
- Link expiry dates
- User accounts
- Rate limiting
- Deploy on Render or Railway

## License
MIT
