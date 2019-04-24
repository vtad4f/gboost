

from collections import OrderedDict
import json
import os
import re
import sys


class Changes(object):
   """
      BRIEF  A collection of to-from replacements
   """
   
   def __init__(self, top_key = 'common', path = 'common.json'):
      """
         BRIEF  These files may need some work...
      """
      self.prefix  = []
      self.replace = OrderedDict()
      self.suffix  = []
      self.regex   = OrderedDict()
      
      if not path.endswith('.json'):
         path = os.path.splitext(path)[0] + '.json'
         
      if os.path.isfile(path):
         with open(path, 'r') as f:
            entire_file = json.load(f, object_pairs_hook=OrderedDict)
            
         if top_key in entire_file:
            content = entire_file[top_key]
            
            if 'prefix'  in content:
               self.prefix = content['prefix']
               
            if 'replace' in content:
               self.replace = content['replace']
               
            if 'suffix' in content:
               self.suffix = content['suffix']
      
            if 'regex' in content:
               for pattern, replacement in content['regex'].items():
                  self.regex[re.compile(pattern)] = replacement
                  
                  
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
         
   def Change(self, method):
      """
         BRIEF  Replace file contents
      """
      for method in ['common', method]:
         for fpath in ['common', self.path]:
            changes = Changes(method, fpath)
            
            for before, after in changes.replace.items():
               self.contents = self.contents.replace(before, after)
               
            lines = self.contents.split('\n')
            for i, line in enumerate(lines):
               for regex, after in changes.regex.items():
                  lines[i] = regex.sub(after.format(regex.findall(line)), line)
                  
            self.contents = '\n'.join(changes.prefix + lines + changes.suffix)
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
   for pypath in sys.argv[2:]:
      PyFile(pypath).Change(sys.argv[1]).Write()
      
      