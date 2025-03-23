# Python PDF Tools

**Python PDF Tools** is a Python-based collection of ready-to-use applications designed for various PDF manipulations. Each tool is set up as an independent app that can be triggered by running a batch file located in the root of its folder. This project is under active development, and it currently includes functions such as merging, splitting, compressing, converting, and protecting PDFs, among other essential features.

## Current Status

The project is currently in development, and functionalities are being implemented gradually. Each function is organized into its own folder within the repository, with individual `input`, `output`, and `scripts` folders to allow easy, modular usage of each tool.

## Functions

- ✅ [add-page-numbers-to-pdf](./add-page-numbers-to-pdf): Adds sequential page numbers to all pages in a PDF document.
- ✅ [add-watermark-to-pdf](./add-watermark-to-pdf): Adds custom text or image watermarks to PDF pages.
- ✅ [adjust-pdf-page-size](./adjust-pdf-page-size): Adjusts page size (e.g., A4 to Letter) to ensure PDF content fits the selected page dimensions.
- ✅ [compress-pdf](./compress-pdf): Reduces the file size of PDF documents while maintaining quality.
- ✅ [convert-to-pdf-from-doc](./convert-to-pdf-from-doc): Converts Word documents (DOC or DOCX) to PDF.
- ✅ [convert-to-pdf-from-html](./convert-to-pdf-from-html): Converts HTML files into PDF format, capturing webpage layout.
- ✅ [convert-to-pdf-from-img](./convert-to-pdf-from-img): Converts various image files (JPG, PNG, TIFF, BMP) to single-page PDFs.
- ✅ [convert-to-pdf-from-url](./convert-to-pdf-from-url): Converts the current view of webpages (from URLs) to PDFs for documentation.
- ✅ [extract-images-from-pdf](./extract-images-from-pdf): Extracts embedded images from PDF pages.
- ✅ [extract-tables-from-pdf](./extract-tables-from-pdf): Extracts tables and data structures from PDFs into structured data formats.
- ✅ [extract-text-from-pdf](./extract-text-from-pdf): Extracts raw text from PDF files.
- ✅ [extract-text-from-pdf-ocr](./extract-text-from-pdf-ocr): Uses OCR to extract text from scanned PDFs.
- ✅ [flatten-pdf](./flatten-pdf): Makes PDF annotations or forms non-editable by flattening content layers.
- ✅ [merge-pdf](./merge-pdf): Merges multiple PDF files into a single document.
- ✅ [pdf-decryption](./pdf-decryption): Removes password protection from PDF files (if password is provided).
- ✅ [pdf-encryption](./pdf-encryption): Adds password protection to PDF files.
- ✅ [pdfa-conversion](./pdfa-conversion): Converts PDFs to PDF/A format for long-term archiving.
- ✅ [repair-pdf](./repair-pdf): Attempts to repair damaged or corrupted PDF files; still under testing.
- ✅ [rotate-pdf](./rotate-pdf): Rotates PDF pages to the specified orientation (e.g., 90, 180 degrees).
- ✅ [select-pdf](./select-pdf): Extracts and merges specified pages from individual PDFs into a new document.
- ✅ [split-pdf](./split-pdf): Splits a PDF into multiple documents based on user-defined page ranges.

## Future Functions

- ❌ [convert-from-pdf-to-doc](./convert-from-pdf-to-doc): Converts PDFs to Word format (DOC or DOCX).
- ❌ [convert-from-pdf-to-epub](./convert-from-pdf-to-epub): Converts PDFs to EPUB format for e-readers.
- ❌ [convert-from-pdf-to-img](./convert-from-pdf-to-img): Converts each PDF page into individual image files.
- ❌ [convert-to-pdf-from-excel](./convert-to-pdf-from-excel): Converts Excel files to PDF, preserving layout.
- ❌ [convert-to-pdf-from-ppt](./convert-to-pdf-from-ppt): Converts PowerPoint presentations to PDF.
- ❌ [convert-to-pdf-from-epub](./convert-to-pdf-from-epub): Converts EPUB eBooks to PDF.

## Contributing

Contributors are welcome! If you'd like to contribute, please fork the repository, make your changes, and submit a pull request. Feel free to open issues for feature requests, bugs, or general improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.