from __future__ import annotations

from datetime import datetime
from pathlib import Path

import yaml
from flask import Flask, abort, render_template, url_for


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "site.yml"
ASSET_DIR = ROOT / "static" / "assets"


def create_app() -> Flask:
    app = Flask(__name__)

    @app.context_processor
    def inject_globals() -> dict:
        site = load_site_data()
        return {
            "site": site,
            "current_year": datetime.now().year,
            "headshot_url": find_headshot_url(),
            "resume_url": url_for("static", filename="assets/resume.pdf"),
            "active_link_class": active_link_class,
        }

    @app.route("/")
    def profile():
        return render_template("profile.html", active_page="profile")

    @app.route("/publications/")
    def publications():
        site = load_site_data()
        return render_template(
            "publications.html",
            active_page="publications",
            publications=site.get("publications", []),
        )

    @app.route("/contact/")
    def contact():
        return render_template("contact.html", active_page="contact")

    @app.route("/healthz/")
    def healthz():
        return {"ok": True}

    return app


def load_site_data() -> dict:
    if not DATA_FILE.exists():
        abort(500, description=f"Missing data file: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    return data


def find_headshot_url() -> str:
    for candidate in sorted(ASSET_DIR.glob("headshot.*")):
        if candidate.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg"}:
            return url_for("static", filename=f"assets/{candidate.name}")

    return url_for("static", filename="assets/headshot.svg")


def active_link_class(page: str, active_page: str) -> str:
    return "is-active" if page == active_page else ""


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
