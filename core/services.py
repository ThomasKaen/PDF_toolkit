from __future__ import annotations
from pathlib import Path
from typing import Optional
from PyPDF2 import PdfReader, PdfWriter
from .models import (PDFResult, MergeOptions, SplitOptions,
                     EncryptOptions, DecryptOptions, CompressOptions)
from .io_utils import ensure_dir, next_available

class PDFService:
    # --- Helpers --- #
    def _open_reader(self, src: Path, get_password) -> PdfReader:
        reader = PdfReader(str(src))
        if getattr(reader, "is_encrypted", False):
            if not get_password:
                raise ValueError("PDF is encrypted and no password provided")
            pwd = get_password() or ""
            if reader.decrypt(pwd) == 0:
                raise ValueError("Wrong password or decryption failed")
        return reader

    def merge(self, opts: MergeOptions) -> PDFResult:
        if not opts.files:
            return PDFResult(False, "No files selected")
        writer = PdfWriter()
        for f in opts.files:
            r = PdfReader(str(f))
            for page in r.pages:
                writer.add_page(page)
        out = next_available(opts.output_path)
        ensure_dir(out.parent)
        with out.open(mode="wb") as fp:
            writer.write(fp)
        return PDFResult(True, f"Merged {len(opts.files)} files(s).", output=out)

    def split(self, opts: SplitOptions) -> PDFResult:
        reader = self._open_reader(opts.src, opts.get_password)
        pages = len(reader.pages)
        if pages == 0:
            return PDFResult(False, "PDF has 0 pages")
        ensure_dir(opts.out_dir)
        base = opts.src.stem
        written = list[Path] = []
        for i in range(pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            out = next_available(opts.out_dir / f"{base}_page{i+1}.pdf")
            with out.open(mode="wb") as fp:
                writer.write(fp)
            written.append(out)
        return PDFResult(True, f"Split into {len(written)} page(s).", outputs=written)

    def encrypt(self, opts: EncryptOptions) -> PDFResult:
        reader = PdfReader(str(opts.src))
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)
        out = next_available(opts.output_path)
        ensure_dir(out.parent)
        with out.open(mode="wb") as fp:
            writer.write(fp)
        return PDFResult(True, f"Encrypted.", output=out)

    def decrypt(self, opts: DecryptOptions) -> PDFResult:
        reader = PdfReader(str(opts.src))
        if getattr(reader, "is_encrypted", False):
            if reader.decrypt(opts.password) == 0:
                return PDFResult(False, "Wrong password")
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)
        out = next_available(opts.output_path)
        ensure_dir(out.parent)
        with out.open(mode="wb") as fp:
            writer.write(fp)
        return PDFResult(True, f"Password removed", output=out)

    def compress(self, opts: CompressOptions) -> PDFResult:
        # Placeholder until Ghostscript is added
        return PDFResult(False, "Compression not added yet.")

