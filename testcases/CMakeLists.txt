add_subdirectory(no_leak)

set(GDB_INIT "${CMAKE_CURRENT_SOURCE_DIR}/gdbinit")

foreach(one gdb_test)
  set(py_file ${CMAKE_CURRENT_SOURCE_DIR}/${one}.py)
  add_test(
    NAME ${one}
    COMMAND ${Python3_EXECUTABLE} ${py_file} --gdb
            ${GDB_COMMAND} --init ${GDB_INIT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

  set_tests_properties("${one}" PROPERTIES FIXTURES_REQUIRED "python_test")
endforeach()


foreach(one ${NO_LEAK_TESTS})
  set(py_file ${CMAKE_CURRENT_SOURCE_DIR}/no_leak/${one}.py)
  if (NOT EXISTS ${py_file})
    message(STATUS "Skipping test ${one}, no python file found")
    continue()
  endif()

  set(NAME "no_leak_${one}")
  add_test(
    NAME ${NAME}
    COMMAND ${Python3_EXECUTABLE} ${py_file} --gdb
            ${GDB_COMMAND} --binary $<TARGET_FILE:${one}> --init ${GDB_INIT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
  set_tests_properties("${NAME}" PROPERTIES FIXTURES_REQUIRED "python_test")

  set(RECORDING "leak_recording_no_leak_${one}")
  add_test(
    NAME ${RECORDING}
    COMMAND ${Python3_EXECUTABLE} ${py_file} --gdb
    ${GDB_COMMAND} --binary $<TARGET_FILE:${one}> --init ${GDB_INIT} --recording ${CMAKE_CURRENT_SOURCE_DIR}/${RECORDING}.sqlite3
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

  set_tests_properties("${RECORDING}" PROPERTIES FIXTURES_REQUIRED "python_test")
endforeach()
