import piexif
import json
import re
import os
import pathlib
from typing import List, Dict, Tuple

import PIL.ExifTags
from piexif import TAGS


def countitude(crds: List[List[int]]) -> float:
    """
    calculating latitude or longitude

    :param crds: integer values from GPSLongitude or GPSLatitude in degrees, minutes and seconds
    :return: double: decimal degrees
    """
    if crds is None:
        return 0
    result = crds[0][0] + crds[1][0] / 60 + crds[2][0] / (10000 * 3600)
    return round(result, 3)


def altitude(crds: Tuple[int, int]) -> int:
    """
    calculating altitude

    :param crds: integer values from GPSAltitude
    :return : integer value: meters above sea level
    """
    if crds is None:
        return 0
    result = crds[0] / 1000
    return round(result)


def time_stamp(crds: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> str:
    """
    reformatting time

    :param crds: integer values from GPSTimeStamp
    :return : string: hh:mm:ss
    """
    if crds is None:
        return "unknown"
    return f"{str(crds[0][0])}:{str(crds[1][0])}:{str(crds[2][0])}"


def prepare_crds(n_dict: Dict) -> List:
    coordinates = [countitude(n_dict.get("GPSLatitude")),
                   countitude(n_dict.get("GPSLongitude")),
                   altitude(n_dict.get("GPSAltitude"))]
    # if coordinates == [0, 0, 0]:
    # coordinates = get from place
    return coordinates


def prepare_geo(n_dict: Dict) -> Dict:
    """
    preparing GPS data to be parsed to GeoJSON

    :param n_dict: readable dictionary (no byte values)
    :return geo_data: dictionary ready to be parsed to GeoJSON (point)

    NB: normalized dictionary must not contain any byte values, thus it is to use make_readable() first
    """

    geometry = {"type": "Point",
                "coordinates": prepare_crds(n_dict)}

    date = n_dict.get("GPSDateStamp")  # parsing date
    time = time_stamp(n_dict.get("GPSTimeStamp"))  # parsing time
    properties = {"date": date,
                  "time": time,
                  "place": "",
                  "tags": []}

    features = [{"type": "Feature",
                 "geometry": geometry,
                 "properties": properties}]

    geo_data = {"type": "FeatureCollection",
                "features": features}
    return geo_data


def make_readable(exif_dict, params):
    """
    processing EXIF data to make them readable

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


def mk_json(conv_dict, src_filename, dst_path):
    """
    parsing JSON to a separate file

    :param dict conv_dict:  a dictionary of exif data with no byte values,
    :param str src_filename: only the name, no path. E.g. IMG001.jpg,
    :param Path dst_path: path to the directory for storing JSON files. Check out mr_dst_dir()
    :return: dst_filename
    """
    regex = re.compile(str(pathlib.Path(src_filename).suffix))

    dst_filename = regex.sub(".json", src_filename)  # Creating a string
    dst_file_path = os.path.join(dst_path, str(dst_filename))  # Composing a filepath

    with open(dst_file_path, "w") as f:
        f.write(json.dumps(conv_dict))  # Creating a JSON and writing it to our file

    return dst_filename


def mk_geojson(json_filename):
    """
    rewriting JSON file with GeoJSON

    :param json_filename:
    """

    with open(json_filename, "r") as f:
        j = json.loads(f.read())  # Creating a JSON and writing it to our file

    with open(json_filename, "w") as f:
        f.write(json.dumps(prepare_geo(j)))  # Creating a JSON and writing it to our file


def mk_dst_dir():
    """
    making destination directory

    :return: dst_path
    """
    cwd = os.getcwd()  # Getting the current working directory
    dst_path = pathlib.Path(os.path.join(cwd, "jsons"))  # Specifying the destination directory path
    dst_path.mkdir(exist_ok=True)  # Making the directory for JSON files
    return dst_path


def mk_src_dir():
    """
    finding and checking source directory

    :return: src_path
    """
    src_path = pathlib.Path(str(input("Введите путь к директории с фотографиями: ")))  # This is our source path
    if not src_path.is_dir():  # Checking whether the entered value is a directory
        return None
    else:
        return src_path


def log_init(src_path, dst_path):
    """
    initializing log

    :type src_path:  Path
    :type dst_path:  Path
    :return: log_path

    Log remembers everything and enables the user to see what has happened.
    Very useful when it comes to errors and failures.
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


def mk_crds(src_filename, dst_dir, n_dict):
    regex = re.compile(str(pathlib.Path(src_filename).suffix))
    dst_filename = regex.sub(".txt", src_filename)  # Creating a string
    dst_path = os.path.join(dst_dir, pathlib.Path(dst_filename))
    crds = prepare_crds(n_dict)
    date = n_dict.get("GPSDateStamp")  # parsing date
    with open(dst_path, "w") as f:
        f.write(f"{crds[0]}, {crds[1]}, {crds[2]}\n")
        if date is not None:
            f.write(date[:4])
    return dst_path


def main():
    src_dir = mk_src_dir()
    dst_dir = mk_dst_dir()
    log_path = log_init(src_dir, dst_dir)
    if log_path is None:
        return
    # register_heif_opener()
    with open(log_path, "a") as log:
        for f in src_dir.iterdir():
            if f.suffix == ".jpg" or f.suffix == ".JPG" or f.suffix == ".jpeg":
                with open(f, "r") as file:
                    log.write(f.name + "\n")
                    exif_dictionary = piexif.load(str(f))
                    normal_dict = make_readable(exif_dictionary, ("GPS",))
                    if len(normal_dict) == 0:
                        log.write("\tGPS data empty\n")
                    else:
                        json_path = mk_json(normal_dict, f.name, dst_dir)
                        mk_geojson(os.path.join(dst_dir, json_path))
                        log.write(f"\t{json_path}\n")
                        mk_crds(json_path, dst_dir, normal_dict)


if __name__ == "__main__":
    main()
