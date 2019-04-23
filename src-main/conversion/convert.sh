

PY_EXE=python # 'python' for python 2, 'py' for python 3+
METHOD=smop # smop, ompc


this_dir=$(pwd)
cd ../original-m


if [[ $METHOD == 'smop' ]]; then
   echo smop *.m
   smop *.m > /dev/null 2>&1 # Convert matlab to python
   $PY_EXE ../conversion/post_smop.py *.py # Some additional changes are necessary

elif [[ $METHOD == 'ompc' ]]; then
   for mpath in *.m; do
      echo "$PY_EXE ../../ompc/examples/translate.py $mpath > $(basename $mpath .m).py"
      $PY_EXE ../../ompc/examples/translate.py $mpath > $(basename $mpath .m).py #2> /dev/null
      # $PY_EXE ../../ompc/ompc/ompcply.py $mpath > $(basename $mpath .m).py #2> /dev/null
   done
fi

# Move 
mv *.py ../
cd ../

echo "Done!"
