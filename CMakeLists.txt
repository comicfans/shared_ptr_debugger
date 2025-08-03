project(shared_ptr_debugger)

cmake_minimum_required(VERSION 3.22)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules)

find_package(GDB)
find_package(Python3 COMPONENTS Interpreter)

if(NOT GDB_FOUND OR NOT Python3_FOUND)
  message(FATAL_ERROR "gdb or python3 not found")
endif()

foreach(module pytest pip)
  execute_process(
    COMMAND ${Python3_EXECUTABLE} -m ${module} --version
    RESULT_VARIABLE "${module}_exit_code"
    OUTPUT_VARIABLE "${module}_version"
    ERROR_VARIABLE "${module}_error"
    OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT ${${module}_exit_code} EQUAL 0)
    message(
      FATAL_ERROR
        "${module} not found, can't run test"
        "exit code ${${module}_exit_code}," "stdout: ${${module}_version}, "
        "stderr: ${${module}_error}")
  else()
    message(STATUS "using ${module} ${${module}_version}")
  endif()
endforeach()

message(STATUS "using python ${Python3_VERSION}: ${Python3_EXECUTABLE}"
               "and GDB version ${GDB_VERSION} to test : ${GDB_COMMAND}")

enable_testing()

add_subdirectory(python)
add_subdirectory(testcases)
