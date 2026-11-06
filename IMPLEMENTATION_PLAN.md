# PDF 가로 프레젠테이션 → A4 유인물 변환기 구현 계획

## 1. 프로젝트 개요

- **이름**: pdf-handout-converter
- **목적**: 가로(landscape) 프레젠테이션 PDF를 입력받아, A4 세로(portrait) 유인물 형식 PDF로 변환
- **옵션**:
  - 2장 모드: 1페이지에 슬라이드 2개 (위/아래 반씩)
  - 6장 모드: 1페이지에 슬라이드 6개 (2열 × 3행, 순서대로)
  - 8장 모드: 1페이지에 슬라이드 8개 (2열 × 4행, 순서대로)
- **부가 옵션**: 슬라이드 사이/페이지 가장자리 여백, 슬라이드 테두리, 원본 페이지 번호 표시
- **마지막 페이지**: 남은 슬라이드만 배치(빈 칸 비움)

## 2. 타당성 판단: 구현 가능 ✅

- 가로 PDF의 각 페이지(슬라이드)를 새 A4 페이지의 지정된 사각형 영역에 삽입하는 작업은 **N-up 레이아웃**으로, 벡터 보존 방식으로 구현 가능.
- **PyMuPDF(fitz)**의 `Page.show_pdf_page(target_rect, src_doc, page_index)`가 슬라이드를 대상 사각형에 자동 스케일/배치하며, 벡터 그래픽·텍스트를 그대로 유지(래스터화 없음) → 화질 손실 없음, 파일 크기 작음.
- 대안으로 이미 설치된 `pypdf`의 `merge_transformed_page` + `Transformation`으로도 구현 가능하나, PyMuPDF가 더 안정적.

## 3. 기술 스택

| 항목 | 선택 | 비고 |
|---|---|---|
| 언어 | Python 3.11+ | |
| PDF 처리 | PyMuPDF (fitz) | pip install pymupdf |
| 웹 UI | Gradio | pip install gradio |
| 출력 규격 | A4 portrait (595.28 × 841.89 pt) | |
| 입력 가정 | 가로 orientation 슬라이드 | 세로 입력도 비율 유지로 처리 |

## 4. 파일 구조

```
pdf-handout-converter/
├── requirements.txt
├── converter.py          # 핵심 변환 로직 (CLI에서도 재사용)
├── app.py                # Gradio 웹 UI
├── tests/
│   └── test_converter.py # 단위/통합 테스트
└── samples/              # 테스트용 샘플 PDF (gitignore 권장)
```

## 5. 핵심 알고리즘 (converter.py)

```python
import fitz  # PyMuPDF

A4_W, A4_H = fitz.paper_size("a4")  # 595.28, 841.89

GRIDS = {2: (1, 2), 6: (2, 3), 8: (2, 4)}  # (cols, rows)

def convert(input_path, output_path, n_per_page=2,
            margin_mm=10, gutter_mm=6,
            border=True, show_numbers=True):
    src = fitz.open(input_path)
    out = fitz.open()
    cols, rows = GRIDS[n_per_page]

    margin = mm_to_pt(margin_mm)
    gutter = mm_to_pt(gutter_mm)
    usable_w = A4_W - 2 * margin
    usable_h = A4_H - 2 * margin
    cell_w = (usable_w - (cols - 1) * gutter) / cols
    cell_h = (usable_h - (rows - 1) * gutter) / rows

    slides = list(src)
    for i in range(0, len(slides), n_per_page):
        group = slides[i:i + n_per_page]
        page = out.new_page(width=A4_W, height=A4_H)
        for idx, slide in enumerate(group):
            r, c = divmod(idx, cols)
            x0 = margin + c * (cell_w + gutter)
            y0 = margin + r * (cell_h + gutter)

            # 비율 유지 스케일 + 중앙 정렬
            scale = min(cell_w / slide.rect.width,
                        cell_h / slide.rect.height)
            w, h = slide.rect.width * scale, slide.rect.height * scale
            cx = x0 + (cell_w - w) / 2
            cy = y0 + (cell_h - h) / 2
            target = fitz.Rect(cx, cy, cx + w, cy + h)

            page.show_pdf_page(target, src, slide.number)
            if border:
                page.draw_rect(target, color=(0, 0, 0), width=0.5)
            if show_numbers:
                page.insert_text(
                    (cx, cy + h + 9),
                    f"{slide.number + 1}",
                    fontsize=8, color=(0.35, 0.35, 0.35),
                )

    out.save(output_path, garbage=4, deflate=True)
    src.close(); out.close()
```

