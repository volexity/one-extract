"""This is a temporary inclusion in this project to address an unknown issue when using msoffcrypto.

https://github.com/volexity/threat-intel/issues/7

Much of the code in this file was borrowed from:

https://github.com/nolze/msoffcrypto-tool/blob/master/msoffcrypto/method/ecma376_agile.py

Changes are highlighted using "#!NOTE".
"""

# builtins
import functools
import logging
from hashlib import sha1, sha256, sha384, sha512
from io import BytesIO
from struct import pack, unpack
from typing import Callable

# installables
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ALGORITHM_HASH = {
    "SHA1": sha1,
    "SHA256": sha256,
    "SHA384": sha384,
    "SHA512": sha512,
}

logger = logging.getLogger(__name__)


def _get_hash_func(algorithm: str) -> Callable:
    return ALGORITHM_HASH.get(algorithm, sha1)


def decrypt(key: bytes, key_data_salt: bytes, hash_algorithm: str, ibuf: BytesIO) -> bytes:
    r"""Return decrypted data.

    >>> key = b'@ f\t\xd9\xfa\xad\xf2K\x07j\xeb\xf2\xc45\xb7B\x92\xc8\xb8\xa7\xaa\x81\xbcg\x9b\xe8\x97\x11\xb0*\xc2'
    >>> keyDataSalt = b'\x8f\xc7x"+P\x8d\xdcL\xe6\x8c\xdd\x15<\x16\xb4'
    >>> hashAlgorithm = 'SHA512'
    """
    hash_calc = _get_hash_func(hash_algorithm)

    obuf = BytesIO()
    total_size = unpack("<I", ibuf.read(4))[0]
    logger.debug("totalSize: %s", total_size)
    remaining = total_size
    ibuf.seek(8)
    # !NOTE - the key change made is that instead of iterating over 4KB segments,
    # we read the data in a single buffer, this resolves the issue outlined
    # in the docstrings of this file.
    for i, buf in enumerate(iter(functools.partial(ibuf.read, total_size), b"")):
        salt_with_block_key = key_data_salt + pack("<I", i)
        iv = hash_calc(salt_with_block_key).digest()
        iv = iv[:16]
        aes = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = aes.decryptor()
        dec = decryptor.update(buf) + decryptor.finalize()
        if remaining < len(buf):
            dec = dec[:remaining]
        obuf.write(dec)
        remaining -= len(buf)
    return obuf.getvalue()
