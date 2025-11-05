from udp_receiver import UDPReceiver
import matplotlib.pyplot as plt
import joblib
import numpy as np
import time
import threading

# --- Global variables ---
predictions = []
timestamps = []
max_points = 100  # number of points to show on plot
model = None
lock = threading.Lock()  # thread-safety for shared data


def handle_data(data):
    """Handle each new UDP message."""
    global predictions, timestamps, model

    try:
        # Parse incoming data string into a numeric feature array
        # (adjust this parsing depending on your actual UDP data format)
        features = np.array(list(map(float, data.strip().split(',')))).reshape(1, -1)

        # Make prediction using your model
        pred = int(model.predict(features)[0])  # assume output is 0 or 1

        # Store for visualization
        with lock:
            predictions.append(pred)
            timestamps.append(time.time())
            # Keep only recent data
            if len(predictions) > max_points:
                predictions = predictions[-max_points:]
                timestamps = timestamps[-max_points:]

    except Exception as e:
        print(f"[ERROR in handle_data]: {e}")


def load_model(model_path):
    print(f"Loading model from {model_path}...")
    return joblib.load(model_path)


def live_plot():
    """Continuously update live prediction plot."""
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'bo-', label='Prediction (1=Active, 0=Inactive)')
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Prediction')
    ax.legend()
    plt.show()

    while True:
        with lock:
            if len(timestamps) > 0:
                t = np.array(timestamps) - timestamps[0]  # relative time
                y = np.array(predictions)
                line.set_xdata(t)
                line.set_ydata(y)
                ax.set_xlim(max(0, t[-1] - 10), t[-1] + 1)  # show last ~10s
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()
        time.sleep(0.1)  # update rate


if __name__ == "__main__":
    model_path = input("Enter path to the pre-trained model: ")
    model = load_model(model_path)

    receiver = UDPReceiver(port=1000)
    receiver.start(callback=handle_data)

    try:
        # Start visualization in the main thread
        live_plot()
    except KeyboardInterrupt:
        print("\nStopping receiver...")
        receiver.stop()
