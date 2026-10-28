from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import pytesseract


def extract_text_from_image(
        image_path: str,
        language: str = "eng", 
) -> str:

    """Extract text from a book or notebook image."""

    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    with Image.open(path) as original:
        image = ImageOps.exif_transpose(original)
        image = ImageOps.grayscale(image)
        image = ImageEnhance.Contrast(image).enhance(1.5)

        text = pytesseract.image_to_string(
            image,
            lang=language
        )


    text = text.strip()

    if not text:
        raise ValueError(
            "No text detected. Try a clearer, well-lit image."
        )

    return text