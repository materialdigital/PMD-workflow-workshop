#!/bin/bash
# conda install papermill
conda install -c conda-forge papermill

# execute notebooks
current_dir=$(pwd)
i=0;
for dir in $current_dir/*/ ; do 
    for f in $(find $dir -name *.ipynb | sort -n); do
        cd $dir;
        notebook=$(basename $f);
        papermill ${notebook} ${notebook%.*}-out.${notebook##*.} -k "python3" || i=$((i+1));
        cd $current_dir;
    done;
done;

# push error to next level
if [ $i -gt 0 ]; then
    exit 1;
fi;
