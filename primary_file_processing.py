import piexif
import json
import re
import os
import pathlib

from PIL import Image
import PIL.ExifTags
from piexif import TAGS

"""   
this function converts incomprehensible tag IDs to 
adequate tag names and turns any bytes values to strings,
because otherwise it is impossible to parse a json
"""


def make_readable(exif_dict, params):
    readable_dict = {}
    str_name = "name"
    for ifd in params:
        for tag in exif_dict[ifd]:
            tag_k = piexif.TAGS[ifd][tag][str_name]
            if type(exif_dict[ifd][tag]) == bytes:
                tag_val = exif_dict[ifd][tag].decode()
            else:
                tag_val = exif_dict[ifd][tag]
            readable_dict.update({tag_k: tag_val})
    return readable_dict


"""
This piece of code is responsible for parsing a JSON:
we put all the info about an image to a JSON file with its name.
NB1: we are using JPG files.
NB2: our convertible dictionary must not contain any byte values,
thus it is to be made readable first.
"""


def parse_dict(conv_dict, src_filename, d_path):
    regex = re.compile(".jpg")
    dest_filename = regex.sub(".json", src_filename)    # Creating a string
    dest_file_path = os.path.join(d_path, str(dest_filename))  # Composing a filepath
    with open(dest_file_path, "w") as f:
        f.write(json.dumps(conv_dict))
    print(dest_filename)


"""
This code is going to work with directories
"""

def main():
    cwd = os.getcwd()  # Get the current working directory
    dest_path = pathlib.Path(os.path.join(cwd, "jsons"))  # Specifying the destination directory path
    dest_path.mkdir(exist_ok=True)  # Making the directory for JSON files
    src_path = pathlib.Path(str(input("Введите путь к директории с фотографиями")))  # This is our source path
    # os.chdir(src_path)
    if not src_path.is_dir():
        print(f"{src_path} is not a directory")

    for f in src_path.iterdir():
        with open(f, "r") as file:
            print("hey")
        #   write things into the file

    exif_dictionary = piexif.load("IMG_20200702_124338.jpg")
    normal_dict = make_readable(exif_dictionary, ("GPS",))
    parse_dict(normal_dict, "IMG_20200702_124338.jpg", dest_path)


if __name__ == "__main__":
    main()
