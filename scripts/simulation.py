import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import random
import os
from PIL import Image
from queue import Queue

# --- Shared state ---
predictions = []
timestamps = []
max_points = 100
lock = threading.Lock()
event_queue = Queue()

model = None
brainrot_counter = 0
attention_counter = 0
max_brainrot = 3        # threshold for "brainrot" detection
max_attention = 5       # number of zeros to clear warning
warning_window_open = False


# --- MODEL SIMULATION ---
class DummyModel:
    def predict(self, X):
        return [random.randint(0, 1) for _ in range(len(X))]


def handle_data(data):
    """Handle simulated incoming data."""
    global predictions, timestamps, brainrot_counter, attention_counter, warning_window_open

    try:
        # Simulate prediction
        pred = int(model.predict([[float(x) for x in data.strip().split(',')]])[0])

        # Track runs of 1s and 0s
        if pred == 1:
            brainrot_counter += 1
            attention_counter = 0
        else:
            brainrot_counter = 0
            attention_counter += 1

        # Store for visualization
        with lock:
            predictions.append(pred)
            timestamps.append(time.time())
            if len(predictions) > max_points:
                predictions[:] = predictions[-max_points:]
                timestamps[:] = timestamps[-max_points:]

        # Handle warning logic
        if brainrot_counter >= max_brainrot and not warning_window_open:
            event_queue.put("show_warning")
            brainrot_counter = 0
        elif warning_window_open and attention_counter >= max_attention:
            event_queue.put("close_warning")
            attention_counter = 0

    except Exception as e:
        print(f"[ERROR in handle_data]: {e}")


def simulate_data_stream():
    """Simulate fake UDP stream."""
    while True:
        fake_data = ','.join(f"{random.random():.3f}" for _ in range(5))
        handle_data(fake_data)
        time.sleep(0.2)


# --- VISUALIZATION ---
def show_warning_window():
    """Show the warning image in a separate Matplotlib window."""
    global warning_window_open
    warning_window_open = True
    print("[MAIN] Displaying brainrot warning window...")
    img = np.asarray(Image.open('imgs/warning.jpg'))
    fig = plt.figure("⚠️ Brainrot Warning ⚠️")
    plt.imshow(img)
    plt.axis('off')
    plt.show(block=False)
    return fig


def close_warning_window(fig):
    """Close the warning window."""
    global warning_window_open
    print("[MAIN] Closing warning window...")
    plt.close(fig)
    warning_window_open = False


def live_plot():
    """Live-updating plot + event handling."""
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'bo-', label='Prediction (1=Brainrot, 0=Normal)')
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Prediction')
    ax.legend()
    plt.show()

    warning_fig = None

    while True:
        # Update main plot
        with lock:
            if timestamps:
                t = np.array(timestamps) - timestamps[0]
                y = np.array(predictions)
                line.set_xdata(t)
                line.set_ydata(y)
                ax.set_xlim(max(0, t[-1] - 10), t[-1] + 1)
                ax.figure.canvas.draw()
                ax.figure.canvas.flush_events()

        # Handle queued events
        try:
            event = event_queue.get_nowait()
            if event == "show_warning" and not warning_window_open:
                warning_fig = show_warning_window()
            elif event == "close_warning" and warning_window_open and warning_fig:
                close_warning_window(warning_fig)
        except Exception:
            pass  # no event

        time.sleep(0.1)


# --- MAIN ---
if __name__ == "__main__":

    # Start fake data
    sim_thread = threading.Thread(target=simulate_data_stream, daemon=True)
    sim_thread.start()

    # Start visualization
    live_plot()
