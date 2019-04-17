
this_dir=$(pwd)

# Convert matlab to python
cd ../original-m
smop *.m > /dev/null 2>&1

# Some additional changes are necessary
python ../conversion/post_smop.py *.py

# Move 
mv *.py ../
cd ../

echo "Done!"
