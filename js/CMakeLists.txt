cmake_minimum_required(VERSION 2.6.0)

project(Js C)

set_source_files_properties(${SRC_FILES} PROPERTIES COMPILE_FLAGS "-std=gnu99")

add_executable(canjs canjs.c joystick.c)
target_link_libraries(canjs pthread functions)
install(TARGETS canjs RUNTIME DESTINATION bin)
