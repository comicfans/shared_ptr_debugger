ADD_SUBDIRECTORY(no_leak)

SET(gdb_init "${CMAKE_CURRENT_BINARY_DIR}/gdbinit")

#FILE(WRITE "${gdb_init}" " \
#python \

#end")

FILE(WRITE "${gdb_init}" "python
import sys
sys.path.insert(0, \"${PROJECT_SOURCE_DIR}\")
import leak_helper_gdb
import leak_cmd_gdb
end")

FOREACH(one ${no_leak_tests})
  add_test(NAME "no_leak_${one}"
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/gdb_test.py --gdb ${GDB_COMMAND} --binary $<TARGET_FILE:${one}> --init ${gdb_init}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  )
ENDFOREACH()

