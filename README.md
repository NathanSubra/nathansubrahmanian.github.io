# Personal Website

A Flask-powered personal website that can be exported to static files for GitHub Pages.

## Update Your Content

- Edit `data/site.yml` for your name, links, profile text, contact text, and publications.
- Replace `static/assets/resume.pdf` with your current resume. Keep the filename `resume.pdf`.
- Add your headshot as `static/assets/headshot.jpg`, `headshot.jpeg`, `headshot.png`, or `headshot.webp`. The app will prefer those files over the placeholder SVG.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open `http://127.0.0.1:5000`.

## Build for GitHub Pages

```bash
python build_static.py
```

Publish the `docs/` directory from your repository settings:

1. Go to the GitHub repository.
2. Open Settings, then Pages.
3. Set the source to your main branch and the `/docs` folder.

After editing content or replacing assets, run `python build_static.py` again and commit the updated files.
