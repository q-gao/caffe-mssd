#bash/bin/bash
#cd $HOME/caffe


# # DON'T use tee see https://github.com/BVLC/caffe/issues/5323
./build/tools/caffe train \
 --weights="examples/mssd-coco/models/mobilenet.caffemodel" \
 --solver="examples/mssd-coco/train_solver_cocovoc_msra.prototxt" \
 -gpu 0,1,2,3,4,5,6,7 > "examples/mssd-coco/logs/training_cocovoc_msra_$(date +%y-%m-%d_%H:%M:%S).log" 2>&1 # Y: 4 digits year

