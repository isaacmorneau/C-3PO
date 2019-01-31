cmake_minimum_required (VERSION 3.0)
project (c3po)

set (c3po_VERSION_MAJOR 1)
set (c3po_VERSION_MINOR 0)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()


set(CMAKE_C_FLAGS "-Wall -Wextra -Wno-unknown-pragmas")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -fsanitize=address -fno-omit-frame-pointer")
set(CMAKE_C_FLAGS_RELEASE "-Ofast -s -fno-ident  -march=native -flto -DNDEBUG")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_LIST_DIR}")

add_definitions(-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -DC3PO)


#this will consume all .c and .h files in src and after parsing will put them in c3po
add_custom_target(gen_c3po ALL COMMAND python3 "${PROJECT_SOURCE_DIR}/c3po.py" "${PROJECT_SOURCE_DIR}/src" "${PROJECT_SOURCE_DIR}/c3po")
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

set(SOURCES
    "./c3po/test.c"
    "./c3po/c3po.c"
    )

add_executable(c3po ${SOURCES})

if (CMAKE_BUILD_TYPE EQUAL Release)
    set_target_properties(c3po PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

target_link_libraries(c3po rt Threads::Threads)
