"""Strict public catalog validator (stdlib only, offline)."""
from __future__ import annotations
import ipaddress
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TOP = {"schema_version", "generated_by", "products"}
REQUIRED_ITEM = {"id", "name", "summary", "kind", "tags", "release_stage", "launch_path", "links"}
REQUIRED_LINK = {"type", "url", "label"}
KINDS = {"tool", "software", "demo", "documentation"}
LINK_KINDS = {"website", "demo", "documentation", "release", "source_repo", "package_registry"}
SECRET_PATTERN = re.compile(r"sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|(?:[A-Za-z]:[\\/])|(?:/Users/|/home/|/mnt/|/root/)")


def validate(value: dict) -> dict:
    if not isinstance(value, dict) or set(value) != REQUIRED_TOP or value["schema_version"] != 1:
        raise ValueError("catalog: unexpected top-level schema")
    if not isinstance(value["generated_by"], str) or not value["generated_by"].strip():
        raise ValueError("catalog: invalid provenance")
    rows = value["products"]
    if not isinstance(rows, list) or len(rows) > 500:
        raise ValueError("catalog: products must be a bounded list")
    ids = set()
    for p in rows:
        if not isinstance(p, dict) or set(p) != REQUIRED_ITEM: raise ValueError("product schema invalid")
        if not isinstance(p["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,79}", p["id"]): raise ValueError("invalid public id")
        if p["id"] in ids: raise ValueError("duplicate public id")
        ids.add(p["id"])
        for key, maxsize in (("name", 140), ("summary", 360)):
            if not isinstance(p[key], str) or not p[key].strip() or len(p[key]) > maxsize or SECRET_PATTERN.search(p[key]): raise ValueError(f"unsafe {key}")
        if p["kind"] not in KINDS or p["release_stage"] not in {"preview", "published"}:
            raise ValueError("invalid category or stage")
        tags = p["tags"]
        if not isinstance(tags, list) or len(tags) > 12 or not all(isinstance(t, str) and 0 < len(t) <= 45 and not SECRET_PATTERN.search(t) for t in tags):
            raise ValueError("invalid tags")
        path = p["launch_path"]
        if path is not None:
            if not isinstance(path, str) or not re.fullmatch(r"/(?:tools|apps)/[a-z0-9/-]+/?", path) or '..' in path:
                raise ValueError("invalid launch path")
            destination = (ROOT / path.lstrip('/') / "index.html")
            if not destination.is_file() or not destination.resolve().is_relative_to(ROOT):
                raise ValueError(f"launch path does not resolve to a local page: {path}")
        links = p["links"]
        if not isinstance(links, list) or len(links) > 25: raise ValueError("invalid links")
        for l in links:
            if not isinstance(l, dict) or set(l) != REQUIRED_LINK or l["type"] not in LINK_KINDS:
                raise ValueError("link shape invalid")
            if not isinstance(l["label"], str) or not l["label"].strip() or len(l["label"]) > 120 or SECRET_PATTERN.search(l["label"]): raise ValueError("invalid link label")
            if not isinstance(l["url"], str): raise ValueError("invalid link url")
            u = urlsplit(l["url"]); h = u.hostname
            if u.scheme != 'https' or not h or u.username or u.password:
                raise ValueError("link url must be external HTTPS")
            if h.lower() in {"localhost", "127.0.0.1", "0.0.0.0"} or h.endswith((".local", ".internal", ".localhost")):
                raise ValueError("private domain in public URL")
            try: ipaddress.ip_address(h)
            except ValueError: pass
            else: raise ValueError("IP literal in public URL")
            if u.port is not None and u.port != 443: raise ValueError("custom public URL port")
    return value


if __name__ == '__main__':
    try:
        data=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
        validate(data)
        print(f"PASS: public catalog validated; {len(data['products'])} entries; no network calls")
    except (OSError, ValueError, json.JSONDecodeError) as err:
        print(f"FAIL_CLOSED: {err}")
        raise SystemExit(1)
