import os
import tempfile
import uuid
import zipfile

import gradio as gr

from converter import convert


def _path(file):
    if isinstance(file, str):
        return file
    if hasattr(file, "name"):
        return file.name
    if hasattr(file, "path"):
        return file.path
    return str(file)


def _safe_name(path):
    base = os.path.splitext(os.path.basename(path))[0] or "handout"
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in base)


def run(files, mode, border, numbers, fmt):
    if files is None:
        raise gr.Error("PDF 파일을 업로드해주세요.")
    if not isinstance(files, (list, tuple)):
        files = [files]
    files = [f for f in files if f is not None]
    if not files:
        raise gr.Error("PDF 파일을 업로드해주세요.")

    mode_str = str(mode)
    if mode_str.startswith("2"):
        n = 2
    elif mode_str.startswith("6"):
        n = 6
    elif mode_str.startswith("8"):
        n = 8
    else:
        n = 6
    out_dir = os.path.join(tempfile.gettempdir(), f"handout_{uuid.uuid4().hex}")
    os.makedirs(out_dir, exist_ok=True)

    outputs = []
    for f in files:
        src = _path(f)
        name = _safe_name(src)
        out = os.path.join(out_dir, f"{name}_handout.pdf")
        i = 1
        while os.path.exists(out):
            out = os.path.join(out_dir, f"{name}_handout_{i}.pdf")
            i += 1
        convert(src, out, n_per_page=n, border=border, show_numbers=numbers)
        outputs.append(out)

    if str(fmt).startswith("ZIP") or str(fmt).lower() == "zip":
        zip_path = os.path.join(out_dir, "handout.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in outputs:
                zf.write(p, os.path.basename(p))
        return zip_path

    return outputs


CUSTOM_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,600;0,6..96,700;1,6..96,400&family=Manrope:wght@300;400;500;600;700&display=swap');

:root {
  --spot: #C9352B;
  --ink: #0E0E0E;
  --paper: #F7F4EE;
  --paper-2: #EFEAE0;
  --rule: #0E0E0E;
  --muted: #5A5650;
  --line: rgba(14,14,14,0.14);
}

.gradio-container {
  background: var(--paper) !important;
  color: var(--ink) !important;
  font-family: 'Manrope', system-ui, sans-serif !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
}

/* Masthead */
.masthead {
  padding: 48px 0 24px;
  border-bottom: 3px solid var(--ink);
  margin-bottom: 40px;
}
.masthead__title {
  font-family: 'Bodoni Moda', 'Times New Roman', serif;
  font-size: clamp(2.6rem, 6vw, 4.6rem);
  line-height: 0.95;
  letter-spacing: -0.02em;
  font-weight: 600;
  margin: 0 0 16px;
  color: var(--ink);
}
.masthead__title em {
  font-style: italic;
  color: var(--spot);
}
.masthead__lede {
  max-width: 46ch;
  font-size: 1rem;
  line-height: 1.55;
  color: var(--muted);
  margin: 0;
}
.rule { border: none; border-top: 1px solid var(--rule); margin: 24px 0; }
.rule--heavy { border-top-width: 3px; }

/* Section headings with drop cap */
.section-title {
  font-family: 'Bodoni Moda', serif;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--ink);
  display: flex;
  align-items: baseline;
  gap: 2px;
}
.dropcap {
  font-size: 2.6rem;
  line-height: 0.85;
  color: var(--spot);
  margin-right: 4px;
  font-weight: 700;
}

