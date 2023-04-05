import piexif
import json
import re
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


def parse_dict(conv_dict, src_filename):
    regex = re.compile(".jpg")
    dest_filename = regex.sub(".json", src_filename)
    with open(dest_filename, "w") as f:
        f.write(json.dumps(conv_dict))
    print(dest_filename)


exif_dictionary = piexif.load("IMG_20200702_124338.jpg")
normal_dict = make_readable(exif_dictionary, ("GPS",))
parse_dict(normal_dict, "IMG_20200702_124338.jpg")

