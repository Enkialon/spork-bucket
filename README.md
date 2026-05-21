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
- `redirect-url`
- `html-regex`

## Multi-Architecture Manifests

Use `architectures` for packages that publish different DEB files per CPU architecture:

```json
{
  "id": "example",
  "version": "1.0.0",
  "architectures": {
    "amd64": {
      "url": "https://example.com/example_1.0.0_amd64.deb",
      "sha256": null
    },
    "arm64": {
      "url": "https://example.com/example_1.0.0_arm64.deb",
      "sha256": null
    }
  },
  "checkver": {
    "type": "github-release",
    "repo": "owner/example",
    "versionRegex": "^v?(.*)$",
    "architectures": {
      "amd64": {
        "assetPattern": "example_[0-9.]+_amd64\\.deb$"
      },
      "arm64": {
        "assetPattern": "example_[0-9.]+_arm64\\.deb$"
      }
    }
  }
}
```

Spork clients select the configured architecture during `spork update`. Repository automation updates each configured architecture in place. Architecture keys use Debian-style names such as `amd64`, `arm64`, `mips64el`, and `loongarch64`.

GitHub Actions runs the script on a schedule and commits manifest changes. Local `spork update` only pulls the repository and reads JSON.
