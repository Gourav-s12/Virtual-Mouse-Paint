import os
import numpy as np
import csv
import random
import cv2
import mediapipe as mp
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import OneHotEncoder
from keras.utils import pad_sequences

# Define hyperparameters
input_shape = 63  # input shape for the model
num_classes = 5  # number of output classes
num_epochs = 1000  # number of epochs for training
batch_size = 64  # batch size for training

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
    label = os.path.basename(csv_file).split('.')[0]
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

# Pad the sequences to the same length
def pad_data(data, max_length):
    return pad_sequences(data, maxlen=max_length, dtype='float32', padding='post', value=0.0)

# Load and prepare the training and test datasets
def load_data(train_path, test_path):
    train_data = extract_data(train_path)
    test_data = extract_data(test_path)

    train_data, train_labels = extract_data_and_label(train_data)
    test_data, test_labels = extract_data_and_label(test_data)

    labels = np.unique(train_labels)
    num_classes = len(labels)
    y_train = OneHotEncoder().fit_transform(np.array(train_labels).reshape(-1, 1)).toarray()
    y_test = OneHotEncoder().fit_transform(np.array(test_labels).reshape(-1, 1)).toarray()

    max_length = max(len(seq) for seq in train_data + test_data)
    x_train = pad_data(train_data, max_length)
    x_test = pad_data(test_data, max_length)

    return x_train, y_train, x_test, y_test, max_length, num_classes

# Train the model
def train_model(train_path, test_path):
    x_train, y_train, x_test, y_test, max_length, num_classes = load_data(train_path, test_path)
    my_model = cnn_model(max_length, num_classes)
    my_model.fit(x_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_data=(x_test, y_test))
    my_model.save("gesture_model_virtual_mouse")
    return my_model

# Test the model using webcam
def test_model():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils
    label = ['screenshot', 'none', 'open']
    model = keras.models.load_model('gesture_model_virtual_mouse')

    def landmark_to_vector(landmarks):
        vector = []
        for landmark in landmarks:
            vector.append(landmark.x)
            vector.append(landmark.y)
            vector.append(landmark.z)
        return vector

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        status, frame = cap.read()
        if status:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            outcomes = hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if outcomes.multi_hand_landmarks:
                for hand_landmarks in outcomes.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    vector = landmark_to_vector(hand_landmarks.landmark)
                    vector = np.array(vector).reshape(1, -1)  # Adjust to match input shape
                    prediction = model.predict(vector)
                    index = np.argmax(prediction)
                    cv2.putText(frame, label[index], (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

# Main function to train and test the model
def main():
    train_path = "trainModel/gesture/train"
    test_path = "trainModel/gesture/test"

    # Train the model
    train_model(train_path, test_path)
    print("testing-")
    # Test the model
    test_model()

if __name__ == "__main__":
    main()
