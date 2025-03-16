import paho.mqtt.client as mqtt
import time
import random

def simulate_fitness_tracker():
    # Initialize MQTT client
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    print("Publishing fitness tracker data...")

    while True:
        sensor_data = {
            "temperature": round(random.uniform(36.0, 37.5), 2),  # Body temperature in Celsius
            "acceleration": round(random.uniform(0.0, 10.0), 2),  # Acceleration in m/s^2
            "heart_rate": random.randint(60, 180),  # Heart rate in BPM
            "steps": random.randint(100, 500),  # Steps taken
            "calories_burned": round(random.uniform(0.5, 10.0), 2)  # Calories burned
        }

        client.publish("wearable/sensor", str(sensor_data))
        print(f"Published: {sensor_data}")

        time.sleep(3)

if __name__ == "__main__":
    simulate_fitness_tracker()