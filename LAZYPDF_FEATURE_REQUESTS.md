# lazypdf Feature Requests

Feature gaps identified while migrating [python-pdf-tools](https://github.com/jmfeck/python-pdf-tools) to lazypdf.

---

## Feature Requests

### 1. `compress()` - Granular compression controls

**Current API:** `compress() -> PDFFile`

**Requested API:** `compress(*, img_quality: int | None = None, compression_level: int = 5) -> PDFFile`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `img_quality` | `int \| None` | `None` | Quality level for image recompression (1-100). `None` skips image compression. |
| `compression_level` | `int` | `5` | Deflate compression level for content streams (1-9). |

**Consumer script:** `compress-pdf/scripts/compress_pdf.py`

---

### 2. `encrypt()` - Algorithm selection

**Current API:** `encrypt(user_password, *, owner_password=None, permissions=4095) -> PDFFile`

**Requested API:** `encrypt(user_password, *, owner_password=None, permissions=4095, algorithm="AES-256-R5") -> PDFFile`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `algorithm` | `str` | `"AES-256-R5"` | Encryption algorithm. Options: `"AES-256-R5"`, `"AES-256"`, `"AES-128"`, `"RC4-128"`, `"RC4-40"`. |

**Consumer script:** `pdf-encryption/scripts/pdf_encryption.py`

---

### 3. `extract_tables()` - Extraction flavor/strategy

**Current API:** `extract_tables(*, pages=None) -> list[list[list[str]]]`

**Requested API:** `extract_tables(*, pages=None, flavor="lattice") -> list[list[list[str]]]`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `flavor` | `str` | `"lattice"` | Table detection strategy. `"lattice"` for tables with visible borders, `"stream"` for borderless tables. |

**Consumer script:** `extract-tables-from-pdf/scripts/extract_tables_from_pdf_camelot.py`

---

### 4. `extract_text()` - Engine system for text extraction + page separators

**Problem:** Currently text extraction and OCR are separate operations (`extract_text()` vs `ocr().extract_text()`). The user has to decide upfront which to use. Should be a single method with an `engine` parameter and built-in page break markers.

**Current API:** `extract_text(*, pages=None, sep="\n") -> str`

**Requested API:** `extract_text(*, pages=None, sep="\n", engine="text", page_separator: str | None = None) -> str`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | `str` | `"text"` | Extraction engine. `"text"` = text layer only, `"ocr"` = force OCR on all pages, `"auto"` = try text first, fallback to OCR per page. |
| `page_separator` | `str \| None` | `None` | Separator inserted between pages. E.g. `"\n--- Page {n} ---\n"`. `{n}` is replaced with page number. `None` = no separator. |

#### Available engines

| Engine | Deps | Description |
|--------|------|-------------|
| `text` (default) | None | Extracts embedded text layer only. Fast, no external deps. |
| `ocr` | pytesseract | Forces OCR on all pages (ignores existing text layer). |
| `auto` | pytesseract | Smart per-page detection: uses text layer if available, falls back to OCR for scanned pages. |

#### Usage

```python
import lazypdf as lz

# Text layer only (default)
text = lz.read("doc.pdf").extract_text()

# Force OCR
text = lz.read("scanned.pdf").extract_text(engine="ocr")

# Auto-detect per page
text = lz.read("mixed.pdf").extract_text(engine="auto")

# With page break markers
text = lz.read("doc.pdf").extract_text(page_separator="\n--- Page {n} ---\n")
# Output:
# --- Page 1 ---
# First page content...
#
# --- Page 2 ---
# Second page content...

# Combine both
text = lz.read("mixed.pdf").extract_text(engine="auto", page_separator="\n--- Page {n} ---\n")
```

**Consumer script:** `extract-text-from-pdf/scripts/extract_text_from_pdf.py`

---

### 5. `read_html()` - Engine system for HTML/URL to PDF

**Problem:** Currently `read_html()` requires WeasyPrint + GTK runtime. GTK is an OS-level dependency that's painful to install on Windows and breaks the "just pip install" experience.

**Current API:** `read_html(path_or_url: str) -> PDFFile`

**Requested API:** `read_html(path_or_url: str, *, engine: str = "pymupdf") -> PDFFile`

#### Available engines

| Engine | Install | Pros | Cons |
|--------|---------|------|------|
| `pymupdf` | None (built-in) | Zero external deps, uses PyMuPDF Story API | Basic CSS support |
| `weasyprint` | `pip install lazypdf[html]` + GTK | Good CSS/layout support | Needs GTK runtime on Windows |
| `playwright` | `pip install lazypdf[browser]` | Best rendering (real Chromium browser) | Heavy dependency (~200MB) |

#### Usage

```python
import lazypdf as lz

# Default - pure Python, works out of the box
lz.read_html("page.html").to_pdf("out.pdf")
lz.read_html("https://example.com").to_pdf("out.pdf")

# Explicit engine selection
lz.read_html("page.html", engine="pymupdf").to_pdf("out.pdf")       # no external deps
lz.read_html("page.html", engine="weasyprint").to_pdf("out.pdf")    # better CSS support
lz.read_html("page.html", engine="playwright").to_pdf("out.pdf")    # best rendering
```

**Consumer scripts:**
- `convert-to-pdf-from-html/scripts/convert_to_pdf_from_html.py`
- `convert-to-pdf-from-url/scripts/convert_to_pdf_from_url.py`

---

### 6. `repair()` - Engine system for PDF repair

**Problem:** The old implementation tried 3 repair methods in sequence (PyMuPDF → pdfplumber → pikepdf). Currently lazypdf only uses PyMuPDF internally. Different engines have different strengths for different types of corruption.

**Current API:** `repair() -> PDFFile`

**Requested API:** `repair(*, engine: str = "auto") -> PDFFile`

#### Available engines

| Engine | Install | Strengths |
|--------|---------|-----------|
| `pymupdf` | None (built-in) | Good for structural issues, xref table repair |
| `pikepdf` | `pip install lazypdf[repair]` | Strong at fixing object stream corruption, linearization issues |
| `auto` (default) | All of above | Tries each engine in order, returns first successful repair |

#### Usage

```python
import lazypdf as lz

# Auto-detect best repair method (default)
lz.read("broken.pdf").repair().to_pdf("fixed.pdf")

# Explicit engine selection
lz.read("broken.pdf").repair(engine="pymupdf").to_pdf("fixed.pdf")
lz.read("broken.pdf").repair(engine="pikepdf").to_pdf("fixed.pdf")
lz.read("broken.pdf").repair(engine="auto").to_pdf("fixed.pdf")
```

**Consumer script:** `repair-pdf/scripts/repair_pdf.py`

---

### 7. `to_pdfa()` - Engine system for PDF/A conversion

**Problem:** Currently `to_pdfa()` requires Ghostscript, which is an OS-level install. Should have a pure-Python default.

**Current API:** `to_pdfa(output_path: str, *, level: int = 2) -> str`

**Requested API:** `to_pdfa(output_path: str, *, level: int = 2, engine: str = "pymupdf") -> str`

#### Available engines

| Engine | Install | Pros | Cons |
|--------|---------|------|------|
| `pymupdf` | None (built-in) | Zero external deps, PyMuPDF metadata + font embedding | May not pass strict PDF/A validators |
| `ghostscript` | Ghostscript binary (OS install) | Industry standard, most compliant | Requires OS-level install, not pip-installable |

#### Usage

```python
import lazypdf as lz

# Default - pure Python, works out of the box
lz.read("input.pdf").to_pdfa("output.pdf")

# Explicit engine selection
lz.read("input.pdf").to_pdfa("output.pdf", engine="pymupdf")       # no external deps
lz.read("input.pdf").to_pdfa("output.pdf", engine="ghostscript")   # most compliant
```

**Consumer script:** `pdfa-conversion/scripts/pdfa_conversion.py`

---

### Engine system - General behavior

These rules apply to all `engine` parameters across the library:

1. **Default is always pure Python** (`pymupdf`) - zero external deps, works with just `pip install lazypdf`
2. **Clear errors** - if user picks an engine that's not installed, raise an error with exact install instructions
3. **Auto mode** - `engine="auto"` picks the best engine available on the system (checks installed deps at runtime)
4. **Lazy imports** - optional engine deps (weasyprint, playwright) are only imported when that engine is selected

---

## Defaults

### 8. `flatten()` - DPI control

**Problem:** `flatten()` rasterizes each page to an image and rebuilds the PDF. The current default DPI (150) produces files 3-4x larger than the originals. Users should be able to control the quality/size tradeoff.

**Current API:** `flatten(*, dpi: int = 150, pages=None) -> PDFFile`

**Proposed change:** Lower default DPI or expose it more prominently. The old fitz-based implementation used `get_pixmap()` without explicit DPI (defaults to 72), producing much smaller files.

| DPI | Quality | Approximate size vs original |
|-----|---------|------------------------------|
| 72 | Low (screen) | ~1x |
| 150 | Medium (default) | ~3-4x |
| 300 | High (print) | ~10-15x |

**Consumer script:** `flatten-pdf/scripts/flatten_pdf.py`

---

### 9. `read_images()` - Default `page_size` should be `"fit"`

**Current default:** `page_size="a4"`

**Proposed default:** `page_size="fit"`

When converting images to PDF, the expected behavior is to preserve the original image dimensions. Forcing A4 as default adds whitespace or distorts the aspect ratio, which is rarely what the user wants. If they need A4, they can pass it explicitly.

```python
# Current - forces A4, user has to know to override
lz.read_images("photo.jpg")                        # A4 page with image inside

# Proposed - preserves original dimensions by default
lz.read_images("photo.jpg")                        # page matches image size
lz.read_images("photo.jpg", page_size="a4")        # explicit A4 when needed
```

---

## Bugs

### 9. `to_pdfa()` - Windows temp file locking

**Severity:** Bug

**Environment:** Windows

When calling `to_pdfa()` with the `ghostscript` engine on Windows, lazypdf creates a temp file for the Ghostscript subprocess but fails to clean it up due to Windows file locking. Ghostscript itself runs fine and produces the output, but lazypdf raises a `PermissionError` when trying to delete the temp file:

```
code=2: cannot remove file 'C:\Users\...\AppData\Local\Temp\tmp....pdf': Permission denied
```

**Suggested fix:** Ensure the temp file handle is fully closed before attempting deletion, or use `tempfile.NamedTemporaryFile(delete_on_close=False)` for Windows compatibility.

---

### 10. `extract_pages()` / `remove_pages()` - Orphaned resources not cleaned up

**Severity:** Bug

**Impact:** Output files are massively bloated (up to 6x larger than expected).

When extracting or removing pages, lazypdf keeps all resources (fonts, images, embedded files) from the original PDF, even those only referenced by removed pages. A single-page extract from a 1.4MB PDF produces a 1.45MB file (99% of original) instead of the expected ~215KB (15%).

**Reproduction:**
```python
import lazypdf as lz

# Original: 1,464,634 bytes (multi-page PDF)
pdf = lz.read("input.pdf")

# Expected: ~215,000 bytes (just page 1 resources)
# Actual:  1,451,769 bytes (99% of original - all resources kept)
pdf.extract_pages([1]).to_pdf("page1.pdf")
```

**Workaround:** Chain `.compress()` after `extract_pages()` to garbage-collect orphaned resources:
```python
pdf.extract_pages([1]).compress().to_pdf("page1.pdf")  # 217,399 bytes - correct
```

**Suggested fix:** `extract_pages()` and `remove_pages()` should automatically run orphan resource cleanup (equivalent to what `compress()` does internally with `remove_identicals` / `remove_orphans`).
