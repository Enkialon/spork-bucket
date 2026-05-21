# Spork Bucket

This repository is a Spork bucket for downloadable Linux packages.

Spork reads package metadata directly from `bucket/*.json`. The optional `scripts/update.py` helper is only for repository automation and is not run by Spork clients.

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
