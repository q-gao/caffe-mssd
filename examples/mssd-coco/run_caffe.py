#!/usr/bin/python
from __future__ import print_function
import subprocess
import shlex
import re
import os.path

def GetCurHumanReadableTime():
    import time
    import datetime

    # strframe == str from time
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

def CreateArgumentParser():
    import argparse
    import textwrap
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                This tool is used to run python
             '''),
        # After the help
        epilog=textwrap.dedent('''\
                examples:
                ---------------------------------------------------------------------------
             ''')
    )

    ap.add_argument("--solver", required = True,
                    help="solver prototxt")
    ap.add_argument("-g", "--gpu_num", type=int, required = True,
                    help="num of GPU used for training")
    ap.add_argument("-m", "--max_iter", type=int, required = True,
                    help="max training iteration")
    ap.add_argument("-s", "--iter_size", type=int, default = 1,
                    help="num of minibatches per iteration")
    ap.add_argument("-b", "--batch_size_per_gpu", type=int, required = True,
                    help="batch size per GPU")    
    ap.add_argument("-p", "--result_file_name_prefix", required = True,
                    help="prefix of result file names, e.g., snapshot file, caffemodel and log")    
    ap.add_argument("-t", "--test_interval", type=int, required = True,
                    help="test intervals in iterations") 
    ap.add_argument("--snapshot_interval", type=int, required = True,
                    help="snapshot intervals in iterations") 
    ap.add_argument("--training_lmdb_location",  required = True,
                    help="training lmdb location") 


    ap.add_argument("-w", "--model_weights_file", default=None,
                    help="initialization model weights")
    ap.add_argument("-r", "--base_learning_rate", type=float, default='0.001',
                    help="base learning rate")
    ap.add_argument("-a", "--learning_rate_adj_iter", type=int, nargs='+', default="None",
                    help="iteration numbers to adjust learing rate")
    return ap

def CheckArgs(args):
    r = os.path.isfile(args.solver)
    if not r:
        print('ERROR: can not find solver file ' + args.solver)

    if args.learning_rate_adj_iter is None:
        args.learning_rate_adj_iter = [args.max_iter]

    for i in xrange( len(args.learning_rate_adj_iter) - 1):
        if args.learning_rate_adj_iter[i] >= args.learning_rate_adj_iter[i+1]:
            r = False
            print('ERROR: argument "learning_rate_adj_iter" must be at increasing order')

    return r

def GetTrainTestNetFromSolverPrototxt(solver_file):
    try:
        with open(solver_file) as fin:
            cnt = 0
            for line in fin:
                m = re.search(r'train_net:\s*"(.+)"', line)
                if m:
                    train_net = m.group(1)
                    cnt += 1
                    if cnt >= 2: return (train_net, test_net)
                else:
                    m = re.search(r'test_net:\s*"(.+)"', line)
                    if m:
                        test_net = m.group(1)
                        cnt += 1                    
                        if cnt >= 2:    return (train_net, test_net)
    except IOError:
        print('FAILED to open ' + solver_file)
        return (None, None)

def EscapeSlashInStr(s):
    return "\/".join( s.split('/') )

def ModifySolverFile(args):
    # base learing rate
    subprocess.call(shlex.split("sed -r -i 's/base_lr:.+/base_lr: {}/' {}".format(
                                args.base_learning_rate, args.solver)))
    # test_interval
    subprocess.call(shlex.split("sed -r -i 's/test_interval:.+/test_interval: {}/' {}".format(
                                args.test_interval, args.solver)))
    # snapshot interval
    subprocess.call(shlex.split("sed -r -i 's/snapshot:.+/snapshot: {}/' {}".format(
                                args.snapshot_interval, args.solver)))    
    # snapshot prefix
    subprocess.call(shlex.split("sed -r -i 's/snapshot_prefix:.+/snapshot_prefix: \"{}\"/' {}".format(
                                EscapeSlashInStr(args.result_file_name_prefix), args.solver)))        
    # max_iter
    subprocess.call(shlex.split("sed -r -i 's/max_iter:.+/max_iter: {}/' {}".format(
                                args.max_iter, args.solver)))

    subprocess.call(shlex.split("sed -r -i 's/iter_size:.+/iter_size: {}/' {}".format(
                                args.iter_size, args.solver)))


    # adjust learning rate adjustment iteration
    subprocess.call(shlex.split("sed -r -i '/stepvalue:/d' " + args.solver))
    if args.learning_rate_adj_iter is not None:
        for v in args.learning_rate_adj_iter:
            # append to the end of file
            subprocess.call(shlex.split("sed -r -i '$ a stepvalue: {}' ".format(v) + args.solver))

def ModifyTrainNet(train_net, args):
    """
    # MobileNet_train.prototxt
    source: "examples/COCO/valminusminival2014_3ch_lmdb"
    batch_size: 8 # mini-batch size per GPU
    """
    if not os.path.isfile(train_net):
        print('ERROR: can not find training net spec file {} specified in {}'.format(train_net, args.solver))
        return False
    cmd = "sed -r -i 's/source:.+/source: \"{}\"/' {}".format(
            EscapeSlashInStr(args.training_lmdb_location), train_net)
    print("  " + cmd)
    subprocess.call(shlex.split(cmd))        
    # batch_size
    cmd = "sed -r -i 's/batch_size:.+/batch_size: {}/' {}".format(
            args.batch_size_per_gpu, train_net)
    print("  " + cmd)
    subprocess.call(shlex.split(cmd))    
    return True

def main(args):  
    # sed -i -r -e 's/source:\s*.+$/source: \/local\/mnt/' t.txt
    if not CheckArgs(args):
        return -1
    
    gpu_id_str = '0'
    for i in xrange(1, args.gpu_num):
        gpu_id_str += (',{}'.format(i))
    training_cmd = "./build/tools/caffe train " \
                   "-solver {} " \
                   "-gpu {} ".format(args.solver, gpu_id_str)
    if args.model_weights_file is not None:
        training_cmd += '-weights {} '.format(args.model_weights_file)

    log_file_name = args.result_file_name_prefix + GetCurHumanReadableTime() + '.log'

    print('Updating {} with specified parameters'.format(args.solver))
    ModifySolverFile(args)

    train_net, test_net = GetTrainTestNetFromSolverPrototxt(args.solver)
    print('Updating {} with specified parameters'.format(train_net))
    if not ModifyTrainNet(train_net, args): return -1

    if not os.path.isfile(test_net):
        print('ERROR: can not find test net file ' + test_net)
        return -1

    try:
        with open(log_file_name, 'w') as fh_log:
            print("\n"+training_cmd)
            subprocess.call(shlex.split(training_cmd), stdout=fh_log, stderr=fh_log)
    except IOError:
        print('FAILED to open log file ' + log_file_name)
    return 0

if __name__ == '__main__':
    #NOTE: muse leave a space at the end of string
    arg_str=\
        "--solver examples/mssd-coco/train_solver_coco_for_script.prototxt " \
        "--gpu_num 8 " \
        "--max_iter 200000 "\
        "--test_interval 5000 " \
        "--snapshot_interval 5000 " \
        "--iter_size 1 " \
        "--batch_size_per_gpu 16 " \
        "--base_learning_rate 0.004 " \
        "--learning_rate_adj_iter 100000 200000 300000 "\
        "--result_file_name_prefix examples/mssd-coco/logs/MSSD_COCO95K " \
        "--training_lmdb_location examples/COCO/trainl2014_valminusminival2014_lmdb"
        #"--model_weights_file examples/mssd-coco/MobileNet_SSD_320x320_COCO_LR1E-3_2_iter_18000.caffemodel " \        

    import shlex
    ap = CreateArgumentParser()
    args = ap.parse_args(shlex.split(arg_str))
    main(args)