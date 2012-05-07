cmake_minimum_required(VERSION 2.6.0)

project(Can C)

file(GLOB SRC_FILES *.c)

set_source_files_properties(${SRC_FILES} PROPERTIES COMPILE_FLAGS "-std=gnu99")

add_library(can SHARED libcan.c)
install(TARGETS can LIBRARY DESTINATION lib)

add_subdirectory(modules)

add_executable(canbridge canbridge.c)
target_link_libraries(canbridge can dl pthread functions)
install(TARGETS canbridge RUNTIME DESTINATION bin)
