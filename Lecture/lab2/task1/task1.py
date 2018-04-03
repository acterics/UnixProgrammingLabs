#!/usr/bin/python3
import os
import argparse
import glob
import collections
from path_type import PathType
from sys import stdin, stdout

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

for file_tuple in ordered_files:
    result_file.write("{filename}\n".format(
        filename=os.path.basename(file_tuple[1])
    ))
result_file.close()
