# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-src"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/tmp"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/src/kinoko-populate-stamp"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/src"
  "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/src/kinoko-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/src/kinoko-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-subbuild/kinoko-populate-prefix/src/kinoko-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
