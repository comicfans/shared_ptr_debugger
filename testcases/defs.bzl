load("@rules_cc//cc:defs.bzl", "cc_library", "cc_test")

def no_leak_test(name):
  cc_binary(
    name = name,
    srcs = [name+".cpp"]
  )
