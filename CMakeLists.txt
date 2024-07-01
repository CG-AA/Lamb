cmake_minimum_required (VERSION 3.6)
project(Lamb)

find_package(Wool REQUIRED)

add_executable(Lamb main.cpp)

target_link_libraries(Lamb Wool::Wool)