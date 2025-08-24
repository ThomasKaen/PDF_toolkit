from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable, Sequence

# Simple result object
@dataclass
class PDFResult:
    ok: bool
    message: str
    output: Optional[Path] = None
    outputs: Optional[list[Path]] = None

# Options for each operation
@dataclass(frozen=True)
class MergeOptions:
    files: Sequence[Path]
    output_path: Path

@dataclass(frozen=True)
class SplitOptions:
    src: Path
    out_dir: Path
    # callback to get password if encrypted (core stay GUI-agnostic)
    get_password: Optional[Callable[[], Optional[str]]] = None

@dataclass(frozen=True)
class EncryptOptions:
    src: Path
    output_path: Path
    password: str

@dataclass(frozen=True)
class DecryptOptions:
    src: Path
    output_path: Path
    password: str

# Optional placeholder (for when Ghostscript implemented)
@dataclass(frozen=True)
class CompressOptions:
    src: Path
    out_path: Path
    method: str = "ghostscript"
    quality: str = "screen"