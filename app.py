from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    new_event = Event(
        id=len(events) + 1,
        title=data["title"]
    )

    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    event_list = [event.to_dict() for event in events]
    return jsonify(event_list), 200


# Get one event by ID
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = next((event for event in events if event.id == event_id), None)

    if event:
        return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# Update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    event = next((event for event in events if event.id == event_id), None)

    if event:
        event.title = data["title"]
        return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events

    event = next((event for event in events if event.id == event_id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events = [event for event in events if event.id != event_id]

    return jsonify({"message": "Event deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)