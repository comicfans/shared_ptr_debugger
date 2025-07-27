ADD_SUBDIRECTORY(no_leak)


FILE(WRITE "${CMAKE_CURRENT_BINARY_DIR}/.gdbinit" " \
set style enabled 'off'
python \
import sys \
sys.path.insert(0, \"${CMAKE_PROJECT_SOURCE_DIR}\")\
import leak_helper_gdb \
import leak_cmd_gdb\
end")


FOREACH(one ${no_leak_tests})
  add_test(NAME "no_leak_${one}"
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/gdb_test.py --gdb ${GDB_COMMAND} --binary $<TARGET_FILE:${one}>
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  )
ENDFOREACH()

