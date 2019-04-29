

set (SRC_GSPAN
   dfs.cpp
   graph.cpp
   gspan.cpp
   gspan.h
   ismin.cpp
   main.cpp
   mexgspan.cpp
   misc.cpp
)

set (SRC_MEX_REPLACEMENT
   ../src-my-mex/mex.h
)


project(gspan)
add_library(gspan SHARED
   ${SRC_GSPAN}
   ${SRC_MEX_REPLACEMENT}
)
include_directories(gspan
   .
   ../src-my-mex/
)
set_target_properties(gspan PROPERTIES COMPILE_OPTIONS "-Wall" "--std=c++11" "-g")

