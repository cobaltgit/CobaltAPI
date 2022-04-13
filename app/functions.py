import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from platform import architecture
from os import environ

def create_webdriver() -> webdriver.Firefox:
    """Create a Selenium GeckoDriver instance"""
    environ["MOZ_HEADLESS"] = "1"
    options = webdriver.FirefoxOptions()
    if architecture() != "aarch64":
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    else:
        return webdriver.Firefox(executable_path="app/files/geckodriver-arm64")

        
def screenshot_webpage(url: str, /, *, resolution: str = "1280x720") -> BytesIO:
    """Take a screenshot of a webpage using GeckoDriver

    Args:
        url (str): The URL to get and screenshot

    Returns:
        BytesIO: The image bytes of the screenshot, in PNG format
    """
    w,h = map(int, resolution.split("x"))
    wd = create_webdriver()
    try:
        wd.set_window_size(w,h)
        wd.get(url)
        sleep(1) # give chance for the page to load
        ss = wd.get_screenshot_as_png()
        return BytesIO(ss)
    finally:
        wd.quit()

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
