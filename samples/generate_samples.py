import os
import random
import fitz

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_sample(n_slides, filename):
    doc = fitz.open()
    for i in range(n_slides):
        page = doc.new_page(width=1280, height=720)
        color = (random.random(), random.random(), random.random())
        page.draw_rect(page.rect, color=color, fill=color)
        page.insert_text((80, 120), f"Slide {i + 1}", fontsize=48, color=(1, 1, 1))
        page.insert_text((80, 200), "Sample presentation", fontsize=24, color=(1, 1, 1))
    path = os.path.join(OUT_DIR, filename)
    doc.save(path, garbage=4, deflate=True)
    doc.close()
    print("created", path)


if __name__ == "__main__":
    random.seed(42)
    for n, name in [(2, "sample_2.pdf"), (7, "sample_7.pdf"), (13, "sample_13.pdf")]:
        make_sample(n, name)
