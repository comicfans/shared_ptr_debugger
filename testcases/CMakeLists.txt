add_subdirectory(no_leak)

set(GDB_INIT "${CMAKE_CURRENT_SOURCE_DIR}/gdbinit")

foreach(one ${NO_LEAK_TESTS})
  set(NAME "no_leak_${one}")
  add_test(
    NAME ${NAME}
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/gdb_test.py --gdb
            ${GDB_COMMAND} --binary $<TARGET_FILE:${one}> --init ${GDB_INIT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
  set_tests_properties("${NAME}" PROPERTIES FIXTURES_REQUIRED "python_test")
endforeach()
