from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "map_data.json"

# Load existing data or create new
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"points": [], "paths": []}

def save_data():
    """Save updated points and paths to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    """Fetch points and paths from file"""
    return jsonify(data)

@app.route('/add_point', methods=['POST'])
def add_point():
    """Add a new point"""
    new_point = request.json
    data["points"].append(new_point)
    save_data()
    return jsonify({"message": "Point added successfully", "data": data})

@app.route('/add_path', methods=['POST'])
def add_path():
    """Create a path between two points"""
    new_path = request.json
    data["paths"].append(new_path)
    save_data()
    return jsonify({"message": "Path added successfully", "data": data})

@app.route('/delete_point', methods=['POST'])
def delete_point():
    """Delete a point and remove related paths"""
    point_name = request.json.get("name")
    
    # Remove the point
    data["points"] = [p for p in data["points"] if p["name"] != point_name]
    
    # Remove paths connected to the deleted point
    data["paths"] = [path for path in data["paths"] if path["start"]["name"] != point_name and path["end"]["name"] != point_name]

    save_data()
    return jsonify({"message": f"Point '{point_name}' deleted!", "data": data})

@app.route('/delete_path', methods=['POST'])
def delete_path():
    """Delete a path between two points"""
    start_name = request.json.get("start")
    end_name = request.json.get("end")

    # Remove the specific path
    data["paths"] = [path for path in data["paths"] if not (path["start"]["name"] == start_name and path["end"]["name"] == end_name)]
    
    save_data()
    return jsonify({"message": f"Path from '{start_name}' to '{end_name}' deleted!", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
