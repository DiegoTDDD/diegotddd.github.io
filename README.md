# diegotddd.github.io

Source of [diegotddd.github.io](https://diegotddd.github.io/), the portfolio of Diego Alves.

- `projects.py`: the content, one entry per project, with the measured results stated in each
  project's README;
- `build.py`: builds `_site/` with the standard library only, and refuses to build if a project
  has no measured results or a media file is missing;
- `scripts/check_links.py`: fails on any broken local link or anchor;
- `.github/workflows/pages.yml`: builds, checks and deploys to GitHub Pages on every push.

```bash
python build.py && python scripts/check_links.py
```
