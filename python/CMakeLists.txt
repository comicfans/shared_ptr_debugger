add_test(NAME "python_package_test"
  COMMAND ${Python3_EXECUTABLE} -m pip install -e .
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

add_test(NAME  "python_test"
    COMMAND ${Python3_EXECUTABLE} -m pytest
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)


set_tests_properties("python_test" PROPERTIES
    FIXTURES_REQUIRED "python_package_test"
  )

