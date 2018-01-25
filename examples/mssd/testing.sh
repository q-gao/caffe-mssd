#cd $HOME/caffe
./build/tools/caffe train \
--solver="examples/mssd/test_solver.prototxt" \
--weights="examples/mssd/MobileNet_SSD_320x320_VOC_iter_120000.caffemodel" \
--gpu=0 2>&1 | tee "examples/mssd/logs/testing_$(date +%y-%m-%d_%H:%M:%S).log"
#--model="examples/mssd/MobileNet_test.prototxt" \
#--weights="examples/mssd/MobileNet_SSD_320x320_VOC_iter_160000.caffemodel" \