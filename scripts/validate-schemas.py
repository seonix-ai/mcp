#!/usr/bin/env python3
"""Validate plugins/seonix/plugin.json and mcp.json against the Agent Plugins
1.0.0 schemas.

Run with `python3 -I scripts/validate-schemas.py` from the repository root.
The schemas are fetched from agent-plugins.org (the `$schema` URLs in the
files). No third-party packages: a small validator covering the keywords the
two schemas use (type, properties, required, additionalProperties, pattern,
const, minLength, maxLength, items, oneOf, $ref, propertyNames, not, enum).

Exit code 0 when both files validate, 1 otherwise. Keeps going after the first
error so the report is complete.

Known tension, reported but not treated as a failure: OpenAI's documentation
places per-server auth under `extensions.com.openai` inside the server entry,
while the 1.0.0 mcp.schema.json declares server entries closed
(`additionalProperties: false`). The script validates mcp.json twice: as
written (expects the single `extensions` finding) and with server-level
`extensions` removed (must be clean).
"""
from __future__ import annotations

import copy
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "plugins" / "seonix"


def fetch(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=20) as resp:  # noqa: S310 - fixed https URLs from the manifests
        return json.load(resp)


class Validator:
    def __init__(self, schema: dict):
        self.root = schema
        self.errors: list[str] = []

    def resolve(self, ref: str) -> dict:
        assert ref.startswith("#/"), ref
        node: object = self.root
        for part in ref[2:].split("/"):
            node = node[part]  # type: ignore[index]
        return node  # type: ignore[return-value]

    def check(self, inst: object, schema: dict, path: str) -> list[str]:
        errs: list[str] = []
        if "$ref" in schema:
            return self.check(inst, self.resolve(schema["$ref"]), path)
        if "oneOf" in schema:
            passing = []
            branch_errs = []
            for i, sub in enumerate(schema["oneOf"]):
                e = self.check(inst, sub, path)
                if not e:
                    passing.append(i)
                branch_errs.append(e)
            if len(passing) != 1:
                titles = []
                for i, s in enumerate(schema["oneOf"]):
                    resolved = self.resolve(s["$ref"]) if "$ref" in s else s
                    titles.append(resolved.get("title", f"#{i}"))
                errs.append(f"{path}: must match exactly one of {titles}, matched {len(passing)}")
                for t, e in zip(titles, branch_errs):
                    for line in e:
                        errs.append(f"{path}: [{t}] {line}")
            return errs
        if "const" in schema and inst != schema["const"]:
            errs.append(f"{path}: must equal {schema['const']!r}")
        if "enum" in schema and inst not in schema["enum"]:
            errs.append(f"{path}: must be one of {schema['enum']!r}")
        if "not" in schema and not self.check(inst, schema["not"], path):
            errs.append(f"{path}: must not match {schema['not']!r}")
        t = schema.get("type")
        if t:
            ok = {
                "object": isinstance(inst, dict),
                "array": isinstance(inst, list),
                "string": isinstance(inst, str),
                "boolean": isinstance(inst, bool),
                "number": isinstance(inst, (int, float)) and not isinstance(inst, bool),
            }[t]
            if not ok:
                errs.append(f"{path}: expected {t}")
                return errs
        if isinstance(inst, str):
            if "minLength" in schema and len(inst) < schema["minLength"]:
                errs.append(f"{path}: shorter than {schema['minLength']}")
            if "maxLength" in schema and len(inst) > schema["maxLength"]:
                errs.append(f"{path}: longer than {schema['maxLength']}")
            if "pattern" in schema and not re.search(schema["pattern"], inst):
                errs.append(f"{path}: does not match /{schema['pattern']}/")
        if isinstance(inst, list) and "items" in schema:
            for i, item in enumerate(inst):
                errs += self.check(item, schema["items"], f"{path}[{i}]")
        if isinstance(inst, dict):
            for key in schema.get("required", []):
                if key not in inst:
                    errs.append(f"{path}: missing required '{key}'")
            props = schema.get("properties", {})
            for key, val in inst.items():
                if key in props:
                    errs += self.check(val, props[key], f"{path}.{key}")
                elif "additionalProperties" in schema:
                    ap = schema["additionalProperties"]
                    if ap is False:
                        errs.append(f"{path}: unexpected property '{key}'")
                    elif isinstance(ap, dict):
                        errs += self.check(val, ap, f"{path}.{key}")
                if "propertyNames" in schema:
                    errs += self.check(key, schema["propertyNames"], f"{path}.<key {key}>")
        return errs


def report(title: str, errs: list[str]) -> bool:
    if errs:
        print(f"FAIL {title}")
        for e in errs:
            print(f"  - {e}")
        return False
    print(f"OK   {title}")
    return True


def main() -> int:
    ok = True
    plugin = json.loads((ROOT / "plugin.json").read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())

    plugin_schema = fetch(plugin["$schema"])
    mcp_schema = fetch(mcp["$schema"])
    print(f"schemas: {plugin_schema['$id']} ; {mcp_schema['$id']}")

    ok &= report("plugin.json", Validator(plugin_schema).check(plugin, plugin_schema, "$"))

    stripped = copy.deepcopy(mcp)
    had_ext = False
    for server in stripped["mcpServers"].values():
        had_ext |= server.pop("extensions", None) is not None
    stripped_errs = Validator(mcp_schema).check(stripped, mcp_schema, "$")
    ok &= report("mcp.json without server-level extensions", stripped_errs)

    as_written = Validator(mcp_schema).check(mcp, mcp_schema, "$")
    tag = "mcp.json as written"
    if as_written and had_ext and not stripped_errs:
        # The only difference from the clean document is the per-server
        # `extensions` key that OpenAI's docs require for the auth declaration.
        print(f"NOTE {tag}: fails only because server entries carry `extensions` "
              "(OpenAI per-server auth), which the closed 1.0.0 server schema does not allow")
    else:
        ok &= report(tag, as_written)

    # Cross-file consistency the schemas cannot express.
    cross: list[str] = []
    oai = plugin.get("extensions", {}).get("com.openai", {})
    iface = oai.get("interface", {})
    for key in ("logo", "composerIcon"):
        p = iface.get(key)
        if not p:
            cross.append(f"interface.{key} missing")
        elif not (ROOT / p).is_file():
            cross.append(f"interface.{key} -> {p} not found")
    skill = oai.get("onboardingSkill")
    if skill and not (ROOT / skill).is_file():
        cross.append(f"onboardingSkill -> {skill} not found")
    if len(mcp["mcpServers"]) != 1:
        cross.append("submission requires exactly one MCP server")
    for name, server in mcp["mcpServers"].items():
        if server.get("headers"):
            cross.append(f"server {name}: public submission rejects non-empty headers")
    review = oai.get("review", {})
    cases = review.get("test_cases", {})
    if len(cases.get("positive", [])) != 5 or len(cases.get("negative", [])) != 3:
        cross.append("review.test_cases must have 5 positive and 3 negative cases")
    if "commerce" not in review:
        cross.append("review.commerce missing")
    if len(iface.get("shortDescription", "")) > 30 or len(iface.get("displayName", "")) > 30:
        cross.append("displayName/shortDescription over 30 characters")
    for name in ("seonix",):
        for other in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
            if json.loads((ROOT / other).read_text()).get("name") != name:
                cross.append(f"{other}: name differs from plugin.json")
    ok &= report("cross-file checks", cross)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
