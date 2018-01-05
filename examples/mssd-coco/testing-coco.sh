cd $HOME/caffe
./build/tools/caffe train \
--model="examples/mssd-coco/MobileNet_test.prototxt" \
--solver="examples/mssd-coco/test_solver.prototxt" \
--weights="examples/mssd-coco/MobileNet_SSD_320x320_VOC_iter_160000.caffemodel" \
--gpu=0 2>&1 | tee "examples/mssd-coco/logs/testing_$(date +%Y%m%d%H%M%S).log"