**설계 포인트**
- 좌표계: PyMuPDF는 좌상단 원점, y 아래 방향 → 행 인덱스 r이 아래로 증가 (자연스러움)
- `show_pdf_page`는 소스 페이지의 MediaBox를 기준으로 스케일 → 회전된 슬라이드도 안전
- 마지막 그룹은 `group` 길이가 n보다 짧아 자동으로 빈 칸 비움

## 6. 웹 UI (app.py, Gradio)

```python
import gradio as gr, tempfile, os
from converter import convert

def run(file, mode, border, numbers):
    n = 2 if mode.startswith("2") else 6
    out = os.path.join(tempfile.gettempdir(), "handout.pdf")
    convert(file.name, out, n_per_page=n, border=border, show_numbers=numbers)
    return out

gr.Interface(
    fn=run,
    inputs=[
        gr.File(label="가로 프레젠테이션 PDF"),
        gr.Radio(["2장 (위/아래)", "6장 (2×3)"], value="2장 (위/아래)", label="배치"),
        gr.Checkbox(True, label="슬라이드 테두리"),
        gr.Checkbox(True, label="원본 페이지 번호 표시"),
    ],
    outputs=gr.File(label="A4 유인물 PDF"),
    title="PDF Handout Converter",
).launch()
```

## 7. 의존성 (requirements.txt)

```
pymupdf>=1.24
gradio>=4.0
```

## 8. 설치 및 실행

```bash
cd pdf-handout-converter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py            # 웹 UI: http://127.0.0.1:7860
# 또는 CLI
python -c "from converter import convert; convert('in.pdf','out.pdf',n_per_page=6)"
```

## 9. 엣지 케이스 처리

| 상황 | 처리 |
|---|---|
| 빈 PDF | "슬라이드가 없습니다" 오류 반환 |
| 1장만 있는 경우 | 2/6 모드 모두 1페이지에 1슬라이드만 배치 |
| 암호화된 PDF | `src.authenticate(pw)` 시도, 실패 시 안내 메시지 |
| 세로 입력 | 경고 로그 후 비율 유지로 그대로 배치(왜곡 없음) |
| 대용량(>200p) | 페이지 단위 스트리밍 저장, 임시파일 정리 |
| 손상된 페이지 | 해당 페이지 건너뛰고 경고, 나머지 계속 처리 |

## 10. 검증 계획

1. 샘플 생성: 16:9 랜덤 색 슬라이드 2/7/13장을 가진 PDF 3종
2. 2장·6장 모드 각각 실행 → 출력 페이지 수 = `ceil(N/n)`
3. 검증 항목:
   - 출력 페이지 크기가 A4 세로인지
   - 슬라이드 순서가 원본 순서와 일치하는지
   - 테두리/번호 옵션 on/off 동작
   - 마지막 페이지 빈 칸 비움 확인
4. 시각 확인: PyMuPDF로 렌더링 후 스크린샷 비교(선택)

## 11. 향후 확장 (선택)

- 슬라이드 재정렬/삭제 UI
- 사용자 지정 여백·거터 슬라이더
- 워터마크/머리말·꼬리말
- Docker 이미지로 배포
- 브라우저 only 변환(JS, pdf-lib) 버전

## 12. 작업 순서 (To-Do)

- [ ] 프로젝트 폴더 초기화 + requirements.txt
- [ ] converter.py 구현 (convert 함수 + 보조 유틸)
- [ ] 엣지 케이스(암호화, 빈 PDF, 세로 입력) 처리
- [ ] app.py Gradio UI 구현
- [ ] 샘플 PDF 생성 스크립트 작성
- [ ] 수동 검증 (2/7/13장 × 2/6 모드)
- [ ] README.md 작성 (사용법, 스크린샷)
- [ ] (선택) Dockerfile + 배포
```

저장 위치: `/Volumes/ External Drive 256G/Dev2/opencode/pdf-handout-converter/IMPLEMENTATION_PLAN.md`