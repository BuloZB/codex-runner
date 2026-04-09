from __future__ import annotations

import json
from pathlib import Path
import sys
import time


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 3:
        print("usage: python -m codex_runner.notify_hook <role> <output_path> <payload_json>", file=sys.stderr)
        return 2

    role, output_path_text, payload_json = args
    output_path = Path(output_path_text)
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as exc:
        print(f"invalid hook payload: {exc}", file=sys.stderr)
        return 1

    normalized_payload = {}
    if isinstance(payload, dict):
        normalized_payload = {str(key).replace("-", "_"): value for key, value in payload.items()}
    event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "role": role,
        **normalized_payload,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
