#bash/bin/bash
#cd $HOME/caffe


# # DON'T use tee see https://github.com/BVLC/caffe/issues/5323
# ./build/tools/caffe train \
# --weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-3_2_iter_18000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_coco.prototxt" \
# --gpu=0 > "examples/mssd-coco/logs/training_coco_$(date +%y-%m-%d_%H:%M:%S).log" 2>&1 # Y: 4 digits year
# # --weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-3_iter_80000.caffemodel" \
# #--weights="examples/mssd-coco/models/mobilenet.caffemodel" \
# #--gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_$(date +%Y%m%d%H%M%S).log"

# Resume
./build/tools/caffe train \
--solver="examples/mssd-coco/train_solver_coco.prototxt" \
-snapshot "examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_iter_30000.solverstate" \
> "examples/mssd-coco/logs/training_coco_$(date +%y-%m-%d_%H:%M:%S).log" 2>&1 

# ./build/tools/caffe train \
# --weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-3_iter_80000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_coco_LR1E-4.prototxt" \
# --gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_coco_LR1E-4.log"

# ./build/tools/caffe train \
# --weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-4_iter_20000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_coco_LR1E-5.prototxt" \
# --gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_coco_LR1E-5.log"


# ./build/tools/caffe train \
# --weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_LR1E-4_3_iter_100000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_voc0712_LR1E-4.prototxt" \
# --gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_voc0712_LR1E-4_$(date +%y-%m-%d_%H:%M:%S).log"
# #--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_LR1E-4_2_iter_80000.caffemodel" \
# #--weights="examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-5_iter_20000.caffemodel" \
# #--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_LR1E-4_iter_20000.caffemodel" \

# ./build/tools/caffe train \
# --weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_LR1E-5_1_iter_80000.caffemodel" \
# --solver="examples/mssd-coco/train_solver_voc0712_LR1E-5.prototxt" \
# --gpu=0 2>&1 | tee "examples/mssd-coco/logs/training_voc0712_LR1E-5_$(date +%y-%m-%d_%H:%M:%S).log"
# #--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_LR1E-4_4_iter_100000.caffemodel" \
