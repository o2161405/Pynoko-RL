# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/luke/Desktop/pynoko-main(5)/pynoko-main"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build"

# Utility rule file for GenerateTestCases.

# Include any custom commands dependencies for this target.
include _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/compiler_depend.make

# Include the progress variables for this target.
include _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/progress.make

_deps/kinoko-build/CMakeFiles/GenerateTestCases: _deps/kinoko-build/testCases.bin

_deps/kinoko-build/testCases.bin: _deps/kinoko-src/testCases.json
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --blue --bold --progress-dir="/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Running generate_tests.py to create test cases"
	cd "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build" && python /home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-src/tools/generate_tests.py /home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-src/testCases.json /home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build/testCases.bin

GenerateTestCases: _deps/kinoko-build/CMakeFiles/GenerateTestCases
GenerateTestCases: _deps/kinoko-build/testCases.bin
GenerateTestCases: _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/build.make
.PHONY : GenerateTestCases

# Rule to build all files generated by this target.
_deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/build: GenerateTestCases
.PHONY : _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/build

_deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/clean:
	cd "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build" && $(CMAKE_COMMAND) -P CMakeFiles/GenerateTestCases.dir/cmake_clean.cmake
.PHONY : _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/clean

_deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/depend:
	cd "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/luke/Desktop/pynoko-main(5)/pynoko-main" "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-src" "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build" "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build" "/home/luke/Desktop/pynoko-main(5)/pynoko-main/build/_deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/DependInfo.cmake" "--color=$(COLOR)"
.PHONY : _deps/kinoko-build/CMakeFiles/GenerateTestCases.dir/depend

