# PDF Handout Converter

가로(landscape) 프레젠테이션 PDF를 A4 세로(portrait) 유인물 형식 PDF로 변환합니다.

## 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 실행

웹 UI:

```bash
python app.py
# http://127.0.0.1:7860
```

CLI:

```python
from converter import convert
convert("in.pdf", "out.pdf", n_per_page=6)
```

## 옵션

- `n_per_page`: 2 또는 6
- `margin_mm`, `gutter_mm`: 여백/간격(mm)
- `border`: 슬라이드 테두리
- `show_numbers`: 원본 페이지 번호 표시

## 테스트

```bash
python -m pytest
```

## 샘플 생성

```bash
python samples/generate_samples.py
```
