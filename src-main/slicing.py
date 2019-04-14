

def SetRange(array2d, row_str, col_str, new_values)
   """
      @brief  Set the specified rows and cols in the array,
              where the array2d is something like: [ [ x, y, z ],
                                                     [ a, b, c ] ]
   """
   for row_i in range(*InterpretSliceStr(row_str, GetNumRows(row_str))):
      for col_i in range(*InterpretSliceStr(col_str, GetNumCols(col_str))):
         array2d[row_i][col_i] = new_values[row_i][col_i]
         
         
def GetRange(array2d, row_str, col_str):
   """
      @brief  Get the specified rows and cols from the array,
              where the array2d is something like: [ [ x, y, z ],
                                                     [ a, b, c ] ]
   """
   new_array = []
   for row_i in range(*InterpretSliceStr(row_str, GetNumRows(row_str))):
      new_row = []
      for col_i in range(*InterpretSliceStr(col_str, GetNumCols(col_str))):
         new_row.append(array2d[row_i][col_i])
      new_array.append(new_row)
   return new_array
   
   
def GetNumRows(array2d):
   """
   """
   return len(array2d)
   
   
def GetNumCols(array2d):
   """
   """
   return 0 if not array2d else len(array2d[0])
   
   
def InterpretSliceStr(string, max_end_i):
   """
   """
   if isinstance(string, str) and ':' in string:
      min_n, max_n = string.split(':') # Doesn't cover case with two colons
      start_i = (int(min_n) - 1) if min_n else 0
      end_i = int(max_n) if max_n else max_end_i
   else:
      start_i = end_i = int(string) - 1
      
   return start_i, end_i
   
   