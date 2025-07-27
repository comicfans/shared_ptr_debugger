PROJECT(shared_ptr_debugger)

CMAKE_MINIMUM_REQUIRED(VERSION 3.22)

SET(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules)

FIND_PACKAGE(GDB)
FIND_PACKAGE(Python3 COMPONENTS Interpreter)

if(GDB_FOUND AND Python3_FOUND)
  message(STATUS "using python ${Python3_VERSION}: ${Python3_EXECUTABLE} and GDB version ${GDB_VERSION} to test : ${GDB_COMMAND}")
else()
  message(WARNING "gdb or python3 not found, can't run test")
  return()
endif()
ENABLE_TESTING()

ADD_SUBDIRECTORY(testcases)
