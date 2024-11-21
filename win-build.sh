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
rm -r models
mkdir -p models 
END=1000
config=train.regression.conf
"../Release/lightgbm" config=$config max_depth=3 num_trees=100 tinygbdt_penalty_feature=0 tinygbdt_penalty_split=0 output_model=models/model.0.0.baseline.txt > models/train.0.0.baseline.out;
# for i in $(seq 5 25 $END); do 
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
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=$i tinygbdt_penalty_split=100 tinygbdt_penalty_feature=10 output_model=models/model.$i.0.penalties.1.tinygbdt_forestsize.txt > models/train.$i.0.penalties.1.tinygbdt_forestsize.out; then
#         echo "Training model $i complete"
#     else
#         echo "Training model $i failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# for i in $(seq -3 1 20); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=101 tinygbdt_penalty_feature=$p tinygbdt_penalty_split=0 output_model=models/model.$p.tinygbdt_penalty_feature.txt > models/train.$p.tinygbdt_penalty_feature.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
# # for i in $(seq 0 0.2 3); do 
# for i in $(seq -3 1 20); do 
#     p=$(python -c "print(float(2**$i))" )
#     if "../Release/lightgbm" config=$config max_depth=3 num_trees=101 tinygbdt_penalty_split=$p tinygbdt_penalty_feature=0 output_model=models/model.$p.tinygbdt_penalty_split.txt > models/train.$p.tinygbdt_penalty_split.out; then
#         echo "Training model $p complete"
#     else
#         echo "Training model $p failed / not complete"
#         # exit 1  
#     fi
#     # sleep 1
# done
for i in $(seq -3 1 10); do 
    p=$(python -c "print(float(2**$i))" )
    if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=64000 tinygbdt_penalty_feature=$p tinygbdt_penalty_split=0 output_model=models/model.$p.tinygbdt_penalty_feature.txt > models/train.$p.tinygbdt_penalty_feature.out; then
        echo "Training model $p complete"
    else
        echo "Training model $p failed / not complete"
        # exit 1  
    fi
    # sleep 1
done
for i in $(seq -3 1 10); do 
    p=$(python -c "print(float(2**$i))" )
    if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=64000 tinygbdt_penalty_split=$p tinygbdt_penalty_feature=0 output_model=models/model.$p.tinygbdt_penalty_split.txt > models/train.$p.tinygbdt_penalty_split.out; then
        echo "Training model $p complete"
    else
        echo "Training model $p failed / not complete"
        # exit 1  
    fi
    # sleep 1
done
for i in $(seq -3 1 10); do 
    p=$(python -c "print(float(2**$i))" )
    if "../Release/lightgbm" config=$config max_depth=3 num_trees=10000 tinygbdt_forestsize=64000 tinygbdt_penalty_split=$p tinygbdt_penalty_feature=$p output_model=models/model.$p.bothpenalties.tinygbdt_penalty_split.txt > models/train.$p.bothpenalties.tinygbdt_penalty_split.out; then
        echo "Training model $p complete"
    else
        echo "Training model $p failed / not complete"
        # exit 1  
    fi
    # sleep 1
done
# echo "Training complete"

# if "../Release/lightgbm" config=predict.conf > predict.output; then
#     echo "Prediction complete"
# else
#     echo "Prediction failed"
#     exit 1
# fi

cd python || exit
python3 evaluate_models.py