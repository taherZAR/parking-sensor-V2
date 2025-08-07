# 🚗 IoT Parking Sensor with ESP32

An IoT-enabled smart parking sensor system using **ESP32**, an
**ultrasonic sensor**, **buzzer**, **LED**, and a **push button**, that
detects object distance and activates an adaptive alarm. It connects to
**WiFi** and publishes distance data via **MQTT**.

------------------------------------------------------------------------

## 🧠 Features

-   📏 Measures distance with HC-SR04 ultrasonic sensor
-   🚨 Activates a buzzer & LED alarm when an object is too close
-   🔇 Manual override using a push button
-   🌐 Sends real-time distance data to the cloud using MQTT
-   🧠 Adaptive buzzer rhythm: faster as objects get closer

------------------------------------------------------------------------

## 🛠️ Components Used

  Component       Description
  --------------- ----------------------------
  ESP32           Main microcontroller
  HC-SR04         Ultrasonic distance sensor
  Active Buzzer   Sound alarm output
  LED             Visual alarm indicator
  Push Button     Manually stop the alarm
  WiFi            Wokwi-GUEST (simulated)
  MQTT Broker     e.g. `broker.hivemq.com`

------------------------------------------------------------------------

## ⚙️ How It Works

1.  The **ultrasonic sensor** measures distance continuously.
2.  If an object is detected closer than **20 cm**, the **buzzer** and
    **LED** are activated in a rhythmic pattern that speeds up as the
    object gets closer.
3.  The **push button** allows manual deactivation of the alarm.
4.  Distance data is **published via MQTT** to the topic `wokwi`.
5.  When the object moves far enough, the alarm can auto-reset (with a
    small buffer zone).

------------------------------------------------------------------------

## 📡 IoT Integration (MQTT)

-   **Broker**: `broker.hivemq.com` (public)
-   **Topic**: `wokwi`
-   **Payload**: Distance in cm (e.g., `12.3`)
-   You can view real-time distance using an MQTT client like [MQTT
    Explorer](https://mqtt-explorer.com/) or [MQTT
    Studio](https://mqtt.studio/).

------------------------------------------------------------------------

## 🔘 Manual Override Logic

-   Pressing the button turns off the alarm.
-   The alarm will only reset **automatically** when the object moves
    beyond **25 cm** (20 + 5 cm buffer).

------------------------------------------------------------------------

## 🧪 How to Use in Wokwi

1.  Go to [wokwi.com](https://wokwi.com)
2.  Use ESP32 with:
    -   HC-SR04 sensor
    -   Buzzer (Pin 15)
    -   LED (Pin 21)
    -   Push Button (Pin 32)
3.  Paste the MicroPython code into `main.py`
4.  Simulate and observe alarm activation, button press override, and
    MQTT publishing

------------------------------------------------------------------------

## 💡 Future Ideas

-   Add temperature or sound sensor
-   Add a web dashboard or Blynk integration
-   Store readings in a database or Google Sheets
