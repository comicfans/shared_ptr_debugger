project(shared_ptr_debugger)

cmake_minimum_required(VERSION 3.22)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules)

find_package(GDB)
find_package(Python3 COMPONENTS Interpreter)

if(NOT GDB_FOUND OR NOT Python3_FOUND)
  message(FATAL_ERROR "gdb or python3 not found")
endif()

foreach(MODULE pytest pip)
  execute_process(
    COMMAND ${Python3_EXECUTABLE} -m ${MODULE} --version
    RESULT_VARIABLE "${MODULE}_EXIT_CODE"
    OUTPUT_VARIABLE "${MODULE}_VERSION"
    ERROR_VARIABLE "${MODULE}_ERROR"
    OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT ${${MODULE}_EXIT_CODE} EQUAL 0)
    message(
      FATAL_ERROR
        "${MODULE} not found, can't run test, exit code ${${MODULE}_EXIT_CODE},stdout: ${${MODULE}_VERSION}, stderr: ${${MODULE}_ERROR}"
    )
  else()
    message(STATUS "using ${MODULE} ${${MODULE}_VERSION}")
  endif()
endforeach()

message(
  STATUS
    "using python ${Python3_VERSION}: ${Python3_EXECUTABLE} and GDB version ${GDB_VERSION} to test : ${GDB_COMMAND}"
)

enable_testing()

add_subdirectory(python)
add_subdirectory(testcases)
