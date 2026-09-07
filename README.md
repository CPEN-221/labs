# CPEN 221 laboratory activities

This directory is the self-contained website source for
`https://cpen-221.github.io/labs/`. It uses the same Jekyll structure, institutional
visual system, and locally hosted reading typefaces as the Fall 2026 project site.

The site is ready for Fall 2026 activities but currently publishes only the public
2025 archive.

## Source and provenance

The canonical archived handouts remain in `../2025/` in the course
workspace. `source/2025/` is the public, repository-local copy used for provenance
and standalone rebuilds. Teaching-team guides and their assets are deliberately
excluded.

## Refresh the archive

Use Pandoc 3.10 and run:

```sh
python3 scripts/import_labs.py
python3 scripts/check_site.py
```

The importer prefers the canonical `../2025/` source when this repository is inside
the course workspace and otherwise falls back to `source/2025/`. It regenerates the
pages below `2025/`, copies the six public images to stable asset paths, and records
a source digest in each activity.

## Preview locally

Use Ruby 3.3 and run:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Then run `python3 scripts/check_site.py` again so that it can validate the rendered
site as well as the source tree.

## Publish with GitHub Pages

The repository must be named `labs` in the `CPEN-221` organization. In the
repository settings, open **Pages**, choose **Deploy from a branch**, and select the
`main` branch and `/(root)` folder. GitHub Pages will run Jekyll and publish the site
at `https://cpen-221.github.io/labs/` after each push. No GitHub Actions workflow is
needed.
