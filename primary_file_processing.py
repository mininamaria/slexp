import piexif
import json
import re
import os
import pathlib

from PIL import Image
import PIL.ExifTags
from piexif import TAGS


def make_readable(exif_dict, params):
    """
    preparing to parse a JSON.
    tags: IDs -> names,
    values: bytes -> str

    :param dict exif_dict:  a dictionary of exif data,
    :param tuple(str) params: the parameters we want to get, e.g. GPS

    :return readable_dict:

    """
    readable_dict = {}
    str_name = "name"
    for ifd in params:
        for tag in exif_dict[ifd]:
            tag_k = piexif.TAGS[ifd][tag][str_name]
            # the following code turns bytes to str, because otherwise it is impossible to parse a json
            if type(exif_dict[ifd][tag]) == bytes:
                tag_val = exif_dict[ifd][tag].decode()
            else:
                tag_val = exif_dict[ifd][tag]
            readable_dict.update({tag_k: tag_val})
    return readable_dict


def parse_dict(conv_dict, src_filename, dst_path):
    """
    This piece of code is responsible for parsing a JSON:
    we put all the info about an image to a JSON file with its name.

    :param dict conv_dict:  a dictionary of exif data with no byte values,
    :param str src_filename: only the name, no path. E.g. IMG001.jpg,
    :param Path dst_path: path to the directory for storing JSON files. Check out mr_dst_dir()/

    NB: our convertible dictionary must not contain any byte values, thus it is to use make_readable() first.

    :return: dst_filename
    """
    regex = re.compile(".jpg")
    dst_filename = regex.sub(".json", src_filename)  # Creating a string
    dst_file_path = os.path.join(dst_path, str(dst_filename))  # Composing a filepath
    with open(dst_file_path, "w") as f:
        f.write(json.dumps(conv_dict))  # Creating a JSON and writing it to our file
    return dst_filename


def mk_dst_dir():
    """
    This makes the destination directory

    :return: dst_path
    """
    cwd = os.getcwd()  # Getting the current working directory
    dst_path = pathlib.Path(os.path.join(cwd, "jsons"))  # Specifying the destination directory path
    dst_path.mkdir(exist_ok=True)  # Making the directory for JSON files
    return dst_path


def mk_src_dir():
    """
    This finds and checks the source directory
    :return: src_path
    """
    src_path = pathlib.Path(str(input("Введите путь к директории с фотографиями: ")))  # This is our source path
    if not src_path.is_dir():  # Checking whether the entered value is a directory
        return None
    else:
        return src_path


def log_init(src_path, dst_path):
    """
    This initializes our log: it remembers everything
    and enables the user to see what has happened.
    Very useful when it comes to errors and failures.

    :type src_path:  Path
    :type dst_path:  Path
    :return: log_path
    """
    log_path = pathlib.Path(os.path.join(dst_path, "log.txt"))  # Specifying the log file path
    with open(log_path, "w") as log_f:
        if src_path is None:
            log_f.write(f"ERROR: {src_path} is not a directory\n")
            return None
        log_f.write(f"SRC: {src_path}\n")
        log_f.write(f"DST: {dst_path}\n")
        log_f.write(f"IMAGES:\n")
    return log_path


def main():
    src_dir = mk_src_dir()
    dst_dir = mk_dst_dir()
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
                        log.write("\tGPS data empty\n")
                    else:
                        json_path = parse_dict(normal_dict, f.name, dst_dir)
                        log.write(f"\t{json_path}\n")


if __name__ == "__main__":
    main()
