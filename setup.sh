

################################################################################
#
#  @brief  Import the python module if not already installed
#
################################################################################
function import()
{
   py -c "import $1"
   if [[ $? -gt 0 ]]; then
      echo "py -m pip install $1"
      py -m pip install $1
   fi
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
   case "$choice_" in
      y|Y|yes|Yes|YES) return 0 ;; # true
      n|N|no|No|NO)    return 1 ;;
      *)               return 1 ;; # {Enter} means no
   esac
}

################################################################################
#
#  @brief  Main execution
#
################################################################################
import smop
_Confirm "make" && make
_Confirm "run" && cd src-main && python example.py && cd -

