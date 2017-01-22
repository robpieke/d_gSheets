cmake_minimum_required(VERSION 3.5)
project(gSheets)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(RMANTREE $ENV{RMANTREE})
include_directories("${RMANTREE}/include")

add_library(d_gSheets MODULE d_gSheets.cpp)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
target_link_libraries(d_gSheets ${PYTHON_LIBRARIES})

set_target_properties(d_gSheets PROPERTIES PREFIX "")

add_custom_command(TARGET d_gSheets POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_SOURCE_DIR}/py_gSheets.py
    ${CMAKE_CURRENT_BINARY_DIR}/py_gSheets.py)

add_custom_command(TARGET d_gSheets POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/test.rib
        ${CMAKE_CURRENT_BINARY_DIR}/test.rib)
