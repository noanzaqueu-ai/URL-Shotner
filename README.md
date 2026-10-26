# 🔗 URL Shortener

A simple URL shortener built with **Python**, **Flask**, and **SQLite**. Generates short links, redirects to the original URL, and tracks clicks.

## ✨ Features

- ✅ Shorten long URLs into 6-character codes (Base62)
- ✅ Automatic redirect to the original URL
- ✅ Click counter per link
- ✅ JSON endpoint with stats for each link
- ✅ Basic URL validation (http/https)
- ✅ SQLite persistence (no external database server)


```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## 📁 Project Structure

url-shortener/
├── app.py              # Routes and application logic
├── database.py         # Database access layer (SQLite)
├── requirements.txt    # Project dependencies
├── README.md
├── templates/
│   └── index.html      # Web interface
└── shortener.db        # Auto-generated database (do not commit)

⚙️ How It Works

1. The user submits a URL through the form
2. The server validates it and generates a **unique 6-character code** (Base62: `a-z`, `A-Z`, `0-9`)
3. The `(code, URL)` pair is stored in SQLite
4. When `/<code>` is accessed, the system looks up the URL, increments the click counter, and redirects with **HTTP 302**
5. The `/stats/<code>` endpoint exposes the data as JSON

---

⭐ If this project helped you, consider giving it a star!
