cmake_minimum_required(VERSION 2.6.0)

project(TcpHub C)

add_executable(tcphub tcphub.c server.c)
add_executable(hubmonitor hubmonitor.c server.c)

target_link_libraries(hubmonitor pthread)

set_target_properties(tcphub hubmonitor PROPERTIES COMPILE_FLAGS -std=gnu99)

install(TARGETS tcphub hubmonitor RUNTIME DESTINATION bin)
