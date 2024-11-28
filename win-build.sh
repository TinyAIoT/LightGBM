# #!/bin/bash

if cmake -B build -S . -A x64 -DUSE_CUDA=0 -DUSE_DEBUG=ON; then
    if cmake --build build --target ALL_BUILD --config Release; then
        echo "build complete"
    else
        echo "cmake build failed"
        exit 1
    fi
else
    echo "CMake configuration failed"
    exit 1
fi

cd experiments || exit
rm -r models # ATTENTION: deletes all models in the models folder
mkdir -p models 
END=1000
################# Change config for other training data #######################
config=train.conf
# use train.regression.conf for regression data
# change datasets in the config file if you want to add new datasets
############################################################################

# base model with both penalties zero
"../Release/lightgbm" config=$config max_depth=3 num_trees=100 tinygbdt_penalty_feature=0 tinygbdt_penalty_split=0 output_model=models/model.0.0.baseline.txt > models/train.0.0.baseline.out;
:'############################################################################################################
each for loop trains different model settings with every run saving a model.txt and a output.out file.
you have to comment / uncomment the desired loop to train the models.
the cbuild process is created for Windows, might need some adaptations for other OS.
############################################################################################################'

:'
training models based on grid of threshold and feature penalties.
ACTIVATE for Exeperiment 2
'
# ms=64000
# for i in $(seq -10 1 15); do 
#     for j in $(seq -10 1 15); do 
#         fp=$(python -c "print(float(2**$i))" )
#         tp=$(python -c "print(float(2**$j))" )
#         if "../Release/lightgbm" config=$config max_depth=3 num_trees=100000 tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=models/model.$ms.0.ms.$fp.fp.$tp.tp.grid.txt > models/train.$ms.0.ms.$fp.fp.$tp.tp.grid.out; then
#             echo "Training model fp $fp tp $tp complete"
#         else
#             echo "Training model fp $fp tp $tp failed / not complete"
#             # exit 1  
#         fi
#     done
# done

:'
the following three loops train the 3 x 3 models for the memory experiments.
! NEED TO CHANGE penalties for the last loop manually to the best performing penalties; use previous grid loop to determine best penalties!
ACTIVATE for Exeriment 3
'
# for i in 9 78 313; do 
#     if "../Release/lightgbm" config=$config max_depth=3 num_iterations=$i output_model=models/model.$i.0.num_iterations.txt > models/train.$i.0.num_iterations.out; then
#         echo "Training model $i complete"
#     else
#         echo "Training model $i failed / not complete"
#         # exit 1  
#     fi
#     # sleep 5
# done
# for i in 8000 64000 256000; do 
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=$i tinygbdt_penalty_split=0 tinygbdt_penalty_feature=0 output_model=models/model.$i.0.tinygbdt_forestsize.txt > models/train.$i.0.tinygbdt_forestsize.out; then
#         echo "Training model $i complete"
#     else
#         echo "Training model $i failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# for i in 8000 64000 256000; do
#     if [ $i -eq 8000 ]; then
#         tp=8
#         fp=16
#     fi
#     if [ $i -eq 64000 ]; then
#         tp=0.0625
#         fp=0.0625
#     fi
#     if [ $i -eq 256000 ]; then
#         tp=0
#         fp=0.0625
#     fi
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=$i tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=models/model.$i.0.penalties.1.tinygbdt_forestsize.txt > models/train.$i.0.penalties.1.tinygbdt_forestsize.out; then
#         echo "Training model $i complete"
#     else
#         echo "Training model $i failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done

:'
altering penalties only along one axis, i.e. only feature or split penalty are changed.
uses static max_depth and num_trees
ACTIVATE for Experiment 1
'
# for i in $(seq -10 1 20); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=100 tinygbdt_penalty_feature=$p tinygbdt_penalty_split=0 output_model=models/model.$p.tinygbdt_penalty_feature.txt > models/train.$p.tinygbdt_penalty_feature.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# for i in $(seq -10 1 20); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=100 tinygbdt_penalty_split=$p tinygbdt_penalty_feature=0 output_model=models/model.$p.tinygbdt_penalty_split.txt > models/train.$p.tinygbdt_penalty_split.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done

:'
altering the penalties individually and together for a given modelsize ms.
'
ms=256000
# for i in $(seq -7 1 5); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=100000 tinygbdt_forestsize=$ms tinygbdt_penalty_feature=$p tinygbdt_penalty_split=0 output_model=models/model.$p.tinygbdt_penalty_feature.txt > models/train.$p.tinygbdt_penalty_feature.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# for i in $(seq -7 1 5); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=100000 tinygbdt_forestsize=$ms tinygbdt_penalty_split=$p tinygbdt_penalty_feature=0 output_model=models/model.$p.tinygbdt_penalty_split.txt > models/train.$p.tinygbdt_penalty_split.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# for i in $(seq -7 1 5); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=100000 tinygbdt_forestsize=$ms tinygbdt_penalty_split=$p tinygbdt_penalty_feature=$p output_model=models/model.$p.bothpenalties.txt > models/train.$p.bothpenalties.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done

# echo "Training complete"

# if "../Release/lightgbm" config=predict.conf > predict.output; then
#     echo "Prediction complete"
# else
#     echo "Prediction failed"
#     exit 1
# fi

:'
ATTENTION: currently need to comment or uncomment the correct functions in the evalution script. 
'
cd python || exit
python3 evaluate_models.py