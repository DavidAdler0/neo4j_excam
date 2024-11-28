from flask import Blueprint, request, jsonify, current_app
from service.neo4j_service import ConversationRepository

phone_blueprint = Blueprint('phone', __name__, url_prefix='/api')


@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   data = request.get_json()
   try:
      repo = ConversationRepository(current_app.neo4j_driver)
      conversation_data = data['interaction']
      idx = 1
      for device in data['devices']:
         location = device.pop('location')
         for key, value in location.items():
            device[key] = value
            repo.create_device(device)
         idx += 1

      print("successfully created two devices")
      repo.create_connected_relationship(conversation_data)

   except Exception as e:
      print(e)
      return jsonify({'error': str(e)})

@phone_blueprint.route("/strong_signal", methods=['GET'])
def get_strong_signal_devices():
   try:
      repo = ConversationRepository(current_app.neo4j_driver)
      res = repo.find_strong_signal()
      devices = []
      for record in res:
         for node in record:
            devices.append(dict(node))

      return jsonify({"list of devices": devices}), 200
   except Exception as e:
      print(e)
      return jsonify({'error': str(e)}), 500

@phone_blueprint.route("/connections/<device_id>", methods=['GET'])
def get_connection_count(device_id):
   try:
      repo = ConversationRepository(current_app.neo4j_driver)
      res = repo.find_strong_signal()
      print(res)
      return jsonify(dict(res)), 200
   except Exception as e:
      print(e)
      return jsonify({'error': str(e)}), 500

