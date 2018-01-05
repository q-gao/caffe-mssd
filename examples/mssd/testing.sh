cd $HOME/caffe
./build/tools/caffe train \
--model="examples/mssd/MobileNet_test.prototxt" \
--solver="examples/mssd/test_solver.prototxt" \
--weights="examples/mssd/MobileNet_SSD_320x320_VOC_iter_160000.caffemodel" \
--gpu=0 2>&1 | tee "examples/mssd/logs/testing_$(date +%Y%m%d%H%M%S).log"
