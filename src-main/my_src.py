

from py2or3 import *
import scipy.io as sio
import sys


################################################################################
#
#  RENAME
#
################################################################################

def my_product(*args):
   """
      BRIEF  Multiply matrices or scalars or a combination
   """
   if len(args) == 1:
      return args[0]
   
   raise Exception("TODO - Implement")
   
   
def my_arg_reader(*args, **kwargs):
   """
      BRIEF  Analyze the args and return values
   """
   nargin = sum([arg is not None for arg in args])
   nargout = kwargs['nargout'] if 'nargout' in kwargs else None
   return nargin, nargout
   
   
def my_isempty(thing):
   """
      BRIEF  If it is an array, check the length
             If it is an optional argument, it may be None
   """
   try:
      iter(thing)
      return len(thing) == 0
   except TypeError:
      return thing is None
      
      
def my_size(np_array, dim):
   """
      BRIEF  The dimension parameter is 1-based in matlab, but 0-based in numpy
   
             https://stackoverflow.com/questions/19389910/in-python-numpy-what-is-a-dimension-and-axis
             https://www.mathworks.com/help/matlab/math/multidimensional-arrays.html
   """
   if my_isempty(np_array):
      return 0
   nrows, ncols = np_array.shape if np_array.ndim > 1 else (1, np_array.shape[0])
   if dim == 1:
      return nrows
   elif dim == 2:
      return ncols
   else:
      return np_array.shape[dim - 1]
      
      
################################################################################
#
#  RENAME and SMOP
#
################################################################################

def my_load(fpath, vars):
   """
      BRIEF  Load a .mat file into the dict
   """
   for name, value in sio.loadmat(fpath).items():
      if not name.startswith('__') and not name.endswith('__'):
         vars[name] = value
         
         
def my_pause():
   """
      BRIEF  Wait for user input
   """
   # Input() # TODO - uncomment in final revision
   
   
def my_sort(np_array, n, descr, nargout): # TODO - does n matter?
   """
      https://stackoverflow.com/questions/28512237/python-equivalent-to-matlab-a-b-sorty
      https://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
      
      Using mergesort b/c it is clean
      
      TODO - Haven't tested this!
   """
   cpy = np_array.copy()
   if nargout == 2:
      # print(np_array)
      if descr == 'ascend':
         cpy.sort(kind='mergesort') # TODO - need to specify axis?
      elif descr == 'descend':
         cpy[::-1].sort(kind='mergesort') # TODO - argsort if descending?
      else:
         raise ValueError(descr)
      # print(cpy)
      return cpy, None # TODO - numpy argsort
      
      
################################################################################
#
#  SMOP only
#
################################################################################

def my_disp(*args):
   """
      BRIEF  Print then force flush
   """
   print(' '.join(args))
   sys.stdout.flush()
   
   
def my_norm(*args):
   """
   """
   # TODO - implement
   
   
def my_concat(*args):
   """
   """
   # TODO - implement
   
   
   
   
   