from flask import Flask, request, jsonify

app = Flask(__name__)

# Memoria en tiempo de ejecución para la configuración
config_data = []

@app.route('/config', methods=['PUT'])
def set_config():
    global config_data
    payload = request.get_json(force=True)
    if not isinstance(payload, list):
        return jsonify({'success': False, 'error': 'Se requiere un array de objetos'}), 400

    for item in payload:
        if not isinstance(item, dict):
            return jsonify({'success': False, 'error': 'Formato de objeto inválido'}), 400
        required = {'id', 'logic_positive', 'detection_always', 'linked_outputs'}
        if not required.issubset(item.keys()):
            return jsonify({'success': False, 'error': 'Faltan campos requeridos en algún objeto'}), 400
        if not isinstance(item['id'], int) or not isinstance(item['logic_positive'], bool) or not isinstance(item['detection_always'], bool) or not isinstance(item['linked_outputs'], list):
            return jsonify({'success': False, 'error': 'Tipo de dato inválido en algún campo'}), 400

    config_data = payload
    return jsonify({'success': True, 'message': 'Configuración guardada'}), 200

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(config_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
