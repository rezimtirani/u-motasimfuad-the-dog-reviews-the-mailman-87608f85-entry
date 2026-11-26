"""The Dog Reviews the Mailman — a one-line make.fun entry.

A dog leaves a one-star review for the mailman: he turns up every day,
never knocks, and shoves paper through the door, yet somehow expects
the dog to stay calm about it. Only the Python standard library is used.
"""

import os
import sys

REVIEW_LINE = "One star. He shows up every single day, never knocks, shoves paper through my door, and somehow still expects me to be calm about it."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def check_review(text):
    """Return the review once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes, so the line must be a
    single line of 1 to 200 characters, not only whitespace, with no
    trailing newline and no control characters in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("review must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"review must be 1 to {MAX_CHARS} characters, got {len(text)}"
        )
    if text.strip() == "":
        raise ValueError("review must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("review must not contain control characters")
    return text


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII line reads
    the same either way while a line with wide characters would not.
    Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    words = len(text.split())
    return f"{chars} characters, {byte_count} UTF-8 bytes, {words} words"


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = check_review(REVIEW_LINE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {path} ({describe_line(line)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
