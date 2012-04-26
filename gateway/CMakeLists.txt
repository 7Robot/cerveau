cmake_minimum_required(VERSION 2.6.0)

add_executable(cangateway cangateway.c)

target_link_libraries(cangateway functions)

set_target_properties(cangateway PROPERTIES COMPILE_FLAGS -std=gnu99)

install(TARGETS cangateway RUNTIME DESTINATION bin)
