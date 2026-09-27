#!/usr/bin/env python3
"""Company-local reviewed correction rules. Trusted local callers own approval identity.

Writes use private sibling temporary files. Acceptance writes the page first and
rolls it back if saving the accepted proposal fails; no rule activates on failure.
These local primitives do not provide multi-process transaction isolation.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any


def _string(value, label, empty=False):
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{label} must be a string" )
    return value


def _safe_path(root: Path, rel: str) -> Path:
    root = Path(os.path.abspath(root))
    # macOS /tmp itself is a system alias; reject aliases at company root
    # and all descendants, while allowing OS parent directory aliases.
    for ancestor in (root, *root.parents):
        if ancestor.is_symlink() and ancestor not in (Path("/tmp"), Path("/var")):
            raise ValueError("symlink root")
    _string(rel, "path")
    part = Path(rel)
    if part.is_absolute() or ".." in part.parts or part == Path("."):
        raise ValueError("path escapes root")
    current = root
    for component in part.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError("symlink path")
    return current


def _wiki(root):
    root = Path(root)
    if ".." in root.parts:
        raise ValueError("root traversal not allowed")
    if not root.is_dir():
        raise ValueError("company root must be an existing directory")
    return _safe_path(root, "wiki")


def _page_path(wiki, scope):
    path = _safe_path(wiki, scope)
    if Path(scope).as_posix() != scope or Path(scope).suffix.lower() not in (".md", ".markdown") or Path(scope).parts[0] == "corrections":
        raise ValueError("scope must be a canonical relative Markdown page")
    return path


def _atomic_write(path: Path, data: bytes) -> None:
    if path.is_symlink() or path.parent.is_symlink():
        raise ValueError("symlink write")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink():
            raise ValueError("symlink write")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def _read_json(path):
    if path.is_symlink():
        raise ValueError("symlink read")
    try:
        return json.loads(path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("invalid JSON store") from exc


def _write_json(path, obj):
    _atomic_write(path, (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode())


def _sha256_of(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _record(record):
    if not isinstance(record, dict):
        raise ValueError("correction must be an object")
    for key in ("original", "rewrite", "reason", "scope"):
        _string(record.get(key), key, empty=key == "rewrite")
    if "example" in record:
        _string(record["example"], "example")
    return record


def record_correction(root: Path, record: dict[str, str]) -> str:
    _record(record)
    wiki = _wiki(root)
    _page_path(wiki, record["scope"])
    directory = _safe_path(wiki, "corrections")
    cid = str(uuid.uuid4())
    entry = {key: record[key] for key in ("original", "rewrite", "reason", "scope")}
    entry.update(id=cid, example=record.get("example", {"original": record["original"], "rewrite": record["rewrite"]}))
    _write_json(_safe_path(directory, cid + ".json"), entry)
    return cid


def _pairs(value):
    if not isinstance(value, list) or not value:
        raise ValueError("missing frozen rewrites")
    result = {}
    for pair in value:
        if not isinstance(pair, dict):
            raise ValueError("invalid rewrite")
        original = _string(pair.get("original"), "original")
        rewrite = _string(pair.get("rewrite"), "rewrite", empty=True)
        if original in result and result[original] != rewrite:
            raise ValueError("conflicting rewrites")
        result[original] = rewrite
    return result


def _load_proposals(path):
    if path.is_symlink():
        raise ValueError("symlink store")
    if not path.exists():
        return []
    proposals = _read_json(path)
    if not isinstance(proposals, list):
        raise ValueError("proposals must be a list")
    ids = set()
    for p in proposals:
        if not isinstance(p, dict):
            raise ValueError("invalid proposal")
        for field in ("id", "scope", "reason", "status"):
            _string(p.get(field), field)
        if p["id"] in ids or p["status"] not in ("pending", "conflict", "accepted", "rejected"):
            raise ValueError("invalid proposal identity/status")
        ids.add(p["id"])
        if not isinstance(p.get("evidence"), list) or len(p["evidence"]) < 2 or any(not isinstance(x, str) or not x for x in p["evidence"]) or len(set(p["evidence"])) != len(p["evidence"]):
            raise ValueError("proposal requires two distinct evidences")
        if p["status"] != "conflict":
            _pairs(p.get("rewrites"))
        if p["status"] == "accepted":
            _string(p.get("approver"), "approver")
            if not re.fullmatch(r"[0-9a-f]{64}", str(p.get("page_sha256", ""))):
                raise ValueError("invalid accepted digest")
    return proposals


def _save_proposals(path, proposals):
    _write_json(path, proposals)


def propose_rule(root: Path, scope: str, reason: str) -> str:
    wiki = _wiki(root)
    _page_path(wiki, scope)
    _string(reason, "reason")
    path = _safe_path(wiki, "proposals.json")
    proposals = _load_proposals(path)
    directory = _safe_path(wiki, "corrections")
    evidence, rewrites = [], []
    if directory.exists():
        for file in sorted(directory.glob("*.json")):
            entry = _read_json(_safe_path(directory, file.name))
            if not isinstance(entry, dict):
                raise ValueError("invalid correction store")
            for field in ("id", "original", "rewrite", "reason", "scope"):
                _string(entry.get(field), field, empty=field == "rewrite")
            if entry["id"] + ".json" != file.name:
                raise ValueError("correction identity mismatch")
            _page_path(wiki, entry["scope"])
            if entry["reason"] == reason and entry["scope"] == scope:
                evidence.append(entry["id"])
                rewrites.append({"original": entry["original"], "rewrite": entry["rewrite"]})
    if len(evidence) < 2:
        raise ValueError("repeated reason requires at least two corrections")
    status = "pending"
    try:
        _pairs(rewrites)
    except ValueError:
        status = "conflict"
    pid = str(uuid.uuid4())
    proposals.append(dict(id=pid, scope=scope, reason=reason, status=status, evidence=evidence, rewrites=rewrites))
    _save_proposals(path, proposals)
    return pid


def accept_rule(root: Path, proposal_id: str, approver: str, expected_sha256: str) -> None:
    _string(approver, "approver")
    wiki = _wiki(root)
    path = _safe_path(wiki, "proposals.json")
    proposals = _load_proposals(path)
    proposal = next((p for p in proposals if p["id"] == proposal_id), None)
    if proposal is None:
        raise ValueError("proposal not found")
    if proposal["status"] != "pending":
        raise ValueError("proposal already accepted/rejected or conflicting")
    pairs = _pairs(proposal["rewrites"])
    for other in proposals:
        if other["status"] == "accepted" and other["scope"] == proposal["scope"]:
            for original, rewrite in _pairs(other["rewrites"]).items():
                if original in pairs and pairs[original] != rewrite:
                    raise ValueError("conflicting accepted rewrite")
    page = _page_path(wiki, proposal["scope"])
    if not page.is_file():
        raise ValueError("scope page does not exist")
    original = page.read_bytes()
    if hashlib.sha256(original).hexdigest() != expected_sha256:
        raise ValueError("page digest mismatch")
    # JSON string values prevent line/comment injection from review metadata.
    metadata = json.dumps({"approver": approver.strip(), "reason": proposal["reason"]}, ensure_ascii=True).replace("--", "\\u002d\\u002d")
    marker = f"\n<!-- rule:{proposal_id} accepted {metadata} -->\n".encode()
    proposal.update(status="accepted", approver=approver.strip(), page_sha256=expected_sha256)
    _atomic_write(page, original + marker)
    try:
        _save_proposals(path, proposals)
    except BaseException as failure:
        try:
            _atomic_write(page, original)
        except BaseException as rollback:
            raise RuntimeError("acceptance not activated; page rollback failed, manual restoration required") from rollback
        raise failure


def apply_corrections(root: Path, page: str, text: str) -> str:
    _string(text, "text", empty=True)
    wiki = _wiki(root)
    _page_path(wiki, page)
    proposals = _load_proposals(_safe_path(wiki, "proposals.json"))
    rewrites = {}
    conflicts = set()
    for p in proposals:
        if p["status"] == "accepted" and p["scope"] == page:
            for original, rewrite in _pairs(p["rewrites"]).items():
                if original in rewrites and rewrites[original] != rewrite:
                    conflicts.add(original)
                rewrites[original] = rewrite
    # Simultaneous replacement avoids cascading accepted transformations.
    if conflicts:
        raise ValueError("conflicting accepted rewrites require review")
    if not rewrites:
        return text
    pattern = "|".join(re.escape(key) for key in sorted(rewrites, key=len, reverse=True))
    return re.sub(pattern, lambda match: rewrites[match.group()], text)


def _cmd_record(root: Path, argv: list[str]) -> int:
    """record-correction --original TEXT --rewrite TEXT --reason TEXT --scope PAGE"""
    record: dict[str, str] = {}
    index = 0
    while index < len(argv) - 1:
        key = argv[index].lstrip("-").replace("-", "_")
        record[key] = argv[index + 1]
        index += 2
    try:
        cid = record_correction(root, record)
        print(cid)
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _cmd_propose(root: Path, argv: list[str]) -> int:
    """propose-rule --scope PAGE --reason TEXT"""
    kwargs: dict[str, str] = {}
    index = 0
    while index < len(argv) - 1:
        key = argv[index].lstrip("-")
        kwargs[key] = argv[index + 1]
        index += 2
    try:
        pid = propose_rule(root, kwargs["scope"], kwargs["reason"])
        print(pid)
        return 0
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _cmd_accept(root: Path, argv: list[str]) -> int:
    """accept-rule --proposal-id ID --approver NAME --expected-sha256 DIGEST"""
    kwargs: dict[str, str] = {}
    index = 0
    while index < len(argv) - 1:
        key = argv[index].lstrip("-").replace("-", "_")
        kwargs[key] = argv[index + 1]
        index += 2
    try:
        accept_rule(root, kwargs["proposal_id"], kwargs["approver"], kwargs["expected_sha256"])
        print("accepted")
        return 0
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _cmd_apply(root: Path, argv: list[str]) -> int:
    """apply-corrections --page PAGE --text TEXT (or reads stdin)"""
    kwargs: dict[str, str] = {}
    index = 0
    while index < len(argv) - 1:
        key = argv[index].lstrip("-")
        kwargs[key] = argv[index + 1]
        index += 2
    page = kwargs.get("page", "")
    text = kwargs.get("text") or sys.stdin.read()
    try:
        result = apply_corrections(root, page, text)
        print(result, end="")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


USAGE = (
    "usage: corrections.py <root> "
    "record-correction|propose-rule|accept-rule|apply-corrections [options]"
)

SUBCOMMANDS = {
    "record-correction": _cmd_record,
    "propose-rule": _cmd_propose,
    "accept-rule": _cmd_accept,
    "apply-corrections": _cmd_apply,
}


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(USAGE, file=sys.stderr)
        return 2
    root = Path(argv[1])
    subcmd = argv[2]
    if subcmd not in SUBCOMMANDS:
        print(f"unknown subcommand: {subcmd!r}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    return SUBCOMMANDS[subcmd](root, argv[3:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
