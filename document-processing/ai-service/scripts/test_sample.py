import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a sample invoice text file to the AI service.")
    parser.add_argument("sample_path", type=Path)
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/extract-invoice",
        help="Invoice extraction endpoint URL.",
    )
    args = parser.parse_args()

    document_text = args.sample_path.read_text()
    payload = json.dumps({"documentText": document_text}).encode("utf-8")
    request = urllib.request.Request(
        args.url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(json.loads(body), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

