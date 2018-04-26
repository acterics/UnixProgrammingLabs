package com.acterics.unix.lab1.consumer


fun main(args: Array<String>) {
    print(args.toList())
    System.in.bufferedReader().readLines()
        .forEach {
            print("$it\n")
        }
}