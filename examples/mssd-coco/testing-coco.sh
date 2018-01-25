#cd $HOME/caffe
./build/tools/caffe train \
--solver="examples/mssd-coco/test_solver.prototxt" \
--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCOVOC_msra_iter_190000.caffemodel" \
-gpu 0 2>&1 | tee "examples/mssd-coco/logs/testing_$(date +%y-%m-%d_%H:%M:%S).log"
#--model="examples/mssd-coco/MobileNet_test_coco.prototxt" \
#--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_VOC_iter_12000.caffemodel"
# --weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCO_iter_400000.caffemodel" \
