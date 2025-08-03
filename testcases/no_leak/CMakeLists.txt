add_library(must_debug_symbol INTERFACE)
target_compile_options(must_debug_symbol INTERFACE -g)

set(no_leak_tests)

foreach(one local_int)
  add_executable(${one} ${one}.cpp)
  target_link_libraries(${one} PRIVATE must_debug_symbol)
  list(APPEND no_leak_tests ${one})
endforeach()

set(no_leak_tests
    ${no_leak_tests}
    PARENT_SCOPE)
