project(Beeper C)

add_executable(beeper beeper.c)

install(TARGETS beeper RUNTIME DESTINATION bin)

