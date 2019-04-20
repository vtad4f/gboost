

from collections import OrderedDict
import json
import os
import sys


class Changes(object):
   """
      BRIEF  A collection of to-from replacements
   """
   
   def __init__(self, path = 'common.json'):
      """
         BRIEF  These files translated from smop may need some work...
      """
      content = OrderedDict()
      
      if not path.endswith('.json'):
         path = os.path.splitext(path)[0] + '.json'
         
      if os.path.isfile(path):
         with open(path, 'r') as f:
            content = json.load(f, object_pairs_hook=OrderedDict)
            
      self.prefix  = content['prefix']  if 'prefix'  in content else []
      self.replace = content['replace'] if 'replace' in content else OrderedDict()
      self.suffix  = content['suffix']  if 'suffix'  in content else []
      
      
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
         
   def Change(self):
      """
         BRIEF  Replace file contents
      """
      for changes in [Changes(), Changes(self.path)]:
         for before, after in changes.replace.items():
            self.contents = self.contents.replace(before, after)
         self.contents = '\n'.join(changes.prefix + [self.contents] + changes.suffix)
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
      PyFile(pypath).Change().Write()
      
      