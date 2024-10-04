from flask import Flask, render_template, jsonify
from utils.mbta_api import fetch_mbta_data, fetch_routes  
from utils.load_data import load_stops
import config

app = Flask(__name__)

# Load the stops data
stops_data = load_stops('data/stops.txt')  # Make sure the path is correct

@app.route('/')
def home():
    return render_template('index.html')

# debugging, green line not working
@app.route('/routes', methods=['GET'])
def get_routes():
    try:
        # Fetch all routes
        routes_data = fetch_routes()

        # Prepare a list of routes with their IDs and names
        routes_list = []
        for route in routes_data.get('data', []):
            routes_list.append({
                'id': route['id'],
                'name': route['attributes']['long_name']  # or 'short_name' depending on preference
            })

        return jsonify(routes_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mbta/<line>', methods=['GET'])
def get_train_updates(line):
    try:
        # Define Green Line routes
        green_line_routes = ['Green-B', 'Green-C', 'Green-D', 'Green-E']

        # If the line is Green, fetch data for all Green Line routes
        if line == 'Green':
            upcoming_trains = []
            for green_line in green_line_routes:
                data = fetch_mbta_data(green_line)

                # Iterate through the data to extract relevant information
                for prediction in data.get('data', []):
                    attributes = prediction.get('attributes', {})
                    relationships = prediction.get('relationships', {})
                    stop_data = relationships.get('stop', {}).get('data', {})
                    route_data = relationships.get('route', {}).get('data', {})

                    # Get the station name from the stops data
                    station_id = stop_data.get('id')
                    station_name = stops_data.get(station_id, "Unknown Station")

                    train_info = {
                        'arrival_time': attributes.get('arrival_time'),
                        'departure_time': attributes.get('departure_time'),
                        'status': attributes.get('status'),
                        'station': station_name,  # Use station name here
                        'route': route_data.get('id')  # Get route ID
                    }
                    upcoming_trains.append(train_info)

            return jsonify(upcoming_trains), 200
        else:
            # Fetch data for the requested metro line normally
            data = fetch_mbta_data(line)

            # Prepare a response list for upcoming trains
            upcoming_trains = []

            # Iterate through the data to extract relevant information
            for prediction in data.get('data', []):
                attributes = prediction.get('attributes', {})
                relationships = prediction.get('relationships', {})
                stop_data = relationships.get('stop', {}).get('data', {})
                route_data = relationships.get('route', {}).get('data', {})

                # Get the station name from the stops data
                station_id = stop_data.get('id')
                station_name = stops_data.get(station_id, "Unknown Station")

                train_info = {
                    'arrival_time': attributes.get('arrival_time'),
                    'departure_time': attributes.get('departure_time'),
                    'status': attributes.get('status'),
                    'station': station_name,  # Use station name here
                    'route': route_data.get('id')  # Get route ID
                }
                upcoming_trains.append(train_info)

            return jsonify(upcoming_trains), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# def get_train_updates(line):
    try:
        # Define a mapping for the Green Line to its route IDs
        green_line_routes = {
            'B': 'Green-B',
            'C': 'Green-C',
            'D': 'Green-D',
            'E': 'Green-E'
        }

        # Check if the line is Green and fetch corresponding route ID
        if line.startswith("Green"):
            route_id = green_line_routes.get(line[-1])  # Get the correct route ID
        else:
            route_id = line  # Use the line directly for other lines

        # Fetch data for the requested metro line
        data = fetch_mbta_data(route_id)

        # Prepare a response list for upcoming trains
        upcoming_trains = []

        # Check if data is empty
        if not data.get('data'):
            return jsonify({'error': 'No predictions available for this line'}), 404

        # Iterate through the data to extract relevant information
        for prediction in data.get('data', []):
            attributes = prediction.get('attributes', {})
            relationships = prediction.get('relationships', {})
            stop_data = relationships.get('stop', {}).get('data', {})
            route_data = relationships.get('route', {}).get('data', {})

            # Get the station name from the stops data
            station_id = stop_data.get('id')
            station_name = stops_data.get(station_id, "Unknown Station")

            train_info = {
                'arrival_time': attributes.get('arrival_time'),
                'departure_time': attributes.get('departure_time'),
                'status': attributes.get('status'),
                'station': station_name,  # Use station name here
                'route': route_data.get('id')  # Get route ID
            }
            upcoming_trains.append(train_info)

        return jsonify(upcoming_trains), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
