# Parking-Allocation-System
This is a simple application that helps to allocate parking slots for vehicles. This is developed using python for PC.

# Development Environment

## Language
Python 3.8.9
### Libraries
- pandas - 1.5.3
- DateTime - 5.0
- tkinter

## GUI
This application has an GUI which is developed using tkinter library in python.

## Data Storing
The parking details are stored in a .csv files.

- "parking_details.csv" will contain the current status of the parking slots.
You can add Slot number, Vehicle type manually in "parking_details.csv" to increase or decrease your parking slots.
The Slot Number must be a unique value.
Currently this code supports only two types of vehicles i.e "Bike" and "Car" (Case Sensitive).
In this file, the data will be deleted by the program as soon as the vehicle leaves, so that the program can identify all the empty slots.

- "parking_log.csv" will contain all records of the parking.
Entry time, Exit time, Slot Number, Vehicle type.. everything will be stored in this file.
In this the data will not be deleted by the program in order to store all the log details.
