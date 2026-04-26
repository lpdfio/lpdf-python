"""
Shared snapshot-test helpers for the Python adapter.
Centralises path constants, SHA-256 hashing, and compare-or-update logic so
that test_snapshot.py only contains test setup and engine invocations.
"""

import hashlib
import os
from pathlib import Path

# Walk up from this file: tests/ → python/ → adapters/ → src/ → workspace root
# Accept a directory that has Cargo.toml (native) OR test/snapshots (Docker).
# Fall back to the adapter repo root (two levels up) so that the module never
# crashes when running from a standalone repo checkout without the monorepo.
_here = Path(__file__).resolve()
ROOT  = next(
    (p for p in _here.parents
     if (p / "Cargo.toml").exists() or (p / "test" / "snapshots").is_dir()),
    _here.parent.parent,   # fallback: adapter repo root (tests/../..)
)
FIXTURES  = ROOT / "test" / "fixtures"
SNAPSHOTS = ROOT / "test" / "snapshots"

HAS_FIXTURES = FIXTURES.is_dir() and any(FIXTURES.glob("*.xml"))

EXAMPLES = [
    *[f"example{i}" for i in range(1, 12)],
    "showcase-cluster", "showcase-flank", "showcase-frame",
    "showcase-grid", "showcase-split", "showcase-stack",
    "showcase-table", "showcase-barcode", "showcase-encryption", "showcase-forms",
    "bench_xs", "bench_s", "bench_m", "bench_l", "bench_xl",
]


def compare_or_update(name: str, pdf_bytes: bytes) -> None:
    """Compare the SHA-256 hash of *pdf_bytes* against the stored snapshot for
    *name*, or write a new snapshot when ``UPDATE_SNAPSHOTS=1``."""
    sha  = hashlib.sha256(pdf_bytes).hexdigest()
    snap = SNAPSHOTS / f"{name}.pdf.sha256"

    if os.environ.get("UPDATE_SNAPSHOTS") == "1":
        snap.write_text(sha)
    else:
        stored = snap.read_text().strip()
        assert sha == stored, (
            f"Snapshot mismatch for {name}. "
            f"Run with UPDATE_SNAPSHOTS=1 to accept.\n"
            f"  expected: {stored}\n  received: {sha}"
        )
