cmake_minimum_required (VERSION 3.6)
project(Lamb)

add_executable(Lamb main.cpp)

add_subdirectory(deps/sleepy-discord)
target_link_libraries(Lamb sleepy-discord)