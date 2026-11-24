# diegotddd.github.io

Source of [diegotddd.github.io](https://diegotddd.github.io/), the portfolio of Diego Alves.

- `projects.py` / `projects_pt.py`: the projects in English and Portuguese, with the measured
  results stated in each project's README;
- `content.py`: profile, education, skills, interface text, filter categories and
  the CI workflow behind each project's live status badge;
- `build.py`: builds `_site/` (Portuguese at `/`, English at `/en/`) with the standard library only, and refuses to build if a project
  has no measured results or a media file is missing;
- `scripts/render_assets.py`: renders the social preview image with Playwright;
- `scripts/check_links.py`: fails on any broken local link or anchor;
- `.github/workflows/pages.yml`: builds, checks and deploys to GitHub Pages on every push.

```bash
python build.py && python scripts/render_assets.py && python scripts/check_links.py
```
