# 
#cd $HOME/caffe
./build/tools/caffe train \
--weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_iter_160000.caffemodel" \
--solver="examples/mssd-coco/train_solver_coco_LR1E-4.prototxt" \
--gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_$(date +%Y%m%d%H%M%S).log"
