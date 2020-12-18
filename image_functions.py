import exiftool


def get_image_size(path):
    with exiftool.ExifTool() as et:
        return et.get_metadata(path)['File:Filesize']
