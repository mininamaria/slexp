from typing import List

import piexif
import json
import geojson
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
    dst_filename = regex.sub(".json", os.path.basename(src_filename))  # Creating a string
    dst_file_path = os.path.join(d_path, str(dst_filename))  # Composing a filepath
    with open(dst_file_path, "w") as f:
        f.write(json.dumps(conv_dict))
    return dst_filename


"""
This code is going to work with directories
"""


def mk_dst_dir():
    cwd = os.getcwd()  # Get the current working directory
    dst_path = pathlib.Path(os.path.join(cwd, "jsons"))  # Specifying the destination directory path
    dst_path.mkdir(exist_ok=True)  # Making the directory for JSON files
    return dst_path


def mk_src_dir():
    src_path = pathlib.Path(str(input("Введите путь к директории с фотографиями: ")))  # This is our source path
    if not src_path.is_dir():
        return None
    else:
        return src_path


'''
The following code calculates decimal degrees for coordinates
'''


def countitude(crds: List[List[int]]):
    result = crds[0][0] + crds[1][0]/60 + crds[2][0]/(10000*3600)
    return round(result, 2)


def parse_geo(data_dict, src_filename, d_path):
    print("Ready to parse!")
    regex = re.compile(".jpg")
    dst_filename = regex.sub(".json", os.path.basename(src_filename))  # Creating a string
    dst_file_path = os.path.join(d_path, str(dst_filename))  # Composing a filepath
    with open(dst_file_path, "w") as f:
        f.write(json.dumps(data_dict))
    return dst_filename
def log_init(src_path, dst_path):
    log_path = pathlib.Path(os.path.join(dst_path, "log.txt"))  # Specifying the log file path
    with open(log_path, "w") as log_f:
        if src_path is None:
            log_f.write(f"ERROR: {src_path} is not a directory\n")
            return None
        log_f.write(f"SOURCE DIRECTORY: {src_path}\n")
        log_f.write(f"DESTINATION DIRECTORY: {dst_path}\n")
        log_f.write(f"IMAGES:\n")
    return log_path


def main():
    src_dir = mk_src_dir()
    print(str(src_dir))  # DEBUG
    dst_dir = mk_dst_dir()
    print(str(dst_dir))  # DEBUG
    log_path = log_init(src_dir, dst_dir)
    if log_path is None:
        return
    with open(log_path, "a") as log:
        for f in src_dir.iterdir():
            if f.suffix == ".jpg":
                with open(f, "r") as file:
                    log.write(f.name + "\n")
                    exif_dictionary = piexif.load(str(f))
                    normal_dict = make_readable(exif_dictionary, ("GPS",))
                    if len(normal_dict) == 0:
                        log.write("GPS data empty\n")
                    else:  # "basename" returns the filename stripped off its path
                        json_path = parse_dict(normal_dict, f, dst_dir)
                        log.write(f"{json_path}\n")
            #   write things into the file


if __name__ == "__main__":
    main()
