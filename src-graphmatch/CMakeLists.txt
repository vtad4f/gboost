

set (SRC_VFLIB2
   vflib-2.0/inc/allocpool.h
   vflib-2.0/inc/argedit.h
   vflib-2.0/inc/argloader.h
   vflib-2.0/inc/argraph.h
   vflib-2.0/inc/dict.h
   vflib-2.0/inc/error.h
   vflib-2.0/inc/gene.h
   vflib-2.0/inc/gene_mesh.h
   vflib-2.0/inc/match.h
   vflib-2.0/inc/sd_state.h
   vflib-2.0/inc/state.h
   vflib-2.0/inc/ull_state.h
   vflib-2.0/inc/ull_sub_state.h
   vflib-2.0/inc/vf_mono_state.h
   vflib-2.0/inc/vf_state.h
   vflib-2.0/inc/vf_sub_state.h
   vflib-2.0/inc/vf2_mono_state.h
   vflib-2.0/inc/vf2_state.h
   vflib-2.0/inc/vf2_sub_state.h
   vflib-2.0/inc/xsubgraph.h
   vflib-2.0/src/argedit.cc
   vflib-2.0/src/argloader.cc
   vflib-2.0/src/argraph.cc
   vflib-2.0/src/error.cc
   vflib-2.0/src/gene.cc
   vflib-2.0/src/gene_mesh.cc
   vflib-2.0/src/match.cc
   vflib-2.0/src/sd_state.cc
   vflib-2.0/src/sortnodes.cc
   vflib-2.0/src/sortnodes.h
   vflib-2.0/src/ull_state.cc
   vflib-2.0/src/ull_sub_state.cc
   vflib-2.0/src/vf_mono_state.cc
   vflib-2.0/src/vf_state.cc
   vflib-2.0/src/vf_sub_state.cc
   vflib-2.0/src/vf2_mono_state.cc
   vflib-2.0/src/vf2_state.cc
   vflib-2.0/src/vf2_sub_state.cc
   vflib-2.0/src/xsubgraph.cc
)

set (SRC_GRAPHMATCH
   ${SRC_VFLIB2}
   graphmatch.cpp
)

set (SRC_MY_MEX
   ../src-my-mex/mex.h
)

set (SRC_OMPC_MEX
   ../ompc/examples/mex/mex.h
   ../ompc/examples/mex/mexlib.h
   ../ompc/examples/mex/mexlib.cpp
)

project(graphmatch)
add_library(graphmatch SHARED
   ${SRC_GRAPHMATCH}
   ${SRC_MY_MEX}
   ${SRC_OMPC_MEX}
)
include_directories(graphmatch
   vflib-2.0/inc/
   ../src-my-mex/
   ../ompc/examples/
)
set_target_properties(graphmatch PROPERTIES COMPILE_OPTIONS "-Wall" "--std=c++11" "-g")

