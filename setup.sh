

PY_EXE=python # 'python' for python 2, 'py' for python 3+


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
#  @brief  Return true if the package is already installed, else false
#
################################################################################
function _Importable
{
   $PY_EXE -c "import $1" 2> /dev/null
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
      echo "$PY_EXE -m pip install $1"
      $PY_EXE -m pip install $1
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
_PipInstall smop
_PipInstall matplotlib
_OsIsLinux && _PipInstall cvxpy # TODO - vs140 dependency on windows...
_EvalArg "$1" "make" && make
_EvalArg "$2" "run" && cd src-main && $PY_EXE example.py

