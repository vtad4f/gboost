

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

set (SRC_MY_MEX
   ../src-my-mex/mex.h
)

set (SRC_OMPC_MEX
   ../ompc/examples/mex/mex.h
   ../ompc/examples/mex/mexlib.h
   ../ompc/examples/mex/mexlib.cpp
)

project(gspan)
add_library(gspan SHARED
   ${SRC_GSPAN}
   ${SRC_MY_MEX}
   ${SRC_OMPC_MEX}
)
include_directories(gspan
   ../src-my-mex/
   ../ompc/examples/
)
set_target_properties(gspan PROPERTIES COMPILE_OPTIONS "-Wall" "--std=c++11" "-g")

