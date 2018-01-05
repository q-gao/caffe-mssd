#!/bin/bash
# This script takes the following inputs:
#   $voc_root_dir/$name/$sub_dir/$dataset.txt (e.g., VOCdevkit/VOC2007/ImageSets/Main)
#
# and creates the following files:
#   <script_folder>/$dataset.txt
#   <script_folder>/test_name_size.txt if $dataset == 'test'
#
# An example line in $dataset.txt (note 'JPEGImages' and 'Annotatopms' are hard-coded):
#  VOC2007/JPEGImages/000001.jpg VOC2007/Annotations/000001.xml
#
# NOTE:
#  - if $dataset == 'trainval', <script_folder>/trainval.txt is shuffled!

voc_root_dir=/local/mnt/workspace/qgao/VOCData/VOCdevkit/
sub_dir=ImageSets/Main

# gets the script's source file pathname, strips it to just the path portion, 
# cds to that path, 
# then uses pwd to return the (effectively) full path of the script
bash_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for dataset in trainval test
do
  dst_file=$bash_dir/$dataset.txt
  if [ -f $dst_file ]
  then
    rm -f $dst_file
  fi
  for name in VOC2007 VOC2012
  do
    if [[ $dataset == "test" && $name == "VOC2012" ]]
    then
      continue
    fi
    echo "Create list for $name $dataset..."
    dataset_file=$voc_root_dir/$name/$sub_dir/$dataset.txt

    img_file=$bash_dir/$dataset"_img.txt"
    cp $dataset_file $img_file
    sed -i "s/^/$name\/JPEGImages\//g" $img_file
    sed -i "s/$/.jpg/g" $img_file

    label_file=$bash_dir/$dataset"_label.txt"
    cp $dataset_file $label_file
    sed -i "s/^/$name\/Annotations\//g" $label_file
    sed -i "s/$/.xml/g" $label_file

    paste -d' ' $img_file $label_file >> $dst_file

    rm -f $label_file
    rm -f $img_file
  done

  # Generate image name and size infomation.
  if [ $dataset == "test" ]
  then
    $bash_dir/../../build/tools/get_image_size $voc_root_dir $dst_file $bash_dir/$dataset"_name_size.txt"
  fi

  # Shuffle trainval file.
  if [ $dataset == "trainval" ]
  then
    rand_file=$dst_file.random
    cat $dst_file | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > $rand_file
    mv $rand_file $dst_file
  fi
done
