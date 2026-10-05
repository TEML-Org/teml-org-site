#!/usr/bin/env python3
"""Copy the TEML spec and JSON Schemas from a local Teml-spec checkout, and build the
demo page with a local teml-tools checkout.

Usage: python3 scripts/sync-from-spec.py [path/to/Teml-spec] [path/to/teml-tools]
       (defaults: ../Teml-spec and ../teml-tools)

- Teml-spec  spec/teml-<latest>.md  -> content/docs/example/specification.md
- Teml-spec  schema/*.schema.json   -> static/schema/   (served at https://teml.org/schema/...)
- teml-tools demo page              -> static/demos/index.html   (needs Node; run `npm install` in teml-tools once)

The demo page is drawn from teml-tools' own spec/ submodule, the spec commit the tools support.
"""
import pathlib, re, shutil, subprocess, sys

site = pathlib.Path(__file__).resolve().parent.parent
spec_repo = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else site.parent / "Teml-spec").resolve()
tools_repo = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else site.parent / "teml-tools").resolve()
GITHUB = "https://github.com/TEML-Org/Teml-spec/blob/main/"

# Spec: the newest teml-alpha-NNN.md
spec_file = sorted((spec_repo / "spec").glob("teml-alpha-*.md"))[-1]
version = spec_file.stem.replace("teml-", "v-")            # e.g. v-alpha-002
text = spec_file.read_text()
text = re.sub(r"^# .*\n", "", text, count=1)                # the page title comes from front matter
text = text.replace("](../schema/", "](/schema/")           # schemas are served by this site
text = re.sub(r"\]\(\.\./(Examples/[^)]+)\)", lambda m: f"]({GITHUB}{m.group(1)})", text)
text = re.sub(r"\]\((teml-alpha-\d+\.md)\)", lambda m: f"]({GITHUB}spec/{m.group(1)})", text)
text = text.replace("<br>", " ")                            # Hugo strips raw HTML by default
front = f"""---
weight: 200
title: "Specification ({version})"
---

# TEML Specification

> Copied from [`{spec_file.relative_to(spec_repo)}`]({GITHUB}{spec_file.relative_to(spec_repo)}) in the Teml-spec repository. Edit it there, then run `scripts/sync-from-spec.py`.

"""
out = site / "content/docs/example/specification.md"
out.write_text(front + text.lstrip("\n"))
print("wrote", out.relative_to(site))

# Schemas
(site / "static/schema").mkdir(parents=True, exist_ok=True)
for f in sorted((spec_repo / "schema").glob("*.schema.json")):
    shutil.copy(f, site / "static/schema" / f.name)
    print("copied", f"static/schema/{f.name}")

# Demo page, built by teml-tools
(site / "static/demos").mkdir(parents=True, exist_ok=True)
subprocess.run(["node", "build-demos.mjs", str(site / "static/demos/index.html")], cwd=tools_repo, check=True)
