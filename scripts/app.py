from udp_receiver import UDPReceiver
import time
import matplotlib.pyplot as plt
import joblib

def handle_data(data):
    # Use the model to make prediction on the received data
    prediction = model.predict([data])  # assuming model has a predict method

    # Visualize the prediction in real time
    


def print_data(data):
    print(f"[DATA RECEIVED]: {data}")

def load_model(model_path):
    # Placeholder for model loading logic
    print(f"Loading model from {model_path}...")

    # Load and return the model
    model = joblib.load(model_path)
    return model

if __name__ == "__main__":
    # prompt for model path
    model_path = input("Enter path to the pre-trained model: ")
    model = load_model(model_path)

    receiver = UDPReceiver(port=1000)
    receiver.start(callback=handle_data)

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping receiver...")
        receiver.stop()
