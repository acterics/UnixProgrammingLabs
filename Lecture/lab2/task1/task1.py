#!/usr/bin/python3
import os
import argparse
import glob
import collections
from argparse import ArgumentTypeError as err
from sys import stdin


class PathType(object):

    FILE_TYPE = 'file'
    DIR_TYPE = 'dir'

    def __init__(self, exists=True, type=FILE_TYPE):
        assert exists in (True, False, None)
        assert type in (
            PathType.FILE_TYPE,
            PathType.DIR_TYPE,
            None
        ) or hasattr(type, '__call__')

        self.exists = exists
        self.type = type

    def __call__(self, string):
        is_exist = os.path.exists(string)
        if self.exists is True:
            if not is_exist:
                raise err("Path does not exist: '{path}'".format(path=string))
            elif (self.type == PathType.FILE_TYPE and
                  not os.path.isfile(string)):
                raise err(
                    "Path does not a file: '{path}'".format(path=string)
                )
            elif self.type == PathType.DIR_TYPE and not os.path.isdir(string):
                raise err(
                    "Path does not a directory: '{path}'".format(path=string)
                )
        else:
            if self.exists is False and is_exist:
                raise err("Path exists: '{path}'".format(path=string))
            parent_directory = os.path.dirname(os.path.normpath(string)) or '.'
            if not os.path.isdir(parent_directory):
                raise err(
                    "Parent path is not a directory: '{path}'".format(
                        path=string
                    )
                )
            elif not os.path.exists(parent_directory):
                raise err(
                    "Parent directory does not a exists: '{path}'".format(
                        path=string
                    )
                )
        return string


SCRIPT_DESCRIPTION = ('Find files with with suffix in given catalog '
                      'and write them in specified file, sorted by size.')

parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
parser.add_argument('catalog',
                    type=PathType(exists=True, type=PathType.DIR_TYPE),
                    help='Search directory'
                    )
parser.add_argument('suffix',
                    help='Search files with this suffix')

args = parser.parse_args()
search_path = os.path.abspath(args.catalog)

print("Searching file with suffix '{suffix}' in {path} directory...".format(
    suffix=args.suffix,
    path=search_path
))

result_files = glob.iglob(
    "{path}/**/*{suffix}".format(path=search_path, suffix=args.suffix),
    recursive=True
)

files_with_size = list((os.path.getsize(file), file) for file in result_files)
ordered_files = sorted(files_with_size, key=lambda t: t[0])


print("Please enter destination filename:", end=' ', flush=True)
result_file_name = stdin.readline()

result_file = open(result_file_name, "w")

for file in map(lambda file_tuple: file_tuple[1], ordered_files):
    result_file.write("{filename}\n".format(
        filename=os.path.basename(file)
    ))
result_file.close()
