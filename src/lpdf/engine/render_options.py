from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderOptions:
    """Per-call options for PdfEngine.render().

    ``user_password``, ``owner_password`` and ``skip_encryption`` are for a document that asks for encryption in its
    ``output``. ``user_password`` is the password a reader asks for before showing the PDF; leave it out, or pass
    ``""``, for a PDF anyone can open, which only the ``allow`` of the ``output`` restricts. ``owner_password`` opens
    the PDF with every permission: a document that asks for encryption renders only with it, or with
    ``skip_encryption``, and a document that doesn't ask for encryption refuses it, so a file never goes out
    unencrypted while you believe it is locked. ``skip_encryption`` renders a document that asks for encryption
    unencrypted, for a render that cannot have the passwords, such as a preview; not together with the passwords.
    """
    created_on: str | None = None
    data: dict | None = None
    user_password: str | None = None
    owner_password: str | None = None
    skip_encryption: bool = False