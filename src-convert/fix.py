

from collections import OrderedDict
import json
import os
import re
import sys


class Changes(object):
   """
      BRIEF  A collection of to-from replacements
   """
   SETTINGS_DIR='../../src-convert/settings' # working dir is build/temp
   
   def __init__(self, top_key = 'common', path = 'common'):
      """
         BRIEF  These files may need some work...
      """
      self.prefix  = []
      self.replace = OrderedDict()
      self.suffix  = []
      self.regex   = OrderedDict()
      
      fname = os.path.basename(path)
      if not fname.endswith('.json'):
         fname = os.path.splitext(fname)[0] + '.json'
         
      this_path = os.path.join(Changes.SETTINGS_DIR, fname)
      
      if os.path.isfile(this_path):
         with open(this_path, 'r') as f:
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
                  
                  
class File(object):
   """
      BRIEF  This class represents the file we are modifying
   """
   
   def __init__(self, path):
      """
         BRIEF  Save the path and file contents
      """
      self.path = path
      with open(self.path, 'r') as f:
         self.contents = f.read()
         
   def Change(self, pre_post, specific_method):
      """
         BRIEF  Replace file contents
      """
      for method in ['common', specific_method]:
         for fpath in ['common', self.path]:
            changes = Changes(pre_post + ' ' + method, fpath)
            
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
   print(os.getcwd())
   for path in sys.argv[3:]:
      File(path).Change(sys.argv[1], sys.argv[2]).Write()
      
      