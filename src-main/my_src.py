

import scipy.io as sio
import sys


def my_load(fpath, vars):
   """
   """
   print(type(sio.loadmat(fpath)))
   for name, value in sio.loadmat(fpath).items():
      if not name.startswith('__') and not name.endswith('__'):
         vars[name] = value
         
         
def my_disp(*args):
   """
      BRIEF  Print then force flush
   """
   print(' '.join(args))
   sys.stdout.flush()
   
   
my_disp("Loading smop ...")
from smop.libsmop import *
my_disp("... Finished loading smop")