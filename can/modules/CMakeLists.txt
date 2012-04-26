cmake_minimum_required(VERSION 2.6.0)

project(CanModule C)

file(GLOB SRC_FILES *.c)

set_source_files_properties(${SRC_FILES} PROPERTIES COMPILE_FLAGS "-std=gnu99")

include_directories(..)


add_library(bin SHARED bin.c)
install(TARGETS bin LIBRARY DESTINATION lib/can)

add_library(dec SHARED dec.c)
install(TARGETS dec LIBRARY DESTINATION lib/can)

add_library(hex SHARED hex.c)
install(TARGETS hex LIBRARY DESTINATION lib/can)

add_library(cmd SHARED cmd.c ini.c)
install(TARGETS cmd LIBRARY DESTINATION lib/can)

add_library(text SHARED text.c ini.c)
install(TARGETS text LIBRARY DESTINATION lib/can)
