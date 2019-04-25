

from py2or3 import *
import scipy.io as sio
import sys


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
   
   
def my_sort(numpy_ndarray, x, descr): # TODO - does x matter?
   """
      https://stackoverflow.com/questions/28512237/python-equivalent-to-matlab-a-b-sorty
      https://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
      
      Using mergesort b/c it is clean
   """
   # print(numpy_ndarray)
   cpy = numpy_ndarray.copy()
   if descr == 'ascend':
      cpy.sort(kind='mergesort') # TODO - need to specify axis?
   elif descr == 'descend':
      cpy[::-1].sort(kind='mergesort') # TODO - argsort if descending?
   else:
      raise ValueError(descr)
   # print(cpy)
   return cpy, None
   
   
def my_norm(*args):
   """
   """
   # TODO - implement
   
   
def my_concat(*args):
   """
   """
   # TODO - implement
   
   
   
   
   