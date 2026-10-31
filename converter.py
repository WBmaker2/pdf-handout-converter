import logging
import math
import os
import tempfile

import fitz

logger = logging.getLogger(__name__)

A4_W, A4_H = 595.28, 841.89
GRIDS = {2: (1, 2), 6: (2, 3)}


class ConversionError(Exception):
    pass


def mm_to_pt(mm):
    return mm * 72.0 / 25.4


def _page_path(file):
    if isinstance(file, str):
        return file
    if hasattr(file, "name"):
        return file.name
    if hasattr(file, "path"):
        return file.path
    return str(file)


def convert(
    input_path,
    output_path,
    n_per_page=2,
    margin_mm=10,
    gutter_mm=6,
    border=True,
    show_numbers=True,
    password=None,
):
    input_path = _page_path(input_path)
    if n_per_page not in GRIDS:
        raise ValueError(f"지원하지 않는 모드입니다: {n_per_page} (2 또는 6)")

    src = fitz.open(input_path)
    out = None
    try:
        if src.is_encrypted:
            ok = src.authenticate(password or "")
            if not ok:
                raise ConversionError("암호화된 PDF입니다. 올바른 비밀번호가 필요합니다.")
        if src.page_count == 0:
            raise ConversionError("슬라이드가 없습니다")

        try:
            first = src[0]
            if first.rect.height > first.rect.width:
                logger.warning("입력 PDF가 세로 방향입니다. 비율 유지로 그대로 배치합니다.")
        except Exception:
            pass

        out = fitz.open()
        try:
            cols, rows = GRIDS[n_per_page]
            margin = mm_to_pt(margin_mm)
            gutter = mm_to_pt(gutter_mm)
            usable_w = A4_W - 2 * margin
            usable_h = A4_H - 2 * margin
            cell_w = (usable_w - (cols - 1) * gutter) / cols
            cell_h = (usable_h - (rows - 1) * gutter) / rows

            total = src.page_count
            for i in range(0, total, n_per_page):
                page = out.new_page(width=A4_W, height=A4_H)
                group_indices = range(i, min(i + n_per_page, total))
                for idx, slide_no in enumerate(group_indices):
                    try:
                        slide = src[slide_no]
                        _ = slide.rect
                    except Exception as e:
                        logger.warning(f"페이지 {slide_no + 1} 손상으로 건너뜁니다: {e}")
                        continue

                    r, c = divmod(idx, cols)
                    x0 = margin + c * (cell_w + gutter)
                    y0 = margin + r * (cell_h + gutter)

                    try:
                        scale = min(cell_w / slide.rect.width, cell_h / slide.rect.height)
                    except Exception:
                        scale = 1.0
                    if not (scale > 0):
                        scale = 1.0
                    w = slide.rect.width * scale
                    h = slide.rect.height * scale
                    cx = x0 + (cell_w - w) / 2
                    cy = y0 + (cell_h - h) / 2
                    target = fitz.Rect(cx, cy, cx + w, cy + h)

                    try:
                        page.show_pdf_page(target, src, slide_no)
                    except Exception as e:
                        logger.warning(f"페이지 {slide_no + 1} 삽입 실패, 건너뜁니다: {e}")
                        continue

                    if border:
                        page.draw_rect(target, color=(0, 0, 0), width=0.5)
                    if show_numbers:
                        page.insert_text(
                            (cx, cy + h + 9),
                            f"{slide_no + 1}",
                            fontsize=8,
                            color=(0.35, 0.35, 0.35),
                        )

            if total > 200:
                fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
                os.close(fd)
                try:
                    out.save(tmp_path, garbage=4, deflate=True)
                    out.close()
                    out = None
                    os.replace(tmp_path, output_path)
                finally:
                    if os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            pass
            else:
                out.save(output_path, garbage=4, deflate=True)
        finally:
            if out is not None:
                out.close()
    finally:
        src.close()

    return output_path
