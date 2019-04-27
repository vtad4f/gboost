

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
   
   
################################################################################
#
#  RENAME and SMOP
#
################################################################################

def my_load(fpath, vars):
   """
      BRIEF  Load a .mat file
   """
   for name, value in sio.loadmat(fpath).items():
      if not name.startswith('__') and not name.endswith('__'):
         vars[name] = value
         
         
def my_pause():
   """
      BRIEF  Wait for user input
   """
   # Input() # TODO - uncomment in final revision
   
   
def my_sort(numpy_ndarray, n, descr, nargout): # TODO - does n matter?
   """
      https://stackoverflow.com/questions/28512237/python-equivalent-to-matlab-a-b-sorty
      https://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
      
      Using mergesort b/c it is clean
      
      TODO - haven't tested this method!
   """
   cpy = numpy_ndarray.copy()
   if nargout == 2:
      # print(numpy_ndarray)
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
   
   
   
   
   