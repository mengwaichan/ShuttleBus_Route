#!/bin/bash

ITEMS_FILE="./Items.data"
CSV_FILE="./Airtags.csv"
CSV_HEADER="datetime,name,batterystatus,locationpositiontype,locationlatitude,locationlongitude,addressstreetaddress,addressstreetname,addressareaofinteresta,addressareaofinterestb"
# Insert firebase info for manual scripting 
# API_KEY= ""
# PROJECT_ID= ""
# FIREBASE_URL_BASE="https://firestore.googleapis.com/v1/projects/$PROJECT_ID/databases/(default)/documents"

copy_items_data() {
    echo "Creating a copy of Items.data to prevent potential file corruption"
    if ! cp -p ~/Library/Caches/com.apple.findmy.fmipcore/Items.data "$ITEMS_FILE"; then
        echo "Failed to copy Items.data file. Please ensure Terminal has 'Full Disk Access' in the 'Privacy & Security' section in macOS Preferences" >&2
        exit 1
    fi
}

create_csv_file() {
    echo "Checking if $CSV_FILE exists"
    if [ ! -f "$CSV_FILE" ]; then
        echo "$CSV_FILE does not exist, creating one"
        if ! echo "$CSV_HEADER" >> "$CSV_FILE"; then
            echo "Failed to create $CSV_FILE. Please ensure the destination directory is writable." >&2
            exit 1
        fi
    fi
}

while true; do
    copy_items_data
    create_csv_file

    echo "Checking number of Airtags to process"
    airtagsnumber=$(jq ".[].serialNumber" "$ITEMS_FILE" | wc -l)
    echo "Number of Airtags to process: $airtagsnumber"
    airtagsnumber=$((airtagsnumber-1))

    for j in $(seq 0 "$airtagsnumber"); do
        echo "Processing airtag number $j"

        datetime=$(date +"%Y-%m-%d  %T")
        name=$(jq -r ".[$j].name" "$ITEMS_FILE")
        sanitized_name=$(echo "$name" | tr ' ' '_')
        FIREBASE_URL="$FIREBASE_URL_BASE/$sanitized_name"
        batterystatus=$(jq -r ".[$j].batteryStatus" "$ITEMS_FILE")

        if [[ $batterystatus =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            batterystatus_json="\"integerValue\":$batterystatus"
        else
            batterystatus_json="\"stringValue\":\"$batterystatus\""
        fi

        locationpositiontype=$(jq -r ".[$j].location.positionType" "$ITEMS_FILE")
        locationlatitude=$(jq -r ".[$j].location.latitude" "$ITEMS_FILE")
        locationlongitude=$(jq -r ".[$j].location.longitude" "$ITEMS_FILE")
        addressstreetaddress=$(jq -r ".[$j].address.streetAddress // \"\"" "$ITEMS_FILE")
        addressstreetname=$(jq -r ".[$j].address.streetName // \"\"" "$ITEMS_FILE")
        addressareaofinteresta=$(jq -r ".[$j].address.areaOfInterest[0] // \"\"" "$ITEMS_FILE")
        addressareaofinterestb=$(jq -r ".[$j].address.areaOfInterest[1] // \"\"" "$ITEMS_FILE")

        echo "Writing data to $CSV_FILE"
        echo "$datetime","$name", "$batterystatus", "$locationpositiontype", "$locationlatitude", "$locationlongitude", "$addressstreetaddress", "$addressstreetname", "$addressareaofinteresta","$addressareaofinterestb" >> "$CSV_FILE"

        # uncomment to send to firebase directly
        # data_to_send_json="{
        #     \"fields\": {
        #         \"datetime\": {\"stringValue\": \"$datetime\"},
        #         \"name\": {\"stringValue\": \"$name\"},
        #         \"batterystatus\": {$batterystatus_json},
        #         \"locationpositiontype\": {\"stringValue\": \"$locationpositiontype\"},
        #         \"locationlatitude\": {\"doubleValue\": $locationlatitude},
        #         \"locationlongitude\": {\"doubleValue\": $locationlongitude},
        #         \"addressstreetaddress\": {\"stringValue\": \"$addressstreetaddress\"},
        #         \"addressstreetname\": {\"stringValue\": \"$addressstreetname\"},
        #         \"addressareaofinteresta\": {\"stringValue\": \"$addressareaofinteresta\"},
        #         \"addressareaofinterestb\": {\"stringValue\": \"$addressareaofinterestb\"}
        #     }
        # }"

        # echo "Sending data to Firebase"
        # curl -X POST "$FIREBASE_URL?key=$API_KEY" \
        #     -H "Content-Type: application/json" \
        #     -d "$data_to_send_json"

    done
    echo -e "Checking again in 1 minute...\n"
    sleep 60

done