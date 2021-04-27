#!/bin/bash
current_dir=$(pwd)
cp -r pyiron $current_dir
cp .github/ci_support/pyironconfig.py $current_dir
# pyiron config 
python pyironconfig.py

# conda install papermill
conda install -c conda-forge papermill

# execute notebooks
exercise_dir=$current_dir/exercise_notebooks/
i=0;
for dir in $current_dir/*/ ; do 
    if [ $dir != $exercise_dir ] ; then
        for f in $(find $dir -name *.ipynb | sort -n); do
            cd $dir;
            notebook=$(basename $f);
            papermill ${notebook} ${notebook%.*}-out.${notebook##*.} -k "python3" || i=$((i+1));
            cd $current_dir;
        done;
    fi
done;

# push error to next level
if [ $i -gt 0 ]; then
    exit 1;
fi;
