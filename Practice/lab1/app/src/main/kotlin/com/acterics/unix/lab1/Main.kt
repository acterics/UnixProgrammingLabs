package com.acterics.unix.lab1

import java.io.File

fun main(args: Array<String>) {
    
    val consumerProcesses = listOf("Tabaco", "Paper", "Matches").map { buildSmoker(it) }

    consumerProcesses[0].inputStream.bufferedReader().readLines().forEach { line ->
        print("$line\n")
    }

}


fun buildSmoker(name: String): Process {
    val currentDir = File("../")
    return ProcessBuilder("java -jar ./consumer/build/libs/consumer.jar $name".split(" "))
            .directory(currentDir)
            .redirectOutput(ProcessBuilder.Redirect.INHERIT)
            .redirectError(ProcessBuilder.Redirect.INHERIT)
            .start()   
}