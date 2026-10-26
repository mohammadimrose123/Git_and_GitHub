# Git & GitHub DevOps Assignment

**GitHub repository:** https://github.com/mohammadimrose123/Git_and_GitHub

Flask app for the Git workflow assignment. It provides:
- `GET /` — To-Do form
- `GET /api` — returns `data.json`
- `POST /submittodoitem` — validates and stores To-Do details in MongoDB
- Item ID and UUID generation when not provided
- SHA-256 Item Hash calculation

## Run locally (Windows)

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set `MONGODB_URI` to your MongoDB connection string. Then run:

```bat
python app.py
```

Open http://127.0.0.1:5000 and test `/api` at http://127.0.0.1:5000/api.

Do not commit `.env`, credentials, or virtual environments.

## Evidence note

The documentation includes a command/evidence checklist. Capture your own terminal and GitHub screenshots while running the workflow on your computer. Screenshots generated from a local demo do not prove that SSH authentication or a remote push succeeded.
