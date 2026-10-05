This is the Teml.Org website files

TEML stands for 'The Event Modeling Language'.

## Updating from the spec

The specification page and the JSON Schemas are copied from the [Teml-spec](https://github.com/TEML-Org/Teml-spec) repository. The demo page is built by TEML-Org/teml-tools (private for now), from the spec commit that teml-tools pins in its `spec/` submodule. Don't edit any of them here. Change them in their repository, then run:

```sh
python3 scripts/sync-from-spec.py ../Teml-spec ../teml-tools
```

This updates `content/docs/example/specification.md`, `static/schema/` (served at `https://teml.org/schema/`) and `static/demos/` (served at `https://teml.org/demos/`). The demo page is built with Node, so run `npm install` in `teml-tools` once first (and clone it with `--recurse-submodules`).

## Deploying

Pushing to `main` builds the site with Hugo and deploys it to GitHub Pages (see `.github/workflows/hugo.yml`).
