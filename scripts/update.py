#!/usr/bin/env python3
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUCKET_DIR = ROOT / "bucket"
BUCKET_FILE = ROOT / "bucket.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"JSON top level must be an object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def comparable_app(app: dict[str, Any]) -> dict[str, Any]:
    comparable = dict(app)
    comparable.pop("updatedAt", None)
    return comparable


def write_app_if_changed(path: Path, app: dict[str, Any]) -> bool:
    if path.exists():
        existing = read_json(path)
        if comparable_app(existing) == comparable_app(app):
            return False
    write_json(path, app)
    return True


def fetch_json(url: str, token: str | None = None) -> dict[str, Any]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "spork-bucket"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError(f"JSON response must be an object: {url}")
    return data


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "spork-bucket"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def update_app(manifest: dict[str, Any], version: str, url: str) -> dict[str, Any]:
    updated = dict(manifest)
    updated["version"] = version
    updated["url"] = url
    updated["updatedAt"] = now_iso()
    return updated


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing or invalid field: {key}")
    return value


def resolve_github_release(manifest: dict[str, Any], token: str | None) -> dict[str, Any]:
    source = manifest["checkver"]
    repo = require_string(source, "repo")
    release = fetch_json(f"https://api.github.com/repos/{repo}/releases/latest", token)
    tag = str(release.get("tag_name") or "")
    version_regex = source.get("versionRegex", "^v?(.*)$")
    match = re.search(version_regex, tag)
    version = match.group(1) if match and match.groups() else tag.lstrip("v")
    asset_pattern = re.compile(require_string(source, "assetPattern"))
    for asset in release.get("assets", []):
        if not isinstance(asset, dict):
            continue
        name = str(asset.get("name") or "")
        if asset_pattern.search(name):
            return update_app(manifest, version, require_string(asset, "browser_download_url"))
    raise ValueError(f"no matching release asset for {manifest['id']}")


def resolve_fixed_url(manifest: dict[str, Any]) -> dict[str, Any]:
    source = manifest["checkver"]
    version = source.get("version") or "unknown"
    return update_app(manifest, str(version), require_string(source, "url"))


def resolve_html_regex(manifest: dict[str, Any]) -> dict[str, Any]:
    source = manifest["checkver"]
    page_url = require_string(source, "pageUrl")
    html = fetch_text(page_url)
    url_match = re.search(require_string(source, "urlRegex"), html)
    if not url_match:
        raise ValueError(f"no url matched for {manifest['id']}")
    url = url_match.group(1) if url_match.groups() else url_match.group(0)
    url = urllib.parse.urljoin(page_url, url)
    version = "unknown"
    version_regex = source.get("versionRegex")
    if version_regex:
        match = re.search(version_regex, url) or re.search(version_regex, html)
        if match:
            version = match.group(1) if match.groups() else match.group(0)
    return update_app(manifest, version, url)


def resolve_manifest(manifest: dict[str, Any], token: str | None) -> dict[str, Any]:
    source = manifest.get("checkver")
    if not isinstance(source, dict):
        raise ValueError(f"missing checkver for {manifest.get('id', '<unknown>')}")
    source_type = source.get("type")
    if source_type == "github-release":
        return resolve_github_release(manifest, token)
    if source_type == "fixed-url":
        return resolve_fixed_url(manifest)
    if source_type == "html-regex":
        return resolve_html_regex(manifest)
    raise ValueError(f"unsupported source type: {source_type}")


def main() -> int:
    token = None
    try:
        import os

        token = os.environ.get("GITHUB_TOKEN")
    except Exception:
        token = None

    failures = []
    changed = False

    for path in sorted(BUCKET_DIR.glob("*.json")):
        try:
            manifest = read_json(path)
            app = resolve_manifest(manifest, token)
            if write_app_if_changed(path, app):
                changed = True
                print(f"updated {app['id']} {app['version']}")
            else:
                print(f"unchanged {app['id']} {app['version']}")
        except Exception as exc:
            failures.append(f"{path.name}: {exc}")

    if changed and BUCKET_FILE.exists():
        bucket = read_json(BUCKET_FILE)
        bucket["updatedAt"] = now_iso()
        write_json(BUCKET_FILE, bucket)

    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
