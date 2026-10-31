import math
import os
import tempfile

import fitz
import pytest

from converter import convert, ConversionError, A4_W, A4_H


def _make_sample(path, n):
    doc = fitz.open()
    for i in range(n):
        page = doc.new_page(width=1280, height=720)
        page.draw_rect(page.rect, color=(0.2, 0.4, 0.8), fill=(0.2, 0.4, 0.8))
        page.insert_text((80, 120), f"Slide {i + 1}", fontsize=48, color=(1, 1, 1))
    doc.save(path, garbage=4, deflate=True)
    doc.close()


@pytest.fixture
def sample_7(tmp_path):
    p = tmp_path / "sample_7.pdf"
    _make_sample(str(p), 7)
    return str(p)


def _expected_pages(n, per):
    return math.ceil(n / per)


def test_page_count_2mode(sample_7):
    out = tempfile.mktemp(suffix=".pdf")
    try:
        convert(sample_7, out, n_per_page=2)
        doc = fitz.open(out)
        assert doc.page_count == _expected_pages(7, 2)
        doc.close()
    finally:
        if os.path.exists(out):
            os.remove(out)


def test_page_count_6mode(sample_7):
    out = tempfile.mktemp(suffix=".pdf")
    try:
        convert(sample_7, out, n_per_page=6)
        doc = fitz.open(out)
        assert doc.page_count == _expected_pages(7, 6)
        doc.close()
    finally:
        if os.path.exists(out):
            os.remove(out)


def test_a4_size(sample_7):
    out = tempfile.mktemp(suffix=".pdf")
    try:
        convert(sample_7, out, n_per_page=6)
        doc = fitz.open(out)
        p = doc[0]
        assert abs(p.rect.width - A4_W) < 0.5
        assert abs(p.rect.height - A4_H) < 0.5
        doc.close()
    finally:
        if os.path.exists(out):
            os.remove(out)


def _write_empty_pdf(path):
    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n",
    ]
    body = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(body))
        body += obj
    xref_pos = len(body)
    body += b"xref\n0 3\n"
    body += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        body += f"{off:010d} 00000 n \n".encode()
    body += b"trailer\n<< /Size 3 /Root 1 0 R >>\n"
    body += f"startxref\n{xref_pos}\n%%EOF\n".encode()
    with open(path, "wb") as f:
        f.write(body)


def test_empty_pdf():
    empty = tempfile.mktemp(suffix=".pdf")
    _write_empty_pdf(empty)
    out = tempfile.mktemp(suffix=".pdf")
    try:
        with pytest.raises(ConversionError):
            convert(empty, out)
    finally:
        for f in (empty, out):
            if os.path.exists(f):
                os.remove(f)


def test_one_slide():
    one = tempfile.mktemp(suffix=".pdf")
    doc = fitz.open()
    doc.new_page(width=842, height=595)
    doc.save(one)
    doc.close()
    out = tempfile.mktemp(suffix=".pdf")
    try:
        convert(one, out, n_per_page=2)
        d = fitz.open(out)
        assert d.page_count == 1
        d.close()
        convert(one, out, n_per_page=6)
        d = fitz.open(out)
        assert d.page_count == 1
        d.close()
    finally:
        for f in (one, out):
            if os.path.exists(f):
                os.remove(f)


def test_options_toggle(sample_7):
    out1 = tempfile.mktemp(suffix=".pdf")
    out2 = tempfile.mktemp(suffix=".pdf")
    try:
        convert(sample_7, out1, n_per_page=2, border=True, show_numbers=True)
        convert(sample_7, out2, n_per_page=2, border=False, show_numbers=False)
        # just ensure both created and valid
        for p in (out1, out2):
            d = fitz.open(p)
            assert d.page_count == 4
            d.close()
    finally:
        for f in (out1, out2):
            if os.path.exists(f):
                os.remove(f)
