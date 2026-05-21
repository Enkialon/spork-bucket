# Spork Bucket

This repository is a Spork bucket for downloadable Linux packages.

Spork reads generated package metadata from `generated/*.json`. Source manifests live in `apps/*.json`, and `scripts/update.py` resolves the latest versions and download URLs.

## Use

```bash
spork bucket add main https://github.com/Enkialon/spork-bucket.git
spork update
spork search code
spork download code
```

## Layout

```text
apps/                 # editable source manifests
generated/            # generated index files consumed by Spork
scripts/update.py     # updates generated metadata
bucket.json           # bucket metadata
```

## Update Locally

```bash
python3 scripts/update.py
```

The update script supports these source types:

- `github-release`
- `fixed-url`
- `html-regex`

GitHub Actions runs the same script on a schedule and commits any generated metadata changes.
