from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EncryptPermissions:
    """Permission flags for PDF encryption.

    All flags default to True (allowed). Set a flag to False to restrict.
    """
    print: bool = True
    modify: bool = True
    copy: bool = True
    annotate: bool = True
    fill_forms: bool = True
    accessibility: bool = True
    assemble: bool = True
    print_hq: bool = True

    def to_dict(self) -> dict[str, bool]:
        from dataclasses import fields
        return {f.name: getattr(self, f.name) for f in fields(self)}


@dataclass(frozen=True)
class EncryptOptions:
    """Encryption configuration for LpdfEngine.set_encryption().

    ``algorithm`` is ``"aes-256"`` (the default) or ``"rc4-128"``, which PDF 2.0 deprecates.
    """
    user_password: str = ""
    owner_password: str = ""
    permissions: EncryptPermissions | None = None
    algorithm: str = "aes-256"
