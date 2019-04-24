

################################################################################
#
#  @brief  Print the cmd then execute it
#
################################################################################
function _PrintRun
{
   echo "$@"
   "$@"
   return $?
}


# Settings
PY_EXE=python # 'python' for python 2, 'py' for python 3+
METHOD=smop # rename, smop, ompc

# Move to the dir containing the m files
_PrintRun cd original-m

# Move copies of the files
temp_dir=../../build/temp
_PrintRun mkdir -p $temp_dir
for mpath in *.m; do
   _PrintRun cp $mpath $temp_dir
done
_PrintRun cd $temp_dir

# Pre processing
_PrintRun $PY_EXE ../../src-convert/fix.py pre $METHOD *.m # Additional changes are necessary

# Convert the files
if [[ $METHOD == 'rename' ]]; then
   for mpath in *.m; do
      pypath=$(basename $mpath .m).py
      _PrintRun mv $mpath $pypath
   done
   
elif [[ $METHOD == 'smop' ]]; then
   _PrintRun smop *.m > /dev/null 2>&1 # Convert m to python
   
elif [[ $METHOD == 'ompc' ]]; then
   for mpath in *.m; do
      pypath=$(basename $mpath .m).py
      ompc_dir=../../ompc/
      _PrintRun $PY_EXE $ompc_dir/examples/translate.py $mpath > $pypath #2> /dev/null
      # _PrintRun $PY_EXE $ompc_dir/ompc/ompcply.py $mpath > $pypath #2> /dev/null
   done
fi

# Post processing
_PrintRun $PY_EXE ../../src-convert/fix.py post $METHOD *.py # Additional changes are necessary

# Move the files
_PrintRun mv *.py ../../src-main/
echo "Done!"

