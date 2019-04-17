

import os
import sys


class PyFile(object):
   """
      BRIEF  This class represents the python file we are modifying
   """
   
   def __init__(self, path):
      """
         BRIEF  Save the path and file contents
      """
      self.path = path
      with open(self.path, 'r') as f:
         self.contents = f.read()
         
   def Replace(self, before, after):
      """
         BRIEF  Replace file contents
      """
      self.contents = self.contents.replace(before, after)
      return self
      
   def Write(self):
      """
         BRIEF  Write the file contents
      """
      with open(self.path, 'w') as f:
         f.write(self.contents)
      return self
      
      
def ProcessCommon(fpath):
   """
      BRIEF  Personal preference - 3 space indent
   """
   PyFile(fpath).Replace('    ', '   ').Replace('libsmop', 'smop.libsmop').Write()
   
   
def ProcessExampleFile(fpath):
   """
      BRIEF  Had to remove the dash and extension for smop
   """
   PyFile(fpath).Replace('example_graphs', 'example-graphs.mat').Replace('   ', '').Write()
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   for fpath in sys.argv[1:]:
      ProcessCommon(fpath)
      if fpath == 'example.py':
         ProcessExampleFile(fpath)
         
         