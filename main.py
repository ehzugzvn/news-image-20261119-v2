#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the grader's output directory.

Standard library only, no rendering at runtime: the front page was
rendered at build time by render.py and is stored in this repository
as entry.png, next to this file. At grading time this program simply
copies that file to MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)


if __name__ == "__main__":
    main()
