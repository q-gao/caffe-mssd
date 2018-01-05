# 
#cd $HOME/caffe
# ./build/tools/caffe train \
# --weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-3_2_iter_18000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_coco_msra.prototxt" \
# --gpu=0 > "examples/mssd-coco/logs/training_coco_msra_$(date +%y-%m-%d_%H:%M:%S).log" 2>&1 # Y: 4 digits year

# Resume
./build/tools/caffe train \
--solver="examples/mssd-coco/train_solver_coco_msra.prototxt" \
-snapshot "examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_msra_iter_70000.solverstate" \
> "examples/mssd-coco/logs/training_coco_msra_$(date +%y-%m-%d_%H:%M:%S).log" 2>&1 
