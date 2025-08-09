add_library(must_debug_symbol INTERFACE)
target_compile_options(must_debug_symbol INTERFACE -g)

set(NO_LEAK_TESTs)

foreach(one empty_int local_int)
  add_executable(${one} ${one}.cpp)
  target_link_libraries(${one} PRIVATE must_debug_symbol)
  list(APPEND NO_LEAK_TESTS ${one})
endforeach()

set(NO_LEAK_TESTS
    ${NO_LEAK_TESTS}
    PARENT_SCOPE)
