#!/usr/bin/env python3
"""Mirror verified Pangolin client binaries from Gitea to this GitHub repo."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, tempfile, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

GITEA_URL = __import__("os").environ.get("GITEA_URL", "https://git.51yanmei.com").rstrip("/")
GITEA_PUBLIC_HOST = "git.51yanmei.com"
GITEA_REPO = "wangjia/pangolin"
GITHUB_REPO = "yanmeillc/pangolin-vpn"
ASSET_NAMES = ("pangolin-android.apk", "pangolin-windows-x64-setup.exe", "pangolin-macos-x64.zip")

class MirrorError(RuntimeError): pass

def request(url: str, timeout: int = 60):
    req = urllib.request.Request(url, headers={"User-Agent": "pangolin-release-mirror/1.0"})
    for attempt in range(3):
        try: return urllib.request.urlopen(req, timeout=timeout)
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2: raise MirrorError(f"Request failed after 3 attempts: {url}: {exc}") from exc
            time.sleep(2 ** attempt)

def fetch_release(tag: str) -> dict:
    url = f"{GITEA_URL}/api/v1/repos/{GITEA_REPO}/releases/tags/{urllib.parse.quote(tag)}"
    try:
        with request(url) as response: data = json.load(response)
    except urllib.error.HTTPError as exc: raise MirrorError(f"Gitea release {tag} lookup returned HTTP {exc.code}") from exc
    if data.get("tag_name") != tag or data.get("draft"): raise MirrorError(f"Gitea response is not a published {tag} release")
    return data

def download_asset(asset: dict, destination: Path) -> str:
    name, size, url = asset.get("name"), asset.get("size"), asset.get("browser_download_url")
    if not isinstance(size, int) or size <= 0: raise MirrorError(f"Invalid advertised size for {name!r}")
    parsed = urllib.parse.urlsplit(url or "")
    if parsed.hostname != GITEA_PUBLIC_HOST or not parsed.path.startswith(f"/{GITEA_REPO}/releases/download/"):
        raise MirrorError(f"Unexpected Gitea asset URL for {name}: {url}")
    base = urllib.parse.urlsplit(GITEA_URL)
    url = urllib.parse.urlunsplit((base.scheme, base.netloc, parsed.path, parsed.query, ""))
    digest, received = hashlib.sha256(), 0
    try:
        with request(url, timeout=180) as response, destination.open("wb") as out:
            length = response.headers.get("Content-Length")
            if length and int(length) != size: raise MirrorError(f"Content-Length mismatch for {name}: expected {size}, got {length}")
            while chunk := response.read(1024 * 1024):
                received += len(chunk)
                if received > size: raise MirrorError(f"Downloaded {name} exceeds advertised size {size}")
                digest.update(chunk); out.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True); raise
    if received != size:
        destination.unlink(missing_ok=True); raise MirrorError(f"Size mismatch for {name}: expected {size}, got {received}")
    return digest.hexdigest()

def gh(*args: str):
    try: subprocess.run(["gh", *args], check=True)
    except FileNotFoundError as exc: raise MirrorError("GitHub CLI (gh) is required") from exc
    except subprocess.CalledProcessError as exc: raise MirrorError(f"GitHub CLI failed with exit code {exc.returncode}") from exc

def release_exists(tag: str) -> bool:
    return subprocess.run(["gh", "release", "view", tag, "--repo", GITHUB_REPO], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def main() -> int:
    global GITEA_URL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Original Pangolin version, e.g. 1.2.42")
    parser.add_argument("--dry-run", action="store_true", help="download and verify only; do not change GitHub")
    parser.add_argument("--replace", action="store_true", help="replace same-named assets in an existing GitHub release")
    parser.add_argument("--gitea-url", default=GITEA_URL, help="Gitea base URL; can use the LAN endpoint")
    args = parser.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version): parser.error("version must be plain semantic version, e.g. 1.2.42")
    GITEA_URL = args.gitea_url.rstrip("/")
    tag = f"client-v{args.version}"
    release = fetch_release(tag)
    by_name = {}
    for asset in release.get("assets", []):
        name = asset.get("name")
        if name in by_name: raise MirrorError(f"Duplicate asset in Gitea release: {name}")
        by_name[name] = asset
    missing = [name for name in ASSET_NAMES if name not in by_name]
    if missing: raise MirrorError("Gitea release is missing required assets: " + ", ".join(missing))
    existing = release_exists(tag)
    if existing and not args.replace and not args.dry_run: raise MirrorError(f"GitHub release {tag} already exists; pass --replace to update assets")
    with tempfile.TemporaryDirectory(prefix=f"pangolin-{tag}-") as temp:
        directory = Path(temp); checksums = []
        for name in ASSET_NAMES:
            digest = download_asset(by_name[name], directory / name)
            checksums.append(f"{digest}  {name}")
            print(f"verified {name}: {by_name[name]['size']} bytes sha256:{digest}")
        checksum_file = directory / "SHA256SUMS.txt"
        checksum_file.write_text("\n".join(checksums) + "\n", encoding="utf-8")
        if args.dry_run:
            print(f"Dry run complete: verified Gitea release {tag}; GitHub was not changed."); return 0
        if not existing:
            notes = (f"Pangolin VPN client {args.version}\n\nWindows x64, Android, and macOS x64 installers mirrored from the official Gitea release.\n\n"
                     f"Source release: {GITEA_URL}/{GITEA_REPO}/releases/tag/{tag}\n"
                     "GitHub source archives belong to this documentation repository; use the installer assets below.\n\n"
                     "## 简体中文\n\n本版本安装包从官方 Gitea Release 转存。源码版本：`" + tag + "`。\n\nmacOS 安装包适用于 Intel x64。SHA-256 校验值见 `SHA256SUMS.txt`。")
            notes_file = directory / "release-notes.md"; notes_file.write_text(notes, encoding="utf-8")
            gh("release", "create", tag, "--repo", GITHUB_REPO, "--target", "main", "--title", f"Pangolin VPN {args.version}", "--notes-file", str(notes_file))
        upload = ["release", "upload", tag, "--repo", GITHUB_REPO]
        if args.replace: upload.append("--clobber")
        gh(*upload, *(str(directory / name) for name in (*ASSET_NAMES, "SHA256SUMS.txt")))
        print(f"Published {tag}: https://github.com/{GITHUB_REPO}/releases/tag/{tag}")
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except MirrorError as exc:
        print(f"error: {exc}", file=sys.stderr); raise SystemExit(1)
