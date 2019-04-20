

from smop.libsmop import *
import sys


def my_disp(*args, **kwargs):
   """
      BRIEF  Print then force flush
   """
   disp(*args, **kwargs)
   sys.stdout.flush()
   
   