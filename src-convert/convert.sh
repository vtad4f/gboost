

################################################################################
#
#  @brief  Run python with the provided args
#
################################################################################
function _TypeExists { type $1 > /dev/null 2>&1 ; return $? ; }
function _GetPyExe
{
   _TypeExists py      && echo -n py      && return 0
   _TypeExists python3 && echo -n python3 && return 0
   _TypeExists python  && echo -n python  && return 0
   return 1
}
function _RunPyExe
{
   local py_exe
   py_exe=$(_GetPyExe) || return 1
   echo $(_GetPyExe) "$@"
   $py_exe "$@" ; return $?
}


################################################################################
#
#  @brief  Print the cmd then execute it
#
################################################################################
function _PrintRun { echo "$@" ; "$@" ; return $? ; }


# Settings
METHOD=rename # rename, smop, ompc

# Move to the dir containing the m files
cd original-m

# Copy the m files to the temp dir and move to it
for mpath in *.m; do
   cp $mpath ../temp
done
cd ../temp

# Pre processing
_RunPyExe ../fix.py pre $METHOD *.m # Additional changes are necessary

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
      _RunPyExe $ompc_dir/examples/translate.py $mpath > $pypath #2> /dev/null
      _RunPyExe $ompc_dir/ompc/ompcply.py $mpath > $pypath #2> /dev/null
   done
fi

# Post processing
_RunPyExe ../fix.py post $METHOD *.py # Additional changes are necessary
_PrintRun sed -i 's/\r$//' *.py # Remove \r from newlines that python adds on windows

# Move the files
for pypath in *.py; do
   _PrintRun cp $pypath ../../src-main/
done
echo "Done!"

