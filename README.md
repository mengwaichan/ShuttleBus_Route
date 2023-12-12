# TagIT Shuttle Bus Route

## Overview

This project is a bus route predictor that utilizes Airtag data and Google Maps API to determine the route and arrival time. It includes modules for fetching route data, geocoding, and predicting the next bus stop based on the current location.

This project is currently live and running at [ccnyshuttle.com](https://ccnyshuttle.com).

**Note:** The corresponding frontend for this project can be found [here](https://github.com/MarkusCDev/TagIT.git). 

## Table of Contents

- [Requirements](#macos-requirements)
- [Installation](#installation)
- [Firebase Authentication](#firebase-authentication)
- [CSV Data Format](#csv-data-format)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributions](#contributions)

## MacOS Requirements

- MacOS Version: `Monterey`, `Ventura`, or `Sonoma`
- Package Manager: `Brew`
    - Installation: (https://brew.sh/)
      
- JSON Processor: `JQ`
    - `brew install jq`
      
- Python: Either Python or Python3 works
    - `brew install python`
      
- Terminal Access: Ensure Terminal has `Full Disk Access` in the `Privacy & Security` settings in MacOS


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mengwaichan/ShuttleBus_Route.git
    cd ShuttleBus_Route
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    
3. Permissions:
    ```bash
    chmod 700 tagit.sh
    ```


## Firebase Authentication

1. Create a Firebase project: [Firebase Console](https://console.firebase.google.com/).
2. Navigate to Project Settings.
3. Under the `Service accounts` tab, generate a new private key.
4. Save the generated JSON key file as `firebase_auth.json` in the root of your project.
5. Ensure `firebase_auth.json` is added to your project's `.gitignore` file to avoid accidental commits.

## CSV Data Format

The Airtag.csv data expected by this program should follow the format:

```csv
datetime,name,batterystatus,locationpositiontype,locationlatitude,locationlongitude,addressstreetaddress,addressstreetname,addressareaofinteresta,addressareaofinterestb
```
- **datetime**: Timestamp indicating when the location data was recorded.
- **name**: Name or identifier of the shuttle bus.
- **batterystatus**: Battery status of the airtag.
- **locationpositiontype**: Method used to determine the location.
- **locationlatitude**: Latitude coordinate of the bus's location.
- **locationlongitude**: Longitude coordinate of the bus's location.
- **addressstreetaddress**: Street address of the bus's location.
- **addressstreetname**: Name of the street where the bus is located.
- **addressareaofinteresta**: Area of interest related to the bus's location.
- **addressareaofinterestb**: Additional area of interest related to the bus's location.

Ensure that your CSV files adhere to this structure for accurate processing by the program.

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

    - Open: `FindMy` Application
  
    - Open Terminal: 
        ```bash
        ./tagit.sh & python main.py
        ```
    - Ensure: `FindMy` is in the foreground, and the script is the background

3. To kill bash tagit.sh script:
    ```bash
    pkill -f tagit.sh
    ```

## Documentation

For detailed documentation on each module and class, refer to the docstrings in the source code. Here's a brief overview:
### Bash
- `tagit.sh`: Copies `Items.data` from `FindMy` Application cache and creates a csv record `Airtag.csv` for python main.py script to parse from.

    - How it Works: The application's cache temporary storage of the airtag data is overwritten when updates occur from either `Crowd Sourcing` or `Owner` connection to the airtag in a nearby vacinity. `Crowd Sourcing` updates only occur if an Iphone user is within 100ft and has both `bluetooth` and `FindMy` enabled. 

### Python
- `AirTag`: Represents an Airtag object with methods for converting data to JSON.
- `Airtags`: Retrieves unique data points from the Airtags CSV file.
- `Route`: Fetches route data using the Google Maps Route API.
- `Geocoding`: Fetches coordinates based on a street address using the Google Maps Geocoding API.
- `BusStop`: Represents a bus stop object with relevant information.
- `BusRoute`: Predicts the shuttle bus route and retrieve arrival time for each shuttle bus
- `StopPredictor`: Predicts the next bus stop based on current location, previous route, and other factors.

## Limitations

- Updates: Airtag updates occur on average every 3 minutes. Outliers do occur and gaps up to 15 minutes can occur when lack of crowd sorucing.

## Contributions

If you would like to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.
