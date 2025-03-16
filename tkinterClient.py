import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt

# Global variable to store fitness tracker data
sensor_data = {
    "temperature": "N/A",
    "acceleration": "N/A",
    "heart_rate": "N/A",
    "steps": "N/A",
    "calories_burned": "N/A",
    "current_activity": "Idle"
}

# Callback function for when a message is received
def on_message(client, userdata, msg):
    global sensor_data
    try:
        # Decode and convert the string to a dictionary
        sensor_data = eval(msg.payload.decode())
        update_gui()
    except Exception as e:
        print(f"Error parsing message: {e}")

def update_gui():
    temp_label_value.config(text=f"{sensor_data['temperature']} \u00b0C")
    accel_label_value.config(text=f"{sensor_data['acceleration']} m/s\u00b2")
    heart_label_value.config(text=f"{sensor_data['heart_rate']} BPM")
    steps_label_value.config(text=f"{sensor_data['steps']} steps")
    calories_label_value.config(text=f"{sensor_data['calories_burned']} kcal")

    if sensor_data['heart_rate'] > 120 or sensor_data['acceleration'] > 5.0:
        activity_label_value.config(text=f"Running")
    elif sensor_data['heart_rate'] > 80 and sensor_data['heart_rate'] <= 120 or sensor_data['acceleration'] < 5.0:
        activity_label_value.config(text=f"Walking")
    elif sensor_data['heart_rate'] <= 80 or sensor_data['acceleration'] < 1.0:
        activity_label_value.config(text=f"Idle")
    else:
        activity_label_value.config(text=f"Idle")

# MQTT Setup
def setup_mqtt(broker_ip, topic):
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_ip, 1883, 60)
    client.subscribe(topic)
    client.loop_start()

# GUI SETUP
def setup_gui():
    app = tk.Tk()
    app.title("Fitness Tracker Data Viewer")
    app.geometry("500x350")
    app.configure(bg="#2e3b4e")  # dark background

    # title
    title_label = ttk.Label(
        app,
        text="Fitness Tracker Data",
        font=("Helvetica", 20, "bold"),
        foreground="#FFFFFF",
        background="#2e3b4e"
    )
    title_label.pack(pady=15)

    # separator
    ttk.Separator(app, orient="horizontal").pack(fill="x", padx=20, pady=10)

    # centered frame for data
    data_frame = tk.Frame(app, bg="#2e3b4e")
    data_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # temperature
    global temp_label_value
    temp_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Temperature:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    temp_label_value.grid(row=0, column=1, sticky="w", padx=10)

    # acceleration
    global accel_label_value
    accel_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Acceleration:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    accel_label_value.grid(row=1, column=1, sticky="w", padx=10)

    # heartrate
    global heart_label_value
    heart_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Heart Rate:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    heart_label_value.grid(row=2, column=1, sticky="w", padx=10)

    # steps
    global steps_label_value
    steps_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Steps:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    steps_label_value.grid(row=3, column=1, sticky="w", padx=10)

    # calories
    global calories_label_value
    calories_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Calories Burned:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    calories_label_value.grid(row=4, column=1, sticky="w", padx=10)

    # activity
    global activity_label_value
    activity_label_value = ttk.Label(data_frame, text="N/A", font=("Helvetica", 14, "bold"), foreground="#FFFFFF", background="#2e3b4e")
    ttk.Label(data_frame, text="Current activity:", font=("Helvetica", 14), foreground="#f4b41a", background="#2e3b4e").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    activity_label_value.grid(row=5, column=1, sticky="w", padx=10)


    return app

if __name__ == "__main__":
    MQTT_BROKER_IP = "192.168.1.8"
    MQTT_TOPIC = "wearable/sensor"

    # Start the MQTT client
    setup_mqtt(MQTT_BROKER_IP, MQTT_TOPIC)

    # Start the GUI
    app = setup_gui()
    app.mainloop()