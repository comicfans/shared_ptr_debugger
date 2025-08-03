CMAKE_MINIMUM_REQUIRED(VERSION 3.22)
PROJECT(shared_ptr_debugger)

SET(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules)

FIND_PACKAGE(GDB)
FIND_PACKAGE(Python3 COMPONENTS Interpreter)

if(NOT GDB_FOUND OR NOT Python3_FOUND)
  message(FATAL_ERROR "gdb or python3 not found")
endif()



FOREACH(MODULE pytest pip)
  execute_process(
    COMMAND ${Python3_EXECUTABLE} -m ${MODULE} --version
    RESULT_VARIABLE "${MODULE}_EXIT_CODE"
    OUTPUT_VARIABLE "${MODULE}_VERSION"
    ERROR_VARIABLE "${MODULE}_ERROR"
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  
  if (NOT ${${MODULE}_EXIT_CODE} EQUAL 0)
    message(FATAL_ERROR "${MODULE} not found, can't run test, exit code ${${MODULE}_EXIT_CODE},stdout: ${${MODULE}_VERSION}, stderr: ${${MODULE}_ERROR}")
  else()
    message(STATUS "using ${MODULE} ${${MODULE}_VERSION}")
  endif()
ENDFOREACH()



message(STATUS "using python ${Python3_VERSION}: ${Python3_EXECUTABLE} and GDB version ${GDB_VERSION} to test : ${GDB_COMMAND}")

ENABLE_TESTING()

ADD_SUBDIRECTORY(python)
ADD_SUBDIRECTORY(testcases)
