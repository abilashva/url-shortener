"""Flask app: shorten URLs, redirect, and track clicks."""
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request

from .db import get_conn
from .utils import generate_code, is_valid_alias, is_valid_url

RESERVED = {"shorten", "stats", "static"}


def create_app(db_path: str = "urls.db") -> Flask:
    app = Flask(__name__, template_folder="../templates")
    app.config["DB_PATH"] = db_path

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/shorten")
    def shorten():
        data = request.get_json(silent=True) or request.form
        url = (data.get("url") or "").strip()
        alias = (data.get("alias") or "").strip()

        if not is_valid_url(url):
            return jsonify(error="Enter a valid http/https URL"), 400
        if alias and (not is_valid_alias(alias) or alias in RESERVED):
            return jsonify(error="Alias must be 3-20 letters, digits, - or _"), 400

        conn = get_conn(app.config["DB_PATH"])
        try:
            if alias:
                code = alias
            else:
                code = generate_code()
                while conn.execute("SELECT 1 FROM urls WHERE code=?", (code,)).fetchone():
                    code = generate_code()
            try:
                conn.execute("INSERT INTO urls (code, url) VALUES (?, ?)", (code, url))
                conn.commit()
            except sqlite3.IntegrityError:
                return jsonify(error="That alias is already taken"), 409
        finally:
            conn.close()

        short_url = request.host_url + code
        return jsonify(code=code, short_url=short_url, url=url), 201

    @app.get("/stats/<code>")
    def stats(code):
        conn = get_conn(app.config["DB_PATH"])
        row = conn.execute("SELECT * FROM urls WHERE code=?", (code,)).fetchone()
        conn.close()
        if row is None:
            return jsonify(error="Not found"), 404
        return jsonify(dict(row))

    @app.get("/<code>")
    def go(code):
        conn = get_conn(app.config["DB_PATH"])
        row = conn.execute("SELECT url FROM urls WHERE code=?", (code,)).fetchone()
        if row is None:
            conn.close()
            return jsonify(error="Not found"), 404
        conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE code=?", (code,))
        conn.commit()
        conn.close()
        return redirect(row["url"], code=302)

    return app
