cmake_minimum_required (VERSION 3.0)
project (C-3PO)

set (C-3PO_VERSION_MAJOR 1)
set (C-3PO_VERSION_MINOR 0)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()


set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -fsanitize=address -fno-omit-frame-pointer")
set(CMAKE_C_FLAGS_RELEASE "-Ofast -s -fno-ident  -march=native -flto -DNDEBUG")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_LIST_DIR}")

add_definitions(-D_POSIX_C_SOURCE=200809L)
add_definitions(-D_DEFAULT_SOURCE)

SET(SOURCES
    "test.c"
    "c3po.c"
    )

#force regeneration of the obfuscated strings header
add_custom_target(gen_obfs ALL COMMAND python3 "${PROJECT_SOURCE_DIR}/obfs.py" "${PROJECT_SOURCE_DIR}/test_obfs.h" "test_obfs_enc.h")
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

add_executable(C-3PO ${SOURCES})

if (CMAKE_BUILD_TYPE EQUAL Release)
    set_target_properties(C-3PO PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

target_link_libraries(C-3PO rt Threads::Threads)