/* Form controls */
.gradio-container .block,
.gradio-container .form {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.gradio-container input[type="text"],
.gradio-container textarea,
.gradio-container select {
  background: var(--paper-2) !important;
  border: 1px solid var(--ink) !important;
  border-radius: 0 !important;
  color: var(--ink) !important;
}
.gradio-container .wrap .item,
.gradio-container label {
  font-family: 'Manrope', sans-serif !important;
}

/* Radio / checkbox rows */
.gradio-container .gr-radio label,
.gradio-container .gr-checkbox label {
  border: 1px solid var(--line) !important;
  padding: 10px 14px !important;
  border-radius: 0 !important;
  transition: border-color 180ms ease, background 180ms ease;
}
.gradio-container .gr-radio label:hover,
.gradio-container .gr-checkbox label:hover {
  border-color: var(--ink) !important;
}
.gradio-container .gr-radio input:checked + span,
.gradio-container .gr-checkbox input:checked + span {
  color: var(--spot) !important;
}

/* File upload dropzone */
.gradio-container .upload-container,
.gradio-container [data-testid="file-upload"] {
  border: 2px dashed var(--ink) !important;
  border-radius: 0 !important;
  background: var(--paper-2) !important;
  min-height: 140px;
  transition: border-color 180ms ease, background 180ms ease;
}
.gradio-container .upload-container:hover {
  border-color: var(--spot) !important;
  background: var(--paper) !important;
}

/* Primary button */
.gradio-container button.primary,
.gradio-container .gr-button-primary {
  background: var(--ink) !important;
  color: var(--paper) !important;
  border: 2px solid var(--ink) !important;
  border-radius: 0 !important;
  font-family: 'Manrope', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  padding: 14px 28px !important;
  transition: background 180ms ease, color 180ms ease, transform 180ms ease;
}
.gradio-container button.primary:hover,
.gradio-container .gr-button-primary:hover {
  background: var(--spot) !important;
  border-color: var(--spot) !important;
  transform: translateY(-1px);
}

/* Note */
.note {
  color: var(--muted);
  font-size: 0.85rem;
  line-height: 1.5;
  margin-top: 12px;
  max-width: 40ch;
}

/* Output file */
.gradio-container .gr-file-output {
  border: 1px solid var(--ink) !important;
  border-radius: 0 !important;
  background: var(--paper-2) !important;
}

/* Footer with hidden mark */
.footer {
  margin-top: 64px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--muted);
  font-size: 0.85rem;
}
.footer__mark {
  width: 28px;
  height: 28px;
  opacity: 0.35;
  transition: opacity 240ms ease;
}
.footer:hover .footer__mark { opacity: 1; }

/* Focus */
.gradio-container *:focus-visible {
  outline: 2px solid var(--spot) !important;
  outline-offset: 2px !important;
}

/* Responsive */
@media (max-width: 768px) {
  .masthead { padding: 32px 0 16px; }
  .masthead__title { font-size: 2.6rem; }
}
"""

theme = gr.themes.Base(
    primary_hue="red",
    secondary_hue="stone",
    neutral_hue="stone",
    font=[gr.themes.GoogleFont("Manrope"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=["ui-monospace", "monospace"],
).set(
    body_background_fill="#F7F4EE",
    body_text_color="#0E0E0E",
    block_background_fill="transparent",
    block_border_width="0px",
    button_primary_background_fill="#0E0E0E",
    button_primary_text_color="#F7F4EE",
    input_background_fill="#EFEAE0",
    input_border_color="#0E0E0E",
)


with gr.Blocks(title="PDF Handout Converter") as demo:
    gr.HTML(
        """
        <header class="masthead">
          <h1 class="masthead__title">PDF Handout<br/><em>Converter</em></h1>
          <p class="masthead__lede">
            가로 프레젠테이션 PDF를 A4 세로 유인물로 변환합니다.
            벡터 그대로 보존되어 화질 손실이 없고, 여러 파일을 한 번에 처리할 수 있습니다.
          </p>
          <hr class="rule rule--heavy"/>
        </header>
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<h2 class="section-title"><span class="dropcap">U</span>pload &amp; options</h2>')
            file_in = gr.File(
                label="가로 프레젠테이션 PDF (여러 개 선택 가능)",
                file_count="multiple",
                file_types=[".pdf"],
            )
            mode = gr.Radio(
                ["2장 (위/아래)", "6장 (2×3)", "8장 (2×4)"],
                value="8장 (2×4)",
                label="배치",
            )
            with gr.Row():
                border = gr.Checkbox(True, label="슬라이드 테두리")
                numbers = gr.Checkbox(True, label="원본 페이지 번호 표시")
            fmt = gr.Radio(
                ["개별 파일", "ZIP 압축"],
                value="개별 파일",
                label="다운로드 방식",
            )
            btn = gr.Button("변환하기", variant="primary")

        with gr.Column(scale=1):
            gr.HTML('<h2 class="section-title"><span class="dropcap">O</span>utput</h2>')
            out = gr.File(label="변환된 PDF", file_count="multiple")
            gr.HTML(
                '<p class="note">변환을 실행하면 결과 파일이 이곳에 표시됩니다. '
                'ZIP 압축을 선택하면 단일 압축 파일로 받을 수 있습니다.</p>'
            )

    gr.HTML(
        """
        <footer class="footer">
          <span>로컬에서 실행 · 인터넷 연결 불필요 · 벡터 보존 변환</span>
          <svg class="footer__mark" viewBox="0 0 28 28" aria-hidden="true">
            <circle cx="14" cy="14" r="10" fill="none" stroke="#0E0E0E" stroke-width="1.5"/>
            <path d="M9 14 L13 18 L19 10" fill="none" stroke="#C9352B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </footer>
        """
    )

    btn.click(run, inputs=[file_in, mode, border, numbers, fmt], outputs=out)


if __name__ == "__main__":
    demo.launch(css=CUSTOM_CSS, theme=theme)
