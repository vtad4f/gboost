

#pragma once

#include "mex/mex.h" // from ompc

#include <iostream>
#include <cassert>


typedef uint32_t uint32_T;

template <class... T>
inline void mexPrintf(const char*, T... args);
inline void mxSetField(const mxArray*, int, const std::string&, const mxArray*);
inline mxArray* mxGetField(const mxArray*, int, const std::string&);
inline mxArray* mxCreateStructMatrix(int, int, int, const char**);
inline mxArray* mxCreateNumericMatrix(int, int, int, int);
inline mxArray* mxCreateDoubleScalar(int);
inline mxArray* mxCreateCellMatrix(int, int);
inline bool mxIsUint32(const mxArray*);
inline bool mxIsStruct(const mxArray*);
inline bool mxIsCell(const mxArray*);
inline void mxSetCell(const mxArray*, int, const mxArray*);

////////////////////////////////////////////////////////////////////////////////
//
// @brief   Print the output message
//
////////////////////////////////////////////////////////////////////////////////
template <class... T>
void mexPrintf(const char* msg, T... args)
{
   std::cout << msg << std::endl; // TODO - include args in message
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mxSetField(const mxArray*, int, const std::string&, const mxArray*)
{
   std::cout << "mxSetField - TODO Implement" << std::endl;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxGetField(const mxArray*, int, const std::string&)
{
   std::cout << "mxGetField - TODO Implement" << std::endl;
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateStructMatrix(int, int, int, const char**)
{
   std::cout << "mxCreateStructMatrix - TODO Implement" << std::endl;
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateNumericMatrix(int, int, int, int)
{
   std::cout << "mxCreateNumericMatrix - TODO Implement" << std::endl;
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateDoubleScalar(int)
{
   std::cout << "mxCreateDoubleScalar - TODO Implement" << std::endl;
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateCellMatrix(int, int)
{
   std::cout << "mxCreateCellMatrix - TODO Implement" << std::endl;
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsUint32(const mxArray* pArray)
{
   std::cout << "mxIsUint32 - TODO Implement" << std::endl;
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsStruct(const mxArray* pArray)
{
   std::cout << "mxIsUint32 - TODO Implement" << std::endl;
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsCell(const mxArray* pArray)
{
   std::cout << "mxIsUint32 - TODO Implement" << std::endl;
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mxSetCell(const mxArray*, int, const mxArray*)
{
   std::cout << "mxSetCell - TODO Implement" << std::endl;
}

