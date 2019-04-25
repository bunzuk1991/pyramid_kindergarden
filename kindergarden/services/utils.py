import uuid
import os
import shutil
from pyramid.threadlocal import get_current_registry
from pyramid.settings import aslist
from PIL import Image
from secrets import token_urlsafe


def get_param_from_config(param):
    registry = get_current_registry()
    settings = registry.settings
    param_value = settings[param] if param in settings else None
    return param_value


def resize(image_name, images_path, images_thumbnails_path, size):
    img = Image.open(os.path.join(images_path, image_name))
    resized = img.resize(size, Image.ANTIALIAS)
    resized.save(os.path.join(images_thumbnails_path, image_name))


def upload_file(form_field, path='', resize_image=False, images_thumbnails_path='', size=None):
    if not path:
        path = get_param_from_config('image_path')

    if hasattr(form_field.data, 'filename'):
        input_file = form_field.data.file
        input_file.seek(0)

        # filename = uuid.uuid4().hex + os.path.splitext(os.path.basename(form_field.data.filename))[1]
        filename = token_urlsafe(12) + os.path.splitext(os.path.basename(form_field.data.filename))[1]

        file_path = os.path.join(path, filename)

        temp_file_path = file_path

        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)

        if resize_image:
            if not images_thumbnails_path:
                images_thumbnails_path = get_param_from_config('thumbnails_path')

            if not size:
                size = aslist(get_param_from_config('thumbnails_size'))

            width, height = size

            resize(filename, path, images_thumbnails_path, (int(width), int(height)))

        return filename
    else:
        return None
