from flask_cors import CORS, cross_origin
import logging
from flask import Flask, make_response, request, jsonify, render_template 
from webhook import processRequest
from db import  get_categorias, set_proyecto, get_project
from webhook import get_query_results, get_textual_query_results
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Esta ruta es para escuchar las peticiones de Dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin(supports_credentials=True)
def webhook():
    req = request.get_json(silent=True, force=True)
    logging.debug(f"Requer:{req}")
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/get_project', methods=['GET'])
def get_project_route():
    project = get_project()
    logging.debug(f"project:{project}")
    return jsonify(project)

#Esta ruta carga las categorias en la pantalla de inicio
@app.route('/load_data', methods=['GET'])
def load_data():
    # Perform the specific query
    distinct_values = get_categorias()
    return jsonify(distinct_values)

@app.route('/get_query_results', methods=['GET'])
def get_query_results_endpoint():
    query_results = get_query_results()
    print('llegamos aca ome')
    print(query_results)
    print('llegamos aca omeEEEEEE')
    return jsonify(query_results)

@app.route('/get_textual_query_results', methods=['GET'])
def get_textual_query_results_endpoint():
    textual_query_results = get_textual_query_results()
    print('llegamos aca ome')
    print(textual_query_results)
    print('llegamos aca omeEEEEEE')
    return jsonify(textual_query_results)

@app.route('/')
def chatbot_ui():
    set_proyecto(0)
    return render_template('chatbot.html')

# Process a request from Dialogflow


