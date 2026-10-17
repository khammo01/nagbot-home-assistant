#!/usr/bin/env python3
"""Parse blueprints and reject private-installation artifacts."""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINTS = ROOT / "blueprints" / "automation"


class BlueprintLoader(yaml.SafeLoader):
    pass


def input_constructor(loader: BlueprintLoader, node: yaml.Node) -> dict[str, str]:
    return {"__blueprint_input__": loader.construct_scalar(node)}


BlueprintLoader.add_constructor("!input", input_constructor)

PRIVATE_WORDS = (
    "page_access_token",
    "bearer_token",
    "client_secret",
    "notify.messenger",
    "nagbot_messenger_input",
)
IP_PATTERN = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")


def iter_inputs(inputs: dict) -> list[str]:
    found: list[str] = []
    for name, value in inputs.items():
        if isinstance(value, dict) and "input" in value:
            found.extend(iter_inputs(value["input"]))
        else:
            found.append(name)
    return found


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text()
    try:
        data = yaml.load(text, Loader=BlueprintLoader)
    except yaml.YAMLError as error:
        return [f"{path}: invalid YAML: {error}"]

    if not isinstance(data, dict):
        return [f"{path}: top level must be a mapping"]
    metadata = data.get("blueprint")
    if not isinstance(metadata, dict):
        errors.append(f"{path}: missing blueprint metadata")
        return errors
    if metadata.get("domain") != "automation":
        errors.append(f"{path}: blueprint domain must be automation")
    for key in ("name", "description", "author", "input"):
        if not metadata.get(key):
            errors.append(f"{path}: missing blueprint.{key}")
    if not data.get("triggers"):
        errors.append(f"{path}: missing triggers")
    if not data.get("actions"):
        errors.append(f"{path}: missing actions")

    declared = set(iter_inputs(metadata.get("input", {})))
    referenced = set(re.findall(r"!input\s+([a-zA-Z0-9_]+)", text))
    missing = referenced - declared
    unused = declared - referenced
    if missing:
        errors.append(f"{path}: undeclared inputs: {sorted(missing)}")
    if unused:
        errors.append(f"{path}: unused inputs: {sorted(unused)}")

    lowered = text.lower()
    for word in PRIVATE_WORDS:
        if word in lowered:
            errors.append(f"{path}: contains forbidden private token name {word!r}")
    for match in IP_PATTERN.finditer(text):
        try:
            address = ipaddress.ip_address(match.group())
        except ValueError:
            continue
        if address.is_private:
            errors.append(f"{path}: contains private IP address")
    return errors


def main() -> int:
    files = sorted(BLUEPRINTS.rglob("*.yaml"))
    if not files:
        print("No blueprints found")
        return 1
    errors = [error for path in files for error in check_file(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(files)} blueprints; no private artifacts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
