
# Just picked an arbitrary version
cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

set (SRC_VFLIB2
   src-graphmatch/vflib-2.0/inc/allocpool.h
   src-graphmatch/vflib-2.0/inc/argedit.h
   src-graphmatch/vflib-2.0/inc/argloader.h
   src-graphmatch/vflib-2.0/inc/argraph.h
   src-graphmatch/vflib-2.0/inc/dict.h
   src-graphmatch/vflib-2.0/inc/error.h
   src-graphmatch/vflib-2.0/inc/gene.h
   src-graphmatch/vflib-2.0/inc/gene_mesh.h
   src-graphmatch/vflib-2.0/inc/match.h
   src-graphmatch/vflib-2.0/inc/sd_state.h
   src-graphmatch/vflib-2.0/inc/state.h
   src-graphmatch/vflib-2.0/inc/ull_state.h
   src-graphmatch/vflib-2.0/inc/ull_sub_state.h
   src-graphmatch/vflib-2.0/inc/vf_mono_state.h
   src-graphmatch/vflib-2.0/inc/vf_state.h
   src-graphmatch/vflib-2.0/inc/vf_sub_state.h
   src-graphmatch/vflib-2.0/inc/vf2_mono_state.h
   src-graphmatch/vflib-2.0/inc/vf2_state.h
   src-graphmatch/vflib-2.0/inc/vf2_sub_state.h
   src-graphmatch/vflib-2.0/inc/xsubgraph.h
   src-graphmatch/vflib-2.0/src/argedit.cc
   src-graphmatch/vflib-2.0/src/argloader.cc
   src-graphmatch/vflib-2.0/src/argraph.cc
   src-graphmatch/vflib-2.0/src/error.cc
   src-graphmatch/vflib-2.0/src/gene.cc
   src-graphmatch/vflib-2.0/src/gene_mesh.cc
   src-graphmatch/vflib-2.0/src/match.cc
   src-graphmatch/vflib-2.0/src/sd_state.cc
   src-graphmatch/vflib-2.0/src/sortnodes.cc
   src-graphmatch/vflib-2.0/src/sortnodes.h
   src-graphmatch/vflib-2.0/src/ull_state.cc
   src-graphmatch/vflib-2.0/src/ull_sub_state.cc
   src-graphmatch/vflib-2.0/src/vf_mono_state.cc
   src-graphmatch/vflib-2.0/src/vf_state.cc
   src-graphmatch/vflib-2.0/src/vf_sub_state.cc
   src-graphmatch/vflib-2.0/src/vf2_mono_state.cc
   src-graphmatch/vflib-2.0/src/vf2_state.cc
   src-graphmatch/vflib-2.0/src/vf2_sub_state.cc
   src-graphmatch/vflib-2.0/src/xsubgraph.cc
)

set (SRC_GRAPHMATCH
   ${SRC_VFLIB2}
   src-graphmatch/graphmatch.cpp
)

set (SRC_GSPAN
   src-gspan/dfs.cpp
   src-gspan/graph.cpp
   src-gspan/gspan.cpp
   src-gspan/gspan.h
   src-gspan/ismin.cpp
   src-gspan/main.cpp
   src-gspan/mexgspan.cpp
   src-gspan/misc.cpp
)

set (SRC_MEX_REPLACEMENT
   src-my-mex/mex.h
)

project(gboost)

add_executable(gboost
   ${SRC_GRAPHMATCH}
   ${SRC_GSPAN}
   ${SRC_MEX_REPLACEMENT}
)

include_directories(gboost
   src-graphmatch/vflib-2.0/inc/
   src-graphmatch/
   src-gspan/
   src-my-mex/
)

set_target_properties(gboost PROPERTIES COMPILE_OPTIONS "-Wall" "--std=c++11" "-g")

