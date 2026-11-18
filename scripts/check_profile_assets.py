#!/usr/bin/env python3
"""Validate README media references and SVG assets without third-party dependencies."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSET_RE = re.compile(r"(?:\./)?assets/[A-Za-z0-9_./-]+\.svg")
SVG_NS = "{http://www.w3.org/2000/svg}"


def main() -> int:
    if not README.is_file():
        print("ERROR: Missing profile README.md")
        return 1

    readme = README.read_text(encoding="utf-8")
    references = sorted(set(ASSET_RE.findall(readme)))
    errors: list[str] = []

    if not references:
        errors.append("README references no local SVG assets.")

    for reference in references:
        resolved = (ROOT / reference).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.is_file():
            errors.append(f"Missing or unsafe asset reference: {reference}")
            continue

        if resolved.stat().st_size > 200_000:
            errors.append(f"SVG too large (>200 KB): {reference}")
        try:
            tree = ET.parse(resolved)
            root = tree.getroot()
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG XML: {reference}: {exc}")
            continue

        if root.tag != f"{SVG_NS}svg":
            errors.append(f"Invalid SVG root/namespace: {reference}")
        if not root.get("viewBox"):
            errors.append(f"Missing responsive viewBox: {reference}")

        has_title = any(node.tag == f"{SVG_NS}title" for node in root.iter())
        has_label = bool(root.get("aria-label"))
        if not (has_title or has_label):
            errors.append(f"SVG lacks an accessible title or aria-label: {reference}")

        for node in root.iter():
            local_name = node.tag.split("}")[-1] if isinstance(node.tag, str) else ""
            if local_name in {"script", "foreignObject"}:
                errors.append(f"Disallowed SVG element <{local_name}>: {reference}")
            for key, value in node.attrib.items():
                local_attr = key.split("}")[-1]
                if local_attr in {"href", "src"} and value.startswith(("http:", "https:", "//")):
                    errors.append(f"External SVG dependency: {reference}")

        print(f"OK  {reference}")

    if errors:
        print("\nProfile asset validation FAILED:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"\nProfile asset validation passed ({len(references)} SVG references).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
