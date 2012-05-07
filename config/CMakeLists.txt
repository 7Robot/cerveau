cmake_minimum_required(VERSION 2.6.0)

project(ConfigFiles C)

install(FILES petit.ini DESTINATION /etc/robot/petit.ini)
install(FILES gros.ini DESTINATION /etc/robot/petit.ini)
