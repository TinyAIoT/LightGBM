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

# sh runExperiment.sh "./Release/lightgbm"
