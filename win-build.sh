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
rm -r results
mkdir -p results 
# "../Release/lightgbm" config=train.conf max_depth=3 num_trees=50 tinygbdt_forestsize=64000 > train.output
END=1000
for i in $(seq 5 25 $END); do 
    if "../Release/lightgbm" config=train.conf max_depth=3 num_iterations=$i output_model=results/model.$i.0.num_iterations.txt > results/train.$i.0.num_iterations.out; then
        echo "Training model $i complete"
    else
        echo "Training model $i failed / not complete"
        # exit 1  
    fi
    # sleep 5
done
for i in $(seq 1 2 15); do 
    if "../Release/lightgbm" config=train.conf max_depth=$i num_trees=50 output_model=results/model.$i.0.max_depth.txt > results/train.$i.0.max_depth.out; then
        echo "Training model $i complete"
    else
        echo "Training model $i failed"
        # exit 1  
    fi
done
for i in 800 1600 3200 6400 12800 25600 51200 102400; do 
    if "../Release/lightgbm" config=train.conf max_depth=3 num_trees=100 tinygbdt_forestsize=$i tinygbdt_penalty_split=0 tinygbdt_penalty_feature=0 output_model=results/model.$i.0.tinygbdt_forestsize.txt > results/train.$i.0.tinygbdt_forestsize.out; then
        echo "Training model $i complete"
    else
        echo "Training model $i failed / not complete"
        # exit 1  
    fi
    # sleep 1
done
for i in $(seq 0 0.5 10); do 
    if "../Release/lightgbm" config=train.conf max_depth=3 num_trees=100 tinygbdt_penalty_feature=$i tinygbdt_penalty_split=0 output_model=results/model.$i.tinygbdt_penalty_feature.txt > results/train.$i.tinygbdt_penalty_feature.out; then
        echo "Training model $i complete"
    else
        echo "Training model $i failed / not complete"
        # exit 1  
    fi
    # sleep 1
done
for i in $(seq 0 0.2 3); do 
    if "../Release/lightgbm" config=train.conf max_depth=3 num_trees=100 tinygbdt_penalty_split=$i tinygbdt_penalty_feature=0 output_model=results/model.$i.tinygbdt_penalty_split.txt > results/train.$i.tinygbdt_penalty_split.out; then
        echo "Training model $i complete"
    else
        echo "Training model $i failed / not complete"
        # exit 1  
    fi
    #
done
echo "Training complete"

# if "../Release/lightgbm" config=predict.conf > predict.output; then
#     echo "Prediction complete"
# else
#     echo "Prediction failed"
#     exit 1
# fi

cd python || exit
python3 evaluate_models.py