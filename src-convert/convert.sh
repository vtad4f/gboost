

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

PY_EXE=python # 'python' for python 2, 'py' for python 3+
METHOD=smop # rename, smop, ompc


# Move to the dir containing the m files
_PrintRun cd original-m

# Convert the files
if [[ $METHOD == 'rename' ]]; then
   for mpath in *.m; do
      _PrintRun cp $mpath $(basename $mpath .m).py
   done
   
elif [[ $METHOD == 'smop' ]]; then
   _PrintRun smop *.m > /dev/null 2>&1 # Convert m to python
   
elif [[ $METHOD == 'ompc' ]]; then
   for mpath in *.m; do
      _PrintRun $PY_EXE ../../ompc/examples/translate.py $mpath > $(basename $mpath .m).py #2> /dev/null
      # _PrintRun $PY_EXE ../../ompc/ompc/ompcply.py $mpath > $(basename $mpath .m).py #2> /dev/null
   done
fi

# Post processing
_PrintRun $PY_EXE ../post.py post $METHOD *.py # Some additional changes are necessary

# Move the files
_PrintRun mv *.py ../../src-main/
echo "Done!"

