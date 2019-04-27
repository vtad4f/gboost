

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
      self.fix_functions     = False
      
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
               self.fix_functions = True
               if content['fix-functions']:
                  self.fix_functions = content['fix-functions']
                  
class File(object):
   """
      BRIEF  This class represents the file we are modifying
   """
   FCN_DEF = re.compile(r"function\s*\[([^\]]+)\]\s*=\s*([^(\s]+)\s*\(([^)]+)\)")
   FCN_CALL = re.compile(r"^(\s*)\[([^\]]+)\](.+)\)\s*$")
   SUB = '!!' # something not present in the file
   INDENT = '   '
   
   def __init__(self, path):
      """
         BRIEF  Save the path and file contents
      """
      self.path = path
      with open(self.path, 'r') as f:
         self.contents = f.read()
         
   def Update(self, pre_post, specific_method):
      """
         BRIEF  Update file contents
      """
      all_changes = []
      for method in ['common', specific_method]:
         for fpath in ['common', self.path]:
            all_changes.append(Changes(pre_post + ' ' + method, fpath))
            
      for changes in all_changes:
         self._Replace(changes.replace)
      for changes in all_changes:
         self._MultiLineRegex(changes.multi_line_regex)
      for changes in all_changes:
         self._SingleLineRegex(changes.single_line_regex)
      for changes in all_changes:
         self._TranslateFcnDefs(changes.fix_functions)
      for changes in all_changes:
         self._AddNargoutToFcnCalls(changes.fix_functions)
      for changes in all_changes:
         self._AddFilePrefixSuffix(changes.prefix, changes.suffix)
         
      return self
      
   def _Replace(self, before_after):
      """
         BRIEF  Good old fashoned string replacement. No commplex regex here.
      """
      for before, after in before_after.items():
         self.contents = self.contents.replace(before, after)
      
   def _MultiLineRegex(self, before_after):
      """
         BRIEF  Apply regex to the file contents as a whole
      """
      for regex, after in before_after.items():
         self.contents = regex.sub(after, self.contents)
         
   def _SingleLineRegex(self, before_after):
      """
         BRIEF  Use regex replacement one line at a time
                
                The big difference between this and the multi-line regex is
                that matches from what is replaced can be inserted into the
                replacement!
      """
      lines = self.contents.split('\n')
      for regex, after in before_after.items():
         for i in range(len(lines)):
            matches = regex.findall(lines[i])
            if matches:
               lines[i] = regex.sub(File.SUB, lines[i])
               for match in matches:
                  if not isinstance(match, tuple):
                     match = [match]
                  try:
                     lines[i] = lines[i].replace(File.SUB, after.format(*match), 1)
                  except Exception as e:
                     print(str(e) + ': ' + regex.pattern + ' #### ' + lines[i])
      self.contents = '\n'.join(lines)
      
   def _TranslateFcnDefs(self, fix_functions):
      """
         BRIEF  This was a bit too complicated for a one-line-regex in the
                settings, so a separate function was created for it
      """
      if fix_functions:
         prefixes = fix_functions['prefix'] if 'prefix' in fix_functions else OrderedDict()
         
         lines = self.contents.split('\n')
         pending_ret = ''
         empty_line = None
         for i, line in enumerate(lines):
            matches = File.FCN_DEF.findall(line)
            if matches:
               ret, name, args = matches[0]
               args_none = ', '.join(map('{0}=None'.format, args.split(', ')))
               args += ', **kwargs'
               args_none += ', **kwargs'
               prefix = prefixes[name] if name in prefixes else '' # configurable
               lines[i] = 'def {0}({1}):\n   {2}({3})\n   {4}'.format(
                  name, args_none, "nargin, nargout = my_arg_reader", args, prefix)
               if pending_ret:
                  lines[empty_line] = '   return ' + pending_ret
               pending_ret = ret
            elif pending_ret:
               lines[i] = '   ' + line
            if line.strip():
               empty_line = None
            elif empty_line is None:
               empty_line = i
         if pending_ret:
            lines[empty_line] = '   return ' + pending_ret
         self.contents = '\n'.join(lines)
      
   def _AddNargoutToFcnCalls(self, fix_functions):
      """
         BRIEF  Fix the function call; The number of returns may vary...
      """
      if fix_functions:
         lines = self.contents.split('\n')
         for i, line in enumerate(lines):
            matches = File.FCN_CALL.findall(line)
            if matches:
               space, ret, the_rest = matches[0]
               nargout = len(ret.split(','))
               lines[i] = space + ret + the_rest + ', nargout={0})'.format(nargout)
         self.contents = '\n'.join(lines)
      
   def _AddFilePrefixSuffix(self, prefixes, suffixes):
      """
         BRIEF  
      """
      self.contents = '\n'.join(prefixes + self.contents.split('\n') + suffixes)
      
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
      File(path).Update(sys.argv[1], sys.argv[2]).Write()
      
      