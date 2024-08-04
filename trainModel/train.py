# -Program Name : Intelligen Teaching Web Based Application - train.py
# -Description : Use for train the model for recognise hand gesture
# -First Written on: 12 Feb 2023
# -Editted on: 22 April 2023

import os
import numpy as np
import csv
import random
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import OneHotEncoder
from keras.utils import pad_sequences

# Define hyperparameters
input_shape = 63  # input shape for the model
num_classes = 5  # number of output classes
num_epochs = 500  # number of epochs for training
batch_size = 128  # batch size for training

# Define the model architecture
def cnn_model(input_shape, num_classes):
    model = keras.Sequential([
        layers.Input(shape=(input_shape, 1)),  # Explicitly define input layer
        layers.Conv1D(filters=64, kernel_size=3, activation='relu'),
        layers.MaxPooling1D(pool_size=2),
        layers.Dense(50, activation='relu'),
        layers.Dropout(0.3),
        layers.Conv1D(filters=30, kernel_size=3, activation='relu'),
        layers.MaxPooling1D(pool_size=2),
        layers.Dense(20, activation='relu'),
        layers.Dropout(0.1),
        layers.Flatten(),
        layers.Dense(num_classes, activation='softmax')
    ])
    print("Started Compiling")
    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print("Model Compiled....")
    return model

# Extract data and labels from the dataset
def extract_data_and_label(dataset):
    data = []
    labels = []
    for p in dataset:
        data.append(p[0])
        labels.append(p[1])
    return data, labels

# Extract information from CSV files
def extract_info_from_csv(csv_file):
    label = csv_file.split('/')[-1].split('.')[0]
    dataset = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            dataset.append([row, label])
    return dataset

# Extract data from a directory of CSV files
def extract_data(base):
    dataset = []
    for file in os.listdir(base):
        dataset += extract_info_from_csv(os.path.join(base, file))
    random.shuffle(dataset)
    return dataset

# Load the training and test datasets
train_dataset_csv = "trainModel/gesture/train"
test_dataset_csv = "trainModel/gesture/test"
train_data = extract_data(train_dataset_csv)
test_data = extract_data(test_dataset_csv)

# Extract the data and labels from the datasets
train_data, train_labels = extract_data_and_label(train_data)
test_data, test_labels = extract_data_and_label(test_data)

labels = np.unique(train_labels)
num_classes = len(labels)
y_train = OneHotEncoder().fit_transform(np.array(train_labels).reshape(-1, 1)).toarray()
y_test = OneHotEncoder().fit_transform(np.array(test_labels).reshape(-1, 1)).toarray()

# Pad the sequences to the same length
max_length = max(len(seq) for seq in train_data + test_data)
x_train = pad_sequences(train_data, maxlen=max_length, dtype='float32', padding='post', value=0.0)
x_test = pad_sequences(test_data, maxlen=max_length, dtype='float32', padding='post', value=0.0)

# Train the model
my_model = cnn_model(max_length, num_classes)
my_model.fit(x_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_data=(x_test, y_test))
my_model.save("gesture_model_virtual_mouse")
