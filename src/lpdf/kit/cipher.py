# Generated from lpdf.xsd by scripts/gen-sdk-api.mjs.
# Do not edit: change the schema and run `make gen-sdk-api`.
from enum import StrEnum


class Cipher(StrEnum):
    """The values of the `encrypt` attribute of the output: the cipher the PDF is encrypted with."""

    AES_256 = "aes-256"
    RC4_128 = "rc4-128"
