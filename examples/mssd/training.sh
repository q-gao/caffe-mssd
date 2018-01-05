#cd $HOME/caffe
./build/tools/caffe train \
--weights="examples/mssd/MobileNet_SSD_320x320_VOC_iter_120000.caffemodel" \
--solver="examples/mssd/train_solver.prototxt" \
--gpu=0 2>&1 | tee "examples/mssd/logs/training_$(date +%Y%m%d%H%M%S).log"
