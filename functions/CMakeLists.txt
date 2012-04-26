cmake_minimum_required(VERSION 2.6.0)

project(Functions C)

file(GLOB SRC_FILES *.c)

add_library(functions STATIC ${SRC_FILES})

set_target_properties(functions PROPERTIES COMPILE_FLAGS -std=gnu99)
