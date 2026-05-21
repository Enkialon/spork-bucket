# Spork Bucket

This repository is the default Spork bucket for downloadable Linux DEB packages.

It contains bucket manifests for Spork, a Scoop-style Linux package manager inspired by the Scoop Windows package manager workflow. Spork reads package metadata directly from `bucket/*.json`. The optional `scripts/update.py` helper is only for repository automation and is not run by Spork clients.

Keywords: Spork bucket, DEB package manifests, Linux package manager bucket, apt package downloads, dpkg package metadata, Scoop-style bucket.

## Use

```bash
spork bucket add main https://github.com/Enkialon/spork-bucket.git
spork update
spork search code
spork download code
```

## Layout

```text
bucket/               # app manifests consumed by Spork
scripts/update.py     # repository automation for checkver fields
bucket.json           # bucket metadata
```

## Update Locally

```bash
python3 scripts/update.py
```

The update script refreshes `bucket/*.json` files from each manifest's `checkver` block. It supports these source types:

- `github-release`
- `fixed-url`
- `html-regex`

GitHub Actions runs the script on a schedule and commits manifest changes. Local `spork update` only pulls the repository and reads JSON.
