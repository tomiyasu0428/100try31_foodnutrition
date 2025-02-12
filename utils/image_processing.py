# utils/image_processing.py
from PIL import Image
import io


def preprocess_image(file_storage):
    """
    アップロードされた画像ファイルの前処理を行います。
    例: 画像を 256x256 にリサイズして JPEG のバイト列として返す。
    """
    image = Image.open(file_storage)
    image = image.resize((256, 256))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    return img_byte_arr.getvalue()
