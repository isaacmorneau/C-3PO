cmake_minimum_required(VERSION 3.4)
project(c3po)

set(c3po_VERSION_MAJOR 1)
set(c3po_VERSION_MINOR 0)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()


set(CMAKE_C_FLAGS "-fvisibility=hidden -masm=intel -Wall -Wextra -Wno-unknown-pragmas")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -fsanitize=address -fno-omit-frame-pointer")
set(CMAKE_C_FLAGS_RELEASE "-Ofast -s -fno-ident  -march=native -flto -DNDEBUG")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_LIST_DIR}")

add_definitions(-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE)

#generated by gen_c3po
set(SOURCES
    "./gen/test.c"
    "./gen/c3po.c"
    )
set(SOURCES_DEBUG
    "./src/test.c"
    "./src/c3po.c"
    )

#enable -rdynamic
set(CMAKE_ENABLE_EXPORTS 1)

add_executable(c3po ${SOURCES})
target_compile_definitions(c3po PRIVATE C3PO)

add_executable(c3pod ${SOURCES_DEBUG})
include_directories("${CMAKE_CURRENT_BINARY_DIR}" "./src")

#also depends on gen for actual sources
#this will consume all .c and .h files in src and after parsing will put them in c3po
add_custom_target(gen_c3po ALL COMMAND python3 "${PROJECT_SOURCE_DIR}/c3po.py" "build" "-s" "${PROJECT_SOURCE_DIR}/src" "-o" "${PROJECT_SOURCE_DIR}/gen")
#ensure code works before attempting generation
add_dependencies(gen_c3po c3pod)
#this ensures that they will be deleted on clean
set_directory_properties(PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${PROJECT_SOURCE_DIR}/gen")
#ensure generation works before attempting final compilation
add_dependencies(c3po gen_c3po)

add_custom_target(post_c3po ALL COMMAND python3 ${PROJECT_SOURCE_DIR}/c3po.py "post" "-s" "${PROJECT_BINARY_DIR}/c3po")
add_dependencies(post_c3po c3po)


if (CMAKE_BUILD_TYPE EQUAL Release)
    set_target_properties(c3po PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
    set_target_properties(c3pod PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

target_link_libraries(c3po rt dl Threads::Threads)
target_link_libraries(c3pod rt dl Threads::Threads)
