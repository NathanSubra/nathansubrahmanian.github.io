from __future__ import annotations

import re
import shutil
from pathlib import Path

from app import app


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
STATIC = ROOT / "static"

PAGES = {
    "/": "index.html",
    "/publications/": "publications/index.html",
    "/contact/": "contact/index.html",
}


def build() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)

    DOCS.mkdir(parents=True)
    shutil.copytree(STATIC, DOCS / "static")

    with app.test_client() as client:
        for route, output_name in PAGES.items():
            response = client.get(route)
            if response.status_code >= 400:
                raise RuntimeError(f"Failed to render {route}: {response.status_code}")
            output_path = DOCS / output_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            html = relativize_root_links(response.data.decode("utf-8"), output_path)
            output_path.write_text(html, encoding="utf-8")

    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


def relativize_root_links(html: str, output_path: Path) -> str:
    depth = len(output_path.relative_to(DOCS).parent.parts)
    prefix = "../" * depth

    def replace(match: re.Match[str]) -> str:
        attribute = match.group("attribute")
        quote = match.group("quote")
        path = match.group("path")

        if path == "/":
            relative_path = prefix or "./"
        else:
            relative_path = f"{prefix}{path.lstrip('/')}"

        return f"{attribute}={quote}{relative_path}{quote}"

    return re.sub(
        r"(?P<attribute>\b(?:href|src|data|action))=(?P<quote>[\"'])(?P<path>/[^\"']*)(?P=quote)",
        replace,
        html,
    )


if __name__ == "__main__":
    build()
    print(f"Built static site in {DOCS}")
