#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh 10 ma QR cho 10 ban - moi ma dan tram menu.html?table=N"""
import os
import qrcode

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_BASE_URL = "https://nguyenvietnga22121976.github.io/lao-homely-website/"
NUM_TABLES = 10
# LUU Y: theo yeu cau cua anh, KHONG chay lai script nay de giu nguyen 10 ma QR
# hien tai (van con tro ve URL cu co "-cuongtv"). Chi chay khi anh muon in QR moi.

out_dir = os.path.join(ROOT, "images", "qr")
os.makedirs(out_dir, exist_ok=True)

for n in range(1, NUM_TABLES + 1):
    url = f"{SITE_BASE_URL}menu.html?table={n}"
    img = qrcode.make(url, box_size=12, border=2)
    path = os.path.join(out_dir, f"ban-{n}.png")
    img.save(path)
    print(f"Table {n}: {url} -> {path}")

print("Done generating QR codes.")
