ADD_LIBRARY(must_debug_symbol INTERFACE)
TARGET_COMPILE_OPTIONS(must_debug_symbol 
  INTERFACE -g)

SET(no_leak_tests)

FOREACH(one local_int)
  ADD_EXECUTABLE(${one} ${one}.cpp)
  TARGET_LINK_LIBRARIES(${one} PRIVATE must_debug_symbol)
  LIST(APPEND no_leak_tests ${one})
ENDFOREACH()  

SET(no_leak_tests ${no_leak_tests} PARENT_SCOPE)
