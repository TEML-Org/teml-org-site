This is the Teml.Org website files

TEML stands for 'The Event Modeling Language'.

## Updating from the spec

The specification page, the JSON Schemas and the demo page are copied from the [Teml-spec](https://github.com/TEML-Org/Teml-spec) repository. Don't edit them here. Change them in Teml-spec, then run:

```sh
python3 scripts/sync-from-spec.py ../Teml-spec
```

This updates `content/docs/example/specification.md`, `static/schema/` (served at `https://teml.org/schema/`) and `static/demos/` (served at `https://teml.org/demos/`). The demo page is built with Node, so run `npm install` in `Teml-spec/tools/prototype` once first.

## Deploying

Pushing to `main` builds the site with Hugo and deploys it to GitHub Pages (see `.github/workflows/hugo.yml`).
