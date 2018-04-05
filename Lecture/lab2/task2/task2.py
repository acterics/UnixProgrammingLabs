#!/usr/bin/python3
import os
import argparse
import glob
import shutil
import sys
from argparse import ArgumentTypeError as err


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


SCRIPT_DESCRIPTION = ('Copy files greater then given size (KB) '
                      'from source path to destination path')

parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
parser.add_argument('source_path',
                    type=PathType(exists=True, type=PathType.DIR_TYPE),
                    help='Source directory for files should copy'
                    )
parser.add_argument('destination_path',
                    type=PathType(exists=True, type=PathType.DIR_TYPE),
                    help='Destination directory for files filtered files'
                    )

args = parser.parse_args()
source_path = os.path.abspath(args.source_path)
destination_path = os.path.abspath(args.destination_path)

if source_path == destination_path:
    message = ("Copying denied. Source path '{source_path}' "
               "is equal to destination path '{destination_path}'").format(
                   source_path=source_path,
                   destination_path=destination_path
    )
    print(message)
    sys.exit(1)

print("Please, enter max file size (KB): ", end=' ', flush=True)
max_size = sys.stdin.readline()

print("Searching files greater then {max_size} KB...".format(
    max_size=max_size)
)

source_files = [(os.path.getsize(file), file) for file in glob.iglob(
    "{source_path}/*".format(source_path=source_path),
    recursive=False)
]


max_size_bytes = int(max_size) * 1024

result_files = filter(
    lambda file_tuple: file_tuple[0] < max_size_bytes,
    source_files
)


if not result_files:
    print("No files less then {max_size} KB found.".format(
        max_size=max_size)
    )
    sys.exit()

print("Copying to {destination_path}...".format(
    destination_path=destination_path)
)

total_bytes = 0
total_count = 0
for file_tuple in result_files:
    print(file_tuple[1])
    shutil.copy2(file_tuple[1], destination_path)
    total_bytes += file_tuple[0]
    total_count += 1

total_size = total_bytes / 1024

print("Copied successfully.")
print("Total files count: {count}".format(count=total_count))
print("Total files size: {size} KB".format(size=total_size))
