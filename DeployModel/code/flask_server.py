import flask
from flask import jsonify, request
from flask_cors import CORS
import os
import json
from flask_main import *
from show_path import *
import random
import math
import numpy as np
from Class import *
from LR import LR
import time
import sys

app = flask.Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/test', methods = ['GET'])
def test():
	return 'test'

@app.route('/getAdjMatrix', methods = ['GET'])
def get_adj_matrix():
	if os.path.exists('adjacency.csv'):
		adjacency_matrix = []
		file = open('adjacency.csv')
		all_rows = file.readlines()
		for row in all_rows:
			row = row[:-1].split(',')
			for i in range(len(row)):
				row[i] = int(row[i])
			adjacency_matrix.append(row)
		file.close()
		return jsonify(adjacency_matrix)
	else:
		return jsonify({'matrix': []})

@app.route('/getJsonLink/<json_file>', methods = ['GET'])
def get_json_link(json_file):
	if os.path.exists('link.csv'):
		links = []
		file = open('link.csv')
		link_list = file.readlines()
		link_list = link_list[1:]
		for link in link_list:
			link = list(map(int, (link[: -1]).split(',')))[1: ]
			links.append(link)
		file.close()

		if os.path.exists(f'path/{json_file}'):
			file = open(f'path/{json_file}')
			path = file.read()
			path = json.loads(path)
			methods = []
			keys = path.keys()
			for key in keys:
				methods.append(path[key])
			return jsonify({'link': links, 'path': methods})

@app.route("/CalPath", methods = ["POST"])
def calculate_path():
	data = request.json
	try:
		response = run_deploy(int(data["iter_times"]), int(data["startID"]), int(data["destID"]), data["config_loc"])
		if response == "success":
			show_path(data["config_loc"])
			return response
		else:
			return response
	except Exception as e:
		print(e)
		return "Something Wrong"

app.run()