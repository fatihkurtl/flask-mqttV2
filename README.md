Flask-MQTT Alarm Logs

Flask-MQTT Alarm Logs is an application that uses Flask and MQTT protocol to track sensor data. With this application, you can record, visualize, and report data from devices that support the MQTT protocol.
Features

Flask-MQTT Alarm Logs has the following features:

    Recording sensor data using the MQTT protocol
    Flask web interface for displaying and managing sensor data
    Visualization of sensor data through charts and graphs
    Notification alerts for certain sensor thresholds
    User authentication and role-based access control

Getting Started

To use Flask-MQTT Alarm Logs, follow these steps:

    Clone the repository to your local machine
    Create a virtual environment and activate it
    Install the required dependencies using pip
    Start the Flask development server

shell

$ git clone https://github.com/fatihkurtl/flask-mqtt_alarm_logs.git
$ cd flask-mqtt_alarm_logs
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ flask run

Usage

Once the Flask development server is running, navigate to http://localhost:5000 in your web browser to access the application. You will be prompted to create a user account and log in.

From the main dashboard, you can view and manage sensor data. You can also create notifications for certain sensor thresholds and view data visualizations in the form of charts and graphs.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Contributions to Flask-MQTT Alarm Logs2 are welcome! Please see the CONTRIBUTING.md file for guidelines.
