import uuid
import os
import shutil
from pyramid.threadlocal import get_current_registry



def get_param_from_config(param):
    registry = get_current_registry()
    settings = registry.settings
    param_value = settings[param] if param in settings else None
    return param_value


def upload_file(form_field, path=''):
    if not path:
        path = get_param_from_config('image_path')

    if hasattr(form_field.data, 'filename'):
        input_file = form_field.data.file
        input_file.seek(0)

        filename = uuid.uuid4().hex + os.path.splitext(os.path.basename(form_field.data.filename))[1]

        file_path = os.path.join(path, filename)

        temp_file_path = file_path

        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)

        return filename
    else:
        return None
