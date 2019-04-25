

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
      self.prefix            = []
      self.replace           = OrderedDict()
      self.suffix            = []
      self.single_line_regex = OrderedDict()
      self.multi_line_regex  = OrderedDict()
      self.function          = None
      
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
               
            if 'single-line-regex' in content:
               for pattern, replacement in content['single-line-regex'].items():
                  self.single_line_regex[re.compile(pattern)] = replacement
                  
            if 'multi-line-regex' in content:
               for pattern, replacement in content['multi-line-regex'].items():
                  self.multi_line_regex[re.compile(pattern, re.MULTILINE)] = replacement
                  
            if 'fix-functions' in content:
               if content['fix-functions'] == "true":
                  self.function = re.compile(r"function \[([^\]]+)\] = ")
                  
                  
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
            
            # 1. Replace
            for before, after in changes.replace.items():
               self.contents = self.contents.replace(before, after)
               
            # 2. Multi-line regex
            for regex, after in changes.multi_line_regex.items():
               self.contents = regex.sub(after, self.contents) # TODO - format
               
            # 3. Single-line regex w/ substitution
            lines = self.contents.split('\n')
            for regex, after in changes.single_line_regex.items():
               for i, line in enumerate(lines):
                  matches = regex.findall(line)
                  if matches:
                     if isinstance(matches[0], tuple):
                        matches = matches[0]
                     try:
                        lines[i] = regex.sub(after.format(*matches), line)
                     except Exception as e:
                        print(str(e) + ': ' + regex.pattern + ' @ ' + line)
                        
            # 4. Replace matlab function with python function
            if changes.function:
               pending_ret = []
               empty_line = None
               for i, line in enumerate(lines):
                  
                  matches = changes.function.findall(line)
                  if matches:
                     lines[i] = 'def' + line.split('=')[1] + ':'
                     if pending_ret:
                        lines[empty_line] = '   return ' + pending_ret
                     pending_ret = matches[0]
                  elif pending_ret:
                     lines[i] = '   ' + line
                     
                  if line.strip():
                     empty_line = None
                  elif empty_line is None:
                     empty_line = i
                     
               if pending_ret:
                  lines[empty_line] = '   return ' + pending_ret
                  
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
   for path in sys.argv[3:]:
      File(path).Change(sys.argv[1], sys.argv[2]).Write()
      
      