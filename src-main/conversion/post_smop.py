
import os
import sys


class Replacements(list):
   """
   """
   COMMON_BASENAME = 'common'
   REPLACE_EXT  = '.txt'
   DELIM = ';'
   
   def __init__(self, pypath):
      """
      """
      base_path, py_ext = os.path.splitext(pypath)
      common_path = Replacements.COMMON_BASENAME + Replacements.REPLACE_EXT
      this_path = base_path + Replacements.REPLACE_EXT
      for path in [common_path, this_path]:
         if os.path.isfile(path):
            self._Read(path)
            
   def _Read(self, path):
      """
      """
      with open(path, 'r') as f:
         for line in f:
            if Replacements.DELIM in line:
               before, after = line.split(Replacements.DELIM)
               if before.strip():
                  before = before.strip()
               if after.strip():
                  after = after.strip()
               self.append((before, after.rstrip('\r\n')))
               
               
class PyFile(object):
   """
      BRIEF  This class represents the python file we are modifying
   """
   
   def __init__(self, pypath):
      """
         BRIEF  Save the path and file contents
      """
      self.path = pypath
      with open(self.path, 'r') as f:
         self.contents = f.read()
         
   def Replace(self):
      """
         BRIEF  Replace file contents
      """
      for before, after in Replacements(self.path):
         self.contents = self.contents.replace(before, after)
      return self
      
   def Write(self):
      """
         BRIEF  Write the file contents
      """
      with open(self.path, 'w') as f:
         f.write(self.contents)
      return self
      
      
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   for pypath in sys.argv[1:]:
      PyFile(pypath).Replace().Write()
      
      