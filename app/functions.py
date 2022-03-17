import textwrap
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def gen_image_macro(image_bytes: bytes | str, top_text: str, bottom_text: str, *, font_path: str) -> BytesIO:
    """Generate an image macro

    Args:
        image_bytes (bytes | str): The image - can be a file path or the image bytes
        top_text (str): The top text
        bottom_text (str): The bottom text
        font_path (str): Path to the font file

    Returns:
        BytesIO: The resulting image macro as bytes
    """

    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    image = Image.open(image_bytes)
    draw = ImageDraw.Draw(image)
    w, h = image.size
    font = ImageFont.truetype(font=font_path, size=h // 10)
    cw, ch = font.getsize("A")
    cpl = w // cw
    top_lines, bottom_lines = (textwrap.wrap(top_text, width=cpl), textwrap.wrap(bottom_text, width=cpl))

    y = 10
    for line in top_lines:
        lw, lh = font.getsize(line)
        x = (w - lw) / 2
        draw.text((x - 1, y), line, font=font, fill="black")
        draw.text((x + 1, y), line, font=font, fill="black")
        draw.text((x, y - 1), line, font=font, fill="black")
        draw.text((x, y + 1), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += lh

    y = h - ch * len(bottom_lines) - 15
    for line in bottom_lines:
        lw, lh = font.getsize(line)
        x = (w - lw) / 2
        draw.text((x - 1, y), line, font=font, fill="black")
        draw.text((x + 1, y), line, font=font, fill="black")
        draw.text((x, y - 1), line, font=font, fill="black")
        draw.text((x, y + 1), line, font=font, fill="black")
        draw.text((x, y), line, fill="white", font=font)
        y += lh

    out = BytesIO()
    image.save(out, format=image.format.lower())
    out.seek(0)
    return out
