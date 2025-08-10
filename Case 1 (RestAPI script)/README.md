# AlphaSense Ingestion – Minimal Upload Script

A Python script to upload a document (plus optional attachments) to the **AlphaSense Ingestion API**.

---

## Features

- **Endpoint:** `POST {base}/services/i/ingestion-api/v1/upload-document`
- **Headers:**
  - `Authorization: Bearer <token>` (required)
  - `ClientId: <client id>` (required, e.g., `"webapp"`)
- **Body** (`multipart/form-data`):
  - `file` *(required)* – primary file
  - `attachments` *(optional)* – zero or more additional files (repeat the `attachments` key)
  - `metadata` *(required)* – JSON string (e.g. `{"sourceId":"abc123","title":"..."}`)
- **Supported file extensions:**
  ```
  pdf, html, htm, txt, doc, docx, xls, xlsx, ppt, pptx,
  msg, eml, csv, xlsb, xlsm, one, tsv, ods
  ```

---

## Installation

### Requirements
- Python 3.9+
- `requests` library

Install dependencies:
```bash
pip install requests
```

---

## Configuration

You can provide parameters via **command-line flags** or **environment variables**.

### Environment variables:
```bash
export ALPHASENSE_BASE_URL="https://research.alpha-sense.com"
# or for enterprise:
export ALPHASENSE_BASE_URL="https://user.enterprise.host"

export ALPHASENSE_BEARER_TOKEN="<your-oauth-bearer-token>"
export ALPHASENSE_CLIENT_ID="webapp"  # or your tenant's client id
```

---

## Usage

### Minimal upload (no attachments):
```bash
python ingest_alphasense.py   --file ./sample/report.pdf   --metadata '{"sourceId":"src-001","title":"Q2 Earnings Deck"}'
```

### With attachments:
```bash
python ingest_alphasense.py  --file ./sample/report.pdf   --attachments ./sample/report_tables.xlsx ./sample/images.zip   --metadata '{"sourceId":"src-001","title":"Q2 Earnings Deck","tags":["demo","internal"]}'
```

---

## Using an Enterprise URL

If you are on an enterprise instance, replace the base URL with your enterprise host:

**Option 1 – Environment variable**
```bash
export ALPHASENSE_BASE_URL="https://user.enterprise.host"
python ingest_alphasense.py   --file ./sample/report.pdf   --metadata '{"sourceId":"src-001","title":"Enterprise Test"}'
```

**Option 2 – CLI flag**
```bash
python ingest_alphasense.py   --base-url https://user.enterprise.host   --file ./sample/report.pdf   --metadata '{"sourceId":"src-001","title":"Enterprise Test"}'
```

Both will produce:
```
https://user.enterprise.host/services/i/ingestion-api/v1/upload-document
```

---

## Command-line arguments

| Argument         | Required | Description |
|------------------|----------|-------------|
| `--base-url`     | No       | Base URL for the API (defaults to `ALPHASENSE_BASE_URL`) |
| `--bearer-token` | Yes      | OAuth Bearer token (defaults to `ALPHASENSE_BEARER_TOKEN`) |
| `--client-id`    | Yes      | Client ID header value (defaults to `ALPHASENSE_CLIENT_ID`) |
| `--file`         | Yes      | Primary document path |
| `--attachments`  | No       | Zero or more attachment file paths |
| `--metadata`     | Yes      | JSON string for `IngestionMetadataWithSourceId` |
| `--timeout`      | No       | HTTP timeout in seconds (default: 60) |

---

## Metadata example

```json
{
  "sourceId": "src-001",
  "title": "Q2 2025 Earnings Deck",
  "language": "en",
  "documentType": "presentation",
  "tags": ["earnings", "IR"],
  "properties": {
    "business_unit": "NA",
    "confidentiality": "internal"
  }
}
```

---

## Error handling

The script prints clear messages for the following HTTP responses:

- **200 OK** – Upload succeeded
- **403** – You don't have access to this feature
- **404** – Not found (check URL/host)
- **413** – Maximum upload size exceeded (≤ 100MB per file)
- **503** – Service unavailable (retry later)

---