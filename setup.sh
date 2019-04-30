

################################################################################
#
#  @brief  Return true if the OS is linux, else false (e.g. cygwin = false)
#
################################################################################
function _OsIsLinux
{
   if [ "$(uname)" == "Linux" ]; then return 0 ; else return 1 ; fi
}


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
   $py_exe "$@" ; return $?
}


################################################################################
#
#  @brief  If the python version is 3 return true, else false
#
################################################################################
function _IsPy3
{
   local major_ver
   major_ver=$(_RunPyExe --version | cut -d ' ' -f 2 | cut -d '.' -f 1)
   if [[ "$major_ver" == "3" ]]; then return 0 ; else return 1 ; fi
}


################################################################################
#
#  @brief  Return true if the package is already installed, else false
#
################################################################################
function _Importable
{
   _RunPyExe -c "import $1" 2> /dev/null
   return $?
}


################################################################################
#
#  @brief  Import the python module
#
################################################################################
function _PipInstall
{
   if ! _Importable "$1" ; then
      echo "$(_GetPyExe) -m pip install $1"
      _RunPyExe -m pip install $1
   fi
}


################################################################################
#
#  @brief  Is the argument $1 a yes or a no?
#
################################################################################
function _EvalYesNo
{
   case "$1" in
      y|Y|yes|Yes|YES) return 0 ;; # true
      n|N|no|No|NO)    return 1 ;;
      *)               return 1 ;; # {Enter} means no
   esac
}


################################################################################
#
#  @brief  Confirm an action with user, then echo yes/no
#
################################################################################
function _Confirm
{
   local action_
   local choice_
   
   [[ $# == 0 ]] && action_="Continue" || action_="$@"
   
   builtin read -p "$action_ (y/n)? " choice_
   _EvalYesNo "$choice_"
   return $?
}


################################################################################
#
#  @brief  Check for a y/n value in the arg $1
#          If we don't find one, ask for it with the specified message $2
#
################################################################################
function _EvalArg
{
   _EvalYesNo "$1" && return 0 # true - evaluated to 'yes'
   [[ ! -z "$1" ]] && return 1 # actually evaluated to 'no'
   _Confirm "$2"               # else ask the user
   return $?
}


################################################################################
#
#  @brief  Main execution
#
################################################################################
! _OsIsLinux && echo "Linux is required for pycvx to install" && exit 1
! _IsPy3 && echo "Python 3 is required for the @ operator" && exit 2
_PipInstall smop
_PipInstall matplotlib
_PipInstall cvxpy
_EvalArg "$1" "make" && make
_EvalArg "$2" "run" && cd src-main && _RunPyExe example.py

