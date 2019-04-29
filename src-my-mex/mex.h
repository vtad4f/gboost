

#pragma once

#include "mex/mex.h" // from ompc

#include <cassert>
#include <string>
// #include <vector>


typedef uint32_t uint32_T;
// struct Elem
// {
   
// };
// typedef std::vector<Elem> mxArray;

// enum SomeType
// {
   // mxUINT32_CLASS,
   // mxREAL,
   // mxDOUBLE_CLASS
// };

template <class... T>
inline void mexPrintf(const std::string&, T... args);
inline void mexErrMsgTxt(const std::string&);
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
inline void mxDestroyArray(const mxArray*);
// inline uint32_t* mxGetPr(const mxArray *);
// inline unsigned int mxGetScalar(const mxArray *);
// inline unsigned int mxGetM(const mxArray *);
// inline unsigned int mxGetN(const mxArray *);

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
template <class... T>
void mexPrintf(const std::string&, T... args)
{

}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mexErrMsgTxt(const std::string&)
{
   
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mxSetField(const mxArray*, int, const std::string&, const mxArray*)
{
   
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxGetField(const mxArray*, int, const std::string&)
{
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateStructMatrix(int, int, int, const char**)
{
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateNumericMatrix(int, int, int, int)
{
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateDoubleScalar(int)
{
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
mxArray* mxCreateCellMatrix(int, int)
{
   return new mxArray;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsUint32(const mxArray*)
{
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsStruct(const mxArray*)
{
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
bool mxIsCell(const mxArray*)
{
   return false;
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mxSetCell(const mxArray*, int, const mxArray*)
{
   
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
void mxDestroyArray(const mxArray*)
{
   
}

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
// uint32_t* mxGetPr(const mxArray *)
// {
   // return nullptr;
// }

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
// unsigned int mxGetScalar(const mxArray *)
// {
   // return 0;
// }

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
// unsigned int mxGetM(const mxArray *)
// {
   // return 0;
// }

////////////////////////////////////////////////////////////////////////////////
//
// @brief   TODO_COMMENT
//
////////////////////////////////////////////////////////////////////////////////
// unsigned int mxGetN(const mxArray *)
// {
   // return 0;
// }

