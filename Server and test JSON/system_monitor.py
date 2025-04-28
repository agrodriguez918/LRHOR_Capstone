from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = "LRH_Dashboard.json"
lock = threading.Lock()

def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

@app.route('/metrics', methods=['GET'])
def get_metrics():
    with lock:
        try:
            return jsonify(read_data())
        except json.JSONDecodeError as e:
            return jsonify({"error": "JSON decode error", "details": str(e)}), 500

@app.route('/adjust_staff', methods=['GET'])
def adjust_staff():
    room_id = int(request.args.get("room"))
    change = int(request.args.get("change", 0))

    with lock:
        data = read_data()
        for room in data:
            if room["rm_ID"] == room_id:
                room["staff_cnt"] += change
                if room["staff_cnt"] < 0:
                    room["staff_cnt"] = 0
                room["last_status_changed"] = timestamp()
                write_data(data)
                return jsonify({"room": room_id, "staff_cnt": room["staff_cnt"]})

    return jsonify({"error": "Room not found."}), 404

def terminal_input_loop():
    print("\nCommands:")
    print("  room <rm_ID> <+/-change>       → Adjust staff count")
    print("  set <ID> <field> <value>       → Update any field by ID")
    print("  exit                           → Quit the loop\n")

    while True:
        try:
            cmd = input("> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                print("Exiting input loop...")
                break

            if cmd.startswith("room "):
                _, room_str, change_str = cmd.split()
                room_id = int(room_str)
                change = int(change_str)

                with lock:
                    data = read_data()
                    for room in data:
                        if room["rm_ID"] == room_id:
                            room["staff_cnt"] += change
                            if room["staff_cnt"] < 0:
                                room["staff_cnt"] = 0
                            room["last_status_changed"] = timestamp()
                            write_data(data)
                            print(f"✅ Updated Room {room_id} → staff_cnt: {room['staff_cnt']}")
                            break
                    else:
                        print(f"❌ Room {room_id} not found.")

            elif cmd.startswith("set "):
                _, id_str, field, *value_parts = cmd.split()
                record_id = int(id_str)
                value = " ".join(value_parts)

                with lock:
                    data = read_data()
                    for row in data:
                        if row.get("ID") == record_id:
                            if field not in row:
                                print(f"❌ Field '{field}' not found in record.")
                                break
                            try:
                                if isinstance(row[field], int):
                                    value = int(value)
                                elif isinstance(row[field], float):
                                    value = float(value)
                            except:
                                pass

                            row[field] = value
                            row["last_status_changed"] = timestamp()
                            write_data(data)
                            print(f"✅ Updated ID {record_id} → {field} = {value}")
                            break
                    else:
                        print(f"❌ No record found with ID {record_id}")
            else:
                print("⚠️ Unknown command. Use 'room' or 'set'.")
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    terminal_input_loop()
