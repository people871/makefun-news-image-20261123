#!/usr/bin/env python3
"""Entry program for news-image-20261123.

Copies the bundled newspaper front page (entry.png, JPEG bytes) to
$MAKEFUN_OUTPUT_DIR/entry.png after verifying it is a whole, in-limits
image, then re-reads the copy and refuses to exit cleanly unless its byte
length and sha256 match the source exactly.

Standard library only. Deterministic: the same input bytes always produce
the same output bytes, so two runs write identical files.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "entry.png"
MAX_BYTES = 1_048_576            # 1 MiB gate limit
EXPECT_WIDTH = 1024
EXPECT_HEIGHT = 1024

JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"entry: error: {message}", file=sys.stderr)
    return 1


def jpeg_frame(data):
    """Walk JPEG marker segments; return (width, height) of the frame.

    Requires the frame header plus the tables a decoder needs, and an end
    marker as the final two bytes, so a truncated file cannot pass.
    """
    if len(data) < 4 or data[:2] != JPEG_SOI:
        return None
    if data[-2:] != JPEG_EOI:
        return None
    pos = 2
    seen_dqt = False
    seen_dht = False
    seen_sos = False
    frame = None
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        # Standalone markers carry no length field.
        if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xD9:  # EOI
            break
        if pos + 4 > len(data):
            return None
        seg_len = int.from_bytes(data[pos + 2:pos + 4], "big")
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            return None
        if marker == 0xDB:
            seen_dqt = True
        elif marker == 0xC4:
            seen_dht = True
        elif marker == 0xDA:
            seen_sos = True
            break  # entropy data follows; the header checks are done
        elif marker in (0xC0, 0xC1, 0xC2):
            # SOF: precision (1), height (2), width (2), components (1).
            if seg_len < 7:
                return None
            precision = data[pos + 4]
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            ncomp = data[pos + 9]
            if precision != 8 or ncomp not in (1, 3, 4):
                return None
            frame = (width, height)
        pos += 2 + seg_len
    if frame is None or not (seen_dqt and seen_dht and seen_sos):
        return None
    return frame


def png_frame(data):
    """Read a PNG header; return (width, height) or None.

    Also requires the IEND trailer as the final chunk, so a PNG cut short
    mid-stream is rejected instead of passing on its header alone.
    """
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        return None
    # First chunk must be IHDR: length 13, type IHDR, then width/height.
    if data[8:12] != (13).to_bytes(4, "big") or data[12:16] != b"IHDR":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    depth = data[24]
    colour = data[25]
    if depth not in (1, 2, 4, 8, 16) or colour not in (0, 2, 3, 4, 6):
        return None
    # IEND chunk: length 0, type IEND, CRC 0xAE426082, as the last 12 bytes.
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return None
    return (width, height)


def verify(data):
    """Return (kind, width, height) if data is a whole in-limits image."""
    if not data or len(data) > MAX_BYTES:
        return None
    if data[:2] == JPEG_SOI:
        frame = jpeg_frame(data)
        return ("JPEG", frame[0], frame[1]) if frame else None
    if data[:8] == PNG_MAGIC:
        frame = png_frame(data)
        return ("PNG", frame[0], frame[1]) if frame else None
    return None


def main():
    src_path = os.path.join(HERE, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    try:
        with open(src_path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail(f"cannot read {SOURCE_NAME}: {exc}")

    checked = verify(data)
    if checked is None:
        return fail(f"{SOURCE_NAME} is not a whole image within the limits")
    kind, width, height = checked
    if (width, height) != (EXPECT_WIDTH, EXPECT_HEIGHT):
        return fail(
            f"{SOURCE_NAME} is {width}x{height}, expected "
            f"{EXPECT_WIDTH}x{EXPECT_HEIGHT}"
        )

    digest = hashlib.sha256(data).hexdigest()
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, SOURCE_NAME)
        with open(out_path, "wb") as fh:
            fh.write(data)
        with open(out_path, "rb") as fh:
            written = fh.read()
    except OSError as exc:
        return fail(f"cannot write output: {exc}")

    if len(written) != len(data):
        return fail(
            f"output length {len(written)} != source length {len(data)}"
        )
    if hashlib.sha256(written).hexdigest() != digest:
        return fail("output sha256 does not match the source")
    print(
        f"entry: wrote {out_path}: {kind} {width}x{height}, "
        f"{len(data)} bytes, sha256 {digest}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
