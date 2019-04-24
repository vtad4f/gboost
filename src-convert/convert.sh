

PY_EXE=python # 'python' for python 2, 'py' for python 3+
METHOD=smop # rename, smop, ompc


# Move to the dir containing the m files
this_dir=$(pwd)
cd ../original-m

# Convert the files
if [[ $METHOD == 'rename' ]]; then
   for mpath in *.m; do
      cp $mpath $(basename $mpath .m).py
   done
   
elif [[ $METHOD == 'smop' ]]; then
   echo smop *.m
   smop *.m > /dev/null 2>&1 # Convert m to python
   
elif [[ $METHOD == 'ompc' ]]; then
   for mpath in *.m; do
      echo "$PY_EXE ../../ompc/examples/translate.py $mpath > $(basename $mpath .m).py"
      $PY_EXE ../../ompc/examples/translate.py $mpath > $(basename $mpath .m).py #2> /dev/null
      # $PY_EXE ../../ompc/ompc/ompcply.py $mpath > $(basename $mpath .m).py #2> /dev/null
   done
fi

# Post processing
$PY_EXE ../conversion/post.py $METHOD *.py # Some additional changes are necessary

# Move 
mv *.py ../
cd ../

echo "Done!"
