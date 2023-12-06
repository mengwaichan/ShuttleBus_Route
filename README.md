# TagIT Shuttle Bus Route

## Overview

This project is a bus route predictor that utilizes Airtag data and Google Maps API to determine the next bus stop. It includes modules for fetching route data, geocoding, and predicting the next bus stop based on the current location.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Examples](#examples)



## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mengwaichan/ShuttleBus_Route.git
    cd ShuttleBus_Route
    ```

2. Install dependencies:

    ```bash
    python -m venv env
    env/Scripts/Activate.ps1
    pip install -r requirements.txt
    ```

## Usage

1. Modify the configuration files:

    - Replace `Constants.MAP_API_KEY` in `route.py` and `geocoding.py` with your Google Maps API key.
        -   Ensure Google Maps Geocoding API is enabled 
        -   Ensure Google Maps Routes API is enabled
    - Set up Firebase Authentication:
        - Create a `firebase_auth.json` file with your Firebase authentication credentials.
        - Ensure this file is kept secure and not shared publicly.

    - Adjust other constants or configurations based on your requirements.

2. Run the main program:

    ```bash
    python main.py
    ```

## Firebase Authentication

1. Create a Firebase project: [Firebase Console](https://console.firebase.google.com/).
2. Navigate to Project Settings.
3. Under the "Service accounts" tab, generate a new private key.
4. Save the generated JSON key file as `firebase_auth.json` in the root of your project.
5. Ensure `firebase_auth.json` is added to your project's `.gitignore` file to avoid accidental commits.


## Documentation

For detailed documentation on each module and class, refer to the docstrings in the source code. Here's a brief overview:

- `AirTag`: Represents an Airtag object with methods for converting data to JSON.
- `Airtags`: Retrieves unique data points from the Airtags CSV file.
- `Route`: Fetches route data using the Google Maps Directions API.
- `Geocoding`: Fetches coordinates based on a street address using the Google Maps Geocoding API.
- `BusStop`: Represents a bus stop object with relevant information.
- `BusRoute`: Predicts the next bus stop and calculates route information.
- `StopPredictor`: Predicts the next bus stop based on current location, previous route, and other factors.