#!/bin/bash

# Create directories
mkdir -p ./bottleneck_values/
mkdir -p ./output/
mkdir -p ./logs/
mkdir -p ./models/

# Retrain the inception v3 model on our training dataset
python3 tensorflow/tensorflow/examples/image_retraining/retrain.py --bottleneck_dir ./bottleneck_values/ --output_graph=./output/graph.pb --output_labels=./output/labels.txt --final_tensor_name=dermatologist --summaries_dir=./logs/ --image_dir=./data/train/ --model_dir=./models/ --validation_batch_size=-1 --learning_rate=0.01 --train_batch_size=250
