"""
Uploads a document (plus optional attachments) to AlphaSense:
POST {base}/services/i/ingestion-api/v1/upload-document

- Headers:
  * Authorization: Bearer <token>
  * ClientId: <client id>  (e.g., "webapp")

- Body (multipart/form-data):
  * file:        primary file (required)
  * attachments: zero or more additional files (repeat the 'attachments' key)
  * metadata:    JSON string (IngestionMetadataWithSourceId)  e.g. {"sourceId":"abc123", "title":"..."}
"""

import os
import argparse
import pathlib
import mimetypes
import json
import requests
from typing import List

SUPPORTED_EXTS = {
    ".pdf", ".html", ".htm", ".txt", ".doc", ".docx", ".xls", ".xlsx",
    ".ppt", ".pptx", ".msg", ".eml", ".csv", ".xlsb", ".xlsm", ".one",
    ".tsv", ".ods"
}

def ensure_supported(path: pathlib.Path) -> None:
    if path.suffix.lower() not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported extension for {path.name}. Allowed: {', '.join(sorted(SUPPORTED_EXTS))}")

def guess_mime(path: pathlib.Path) -> str:
    return mimetypes.guess_type(str(path))[0] or "application/octet-stream"

def build_files(primary: pathlib.Path, attachments: List[pathlib.Path]):
    """Build the 'files' list for requests.post with correct field names."""
    files = [
        ("file", (primary.name, open(primary, "rb"), guess_mime(primary)))
    ]
    for att in attachments:
        files.append(("attachments", (att.name, open(att, "rb"), guess_mime(att))))
    return files

def main():
    p = argparse.ArgumentParser(description="Upload a document + attachments to AlphaSense /v1/upload-document")
    p.add_argument("--base-url", default=os.getenv("ALPHASENSE_BASE_URL", "https://research.alpha-sense.com"),
                   help="Base URL. For enterprise, use https://<user.enterprise.host>")
    p.add_argument("--bearer-token", default=os.getenv("ALPHASENSE_BEARER_TOKEN", ""),
                   help="OAuth bearer token for Authorization header")
    p.add_argument("--client-id", default=os.getenv("ALPHASENSE_CLIENT_ID", "webapp"),
                   help='ClientId header value (e.g., "webapp")')
    p.add_argument("--file", required=True, help="Primary document path")
    p.add_argument("--attachments", nargs="*", default=[], help="Zero or more attachment file paths")
    p.add_argument("--metadata", default='{"sourceId":"sample-source","title":"Sample Upload"}',
                   help="JSON string for IngestionMetadataWithSourceId")
    p.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds")
    args = p.parse_args()

    # Resolve endpoint
    url = f"{args.base_url.rstrip('/')}/services/i/ingestion-api/v1/upload-document"

    # Validate inputs
    primary = pathlib.Path(args.file).expanduser().resolve()
    if not primary.exists():
        raise SystemExit(f"Primary file not found: {primary}")
    ensure_supported(primary)

    att_paths: List[pathlib.Path] = []
    for a in args.attachments:
        ap = pathlib.Path(a).expanduser().resolve()
        if not ap.exists():
            raise SystemExit(f"Attachment not found: {ap}")
        ensure_supported(ap)
        att_paths.append(ap)

    # Parse metadata string (keep as string when sending)
    try:
        md_obj = json.loads(args.metadata)  # validate it's valid JSON
    except json.JSONDecodeError as e:
        raise SystemExit(f"--metadata must be valid JSON: {e}")

    # Build request
    headers = {
        "Authorization": f"Bearer {args.bearer_token}",
        "ClientId": args.client_id,
        "Accept": "application/json",
    }
    if not args.bearer_token:
        raise SystemExit("Missing bearer token. Set --bearer-token or ALPHASENSE_BEARER_TOKEN")

    files = build_files(primary, att_paths)
    data = {"metadata": json.dumps(md_obj)}  # send as string field

    # Send
    resp = requests.post(url, headers=headers, files=files, data=data, timeout=args.timeout)

    # Handle documented responses
    ct = resp.headers.get("Content-Type", "")
    body = None
    if "application/json" in ct:
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
    else:
        body = {"raw": resp.text}

    if resp.status_code == 200:
        print("[200 OK] Upload succeeded")
        print(json.dumps(body, indent=2))
    elif resp.status_code == 403:
        print("[403] You don't have access to this feature")
        print(json.dumps(body, indent=2))
    elif resp.status_code == 404:
        print("[404] Not Found (check URL/host)")
        print(json.dumps(body, indent=2))
    elif resp.status_code == 413:
        print("[413] Maximum upload size exceeded (file must be <= 100MB)")
        print(json.dumps(body, indent=2))
    elif resp.status_code == 503:
        print("[503] Service Unavailable (try again later)")
        print(json.dumps(body, indent=2))
    else:
        print(f"[{resp.status_code}] Unexpected response")
        print(json.dumps(body, indent=2))

if __name__ == "__main__":
    main()
