# lazypdf Feature Requests

Feature gaps identified while migrating python-pdf-tools to lazypdf.

---

## 1. `compress()` - Granular compression controls

**Current API:** `compress() -> PDFFile`

**Requested API:** `compress(*, img_quality: int | None = None, compression_level: int = 5) -> PDFFile`

- `img_quality` (1-100): Quality level for image recompression. `None` skips image compression.
- `compression_level` (1-9): Deflate compression level for content streams.

---

## 2. `encrypt()` - Algorithm selection

**Current API:** `encrypt(user_password, *, owner_password=None, permissions=4095) -> PDFFile`

**Requested API:** `encrypt(user_password, *, owner_password=None, permissions=4095, algorithm="AES-256-R5") -> PDFFile`

- `algorithm`: Encryption algorithm. Options: `"AES-256-R5"`, `"AES-256"`, `"AES-128"`, `"RC4-128"`, `"RC4-40"`.

---

## 3. `extract_tables()` - Extraction flavor/strategy

**Current API:** `extract_tables(*, pages=None) -> list[list[list[str]]]`

**Requested API:** `extract_tables(*, pages=None, flavor="lattice") -> list[list[list[str]]]`

- `flavor`: Table detection strategy. `"lattice"` for tables with visible borders, `"stream"` for borderless tables.
