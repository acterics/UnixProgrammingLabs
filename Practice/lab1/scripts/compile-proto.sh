#!/bin/bash
SRC_DIR=./protobuf
DST_DIR=./src/generated

mkdir -p $DST_DIR
touch $DST_DIR/__init__.py

protoc -I=$SCR_DIR. --python_out=$DST_DIR $SRC_DIR/components.proto 
touch $DST_DIR/protobuf/__init__.py