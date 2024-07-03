from PIL import Image

from src.domain.ocr.model import ocr_model


def crop_image(
    *,
    image: Image.Image,
    roi: ocr_model.Roi,
) -> Image.Image:
    # image.crop(box=(left, top, right, bottom))

    # vertical crop
    image_width, image_height = image.size
    crop_right = roi.x2 if roi.x2 < image_width else image_width
    if roi.x1 and roi.x2:
        image = image.crop(box=(roi.x1, 0, crop_right, image_height))
    elif roi.x1:
        image = image.crop(box=(roi.x1, 0, image_width, image_height))
    elif roi.x2:
        image = image.crop(box=(0, 0, crop_right, image_height))

    # horizontal crop
    image_width, image_height = image.size
    crop_bottom = roi.y2 if roi.y2 < image_height else image_height
    if roi.y1 and roi.y2:
        image = image.crop(box=(0, roi.y1, image_width, crop_bottom))
    elif roi.y1:
        image = image.crop(box=(0, roi.y1, image_width, image_height))
    elif roi.y2:
        image = image.crop(box=(0, 0, image_width, crop_bottom))

    return image
