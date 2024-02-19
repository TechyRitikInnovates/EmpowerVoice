import tensorflow as tf
import sounddevice as sd
import numpy as np

# Load the TFLite model and labels
model_path = "soundclassifier_with_metadata.tflite"
labels_path = "labels.txt"

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Load labels
with open(labels_path, "r") as f:
    labels = f.read().splitlines()

# Function to preprocess input audio
def preprocess_audio(audio_data, target_size=44032):  # Adjust target_size as needed
    # Your preprocessing logic goes here
    # Ensure the input size matches the expected size of the model
    if len(audio_data) < target_size:
        # Pad with zeros if the input is shorter than the target size
        audio_data = np.pad(audio_data, (0, target_size - len(audio_data)))
    elif len(audio_data) > target_size:
        # Trim if the input is longer than the target size
        audio_data = audio_data[:target_size]
    # Reshape to a 1D array
    audio_data = audio_data.reshape((1, -1))
    # Normalize and convert to float32
    return audio_data.astype(np.float32) / 32767.0


# Function to make predictions
def predict(audio_data):
    input_data = preprocess_audio(audio_data)

    # Get input and output tensors
    input_tensor_index = interpreter.get_input_details()[0]['index']
    output = interpreter.tensor(interpreter.get_output_details()[0]['index'])

    # Set the input tensor with the preprocessed audio data
    interpreter.set_tensor(input_tensor_index, input_data)

    # Run inference
    interpreter.invoke()

    # Get the output results
    output_data = output()[0]

    # Post-process the output data if needed
    predicted_label_index = np.argmax(output_data)
    predicted_label = labels[predicted_label_index]

    return predicted_label

# Function to process microphone input
def process_microphone_input():
    # Set up the microphone
    duration = 10  # seconds
    sample_rate = 44100  # Hz

    # Record audio from the microphone
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    print("Recoding Started...")
    sd.wait()

    # Make prediction
    prediction = predict(audio_data)
    print("Recoding Ended.")

    print("Predicted label:", prediction)

# Run the program
process_microphone_input()
