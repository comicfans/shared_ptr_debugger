ADD_SUBDIRECTORY(no_leak)

SET(gdb_init "${CMAKE_CURRENT_SOURCE_DIR}/gdbinit")


FOREACH(one ${no_leak_tests})
  set(NAME "no_leak_${one}")
  add_test(NAME  ${NAME}
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/gdb_test.py --gdb ${GDB_COMMAND} --binary $<TARGET_FILE:${one}> --init ${gdb_init}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  )
  set_tests_properties("${NAME}" PROPERTIES
    FIXTURES_REQUIRED "python_test"
  )
ENDFOREACH()


