from glob import glob
from os import path
from subprocess import Popen
import argparse
import json
import re

AWS_CLI_COMMAND = """aws s3 cp %s %s --content-type "image/svg+xml; charset=utf-8" --cache-control max-age=31536000,public --acl public-read --metadata-directive REPLACE"""

OUTPUT_LIST_FILE_NAME = "list.json"
OUTPUT_MAP_FILE_NAME = "filenames.json"
# Whether to upload and list the largest size. If False, the smallest icon is uploaded.
# This shouldn't matter for SVGs.
PREFER_LARGEST_SIZE = True

def upload_file_to_svg(local_pathname, s3_pathname):
    cmd = AWS_CLI_COMMAND % (local_pathname, s3_pathname)
    p = Popen(cmd, shell=True)
    stdout, stderr = p.communicate()
    if stderr:
        raise Exception(stderr)


def upload_svg_icons_to_s3(svg_icons, s3_folder_pathname):
    comp = max if PREFER_LARGEST_SIZE else min
    icon_list = [v[comp(v.keys())] for v in svg_icons.values()]
    for icon in icon_list:
        upload_file_to_svg(icon['pathname'], s3_folder_pathname + icon['filename'])


def write_svg_icon_name_list(svg_icons):
    f = open(OUTPUT_LIST_FILE_NAME, "w")
    f.write(json.dumps(sorted(svg_icons.keys())))
    f.close()


def write_svg_icon_name_filename_tuples(svg_icons):
    comp = max if PREFER_LARGEST_SIZE else min
    icon_filename_list = [(icon_name, v[comp(v.keys())]['filename']) for icon_name, v in svg_icons.items()]
    f = open(OUTPUT_MAP_FILE_NAME, "w")
    f.write(json.dumps(sorted(icon_filename_list, key=lambda x: x[0])))
    f.close()


def get_svg_icon_list():
    """
    {
        [icon_name:string]: {
            [size_px:int]: {
                pathname: '',
                filename: '',
            }
            ...
        }
        ...
    }
    """
    icons = {}
    glob_pattern = path.join(path.dirname(path.realpath(__file__)), "material-design-icons/*/svg/production/*.svg")
    for pathname in glob(glob_pattern):
        (dirname, filename) = path.split(pathname)
        r = re.match(r"ic_([a-z0-9_]+?)_?([0-9]+)px.svg", filename)
        (icon_name, icon_size) = r.groups(1)
        if icon_name not in icons:
            icons[icon_name] = {}
        icons[icon_name][int(icon_size)] = {
            'pathname': pathname,
            'filename': filename,
        }
    return icons


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="material-design-icons-uploader")
    parser.add_argument('--s3bucket', type=str, help="s3://your-bucket/your/path/")
    args = parser.parse_args()

    svg_icons = get_svg_icon_list()

    write_svg_icon_name_list(svg_icons)
    write_svg_icon_name_filename_tuples(svg_icons)

    if args.s3bucket:
        S3_BUCKET_PATH = "s3://usercontent.formsort.com/formsort/icons/"
        upload_svg_icons_to_s3(svg_icons, S3_BUCKET_PATH)



