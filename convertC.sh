#!/bin/bash
# input a model path as paramter to bash call, otherwise binary_classification model is used as default
input_model="./examples/min/LightGBM_model.txt"
./lightgbm task=convert_model input_model=$input_model convert_model=/Users/ninaherrmann/Documents/Arduino/sketch_LightGBM_native/ifelse_model.h
