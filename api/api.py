import json
from flask import Flask, request, jsonify

from game import Grid
from solver import Solver

'''
    Simple api to interact with the Sudoku solver.
    For simplicity, the api reads and writes to a json file
    rather than using a database.

    Summary of functionality:
        GET /api
            return a list of valid ids
            
        POST /api/new?size=<size>
            start a new game with given size, return newly registered id

        GET /api/<grid_id>
            return the repr for the grid with given id

        DELETE /api/<grid_id>
            delete the grid with the given id

        POST /api/<grid_id>/load?difficulty=<difficulty>
            for the given grid id, load the saved example for the given difficulty
        
        POST /api/<grid_id>/solve
            solve the grid with the given id, return the repr of solved grid
'''

app = Flask(__name__)
grid_data = json.load(open('api/game_data.json'))

def save_data():
    with open('api/game_data.json', 'w') as outfile:
        json.dump(grid_data, outfile)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/', methods=['GET'])
def home():
    return 'API for Sudoku solver'

@app.route('/api', methods=['GET'])
def api_root():
    ids = []
    for grid_id in grid_data:
        if grid_data[grid_id]:
            ids.append(grid_id)
    return jsonify(ids)

@app.route('/api/new', methods=['POST'])
def new():
    "Start a new game and register a new id"
    grid_id = str(len(grid_data))
    size = int(request.args['size'])
    grid = Grid(size)

    grid_data[grid_id] = repr(grid)
    save_data()

    return grid_id

@app.route('/api/<grid_id>', methods=['GET', 'DELETE'])
def get_grid(grid_id):
    "Get or delete the grid for the given id"
    if grid_id not in grid_data or grid_data[grid_id] == None:
        return 'invalid id', 403
    
    if request.method == 'GET':
        return grid_data[grid_id]
    elif request.method == 'DELETE':
        grid_data[grid_id] = None
        save_data()
        return f'deleted id {grid_id}'
    else:
        return 'invalid id', 403

@app.route('/api/<grid_id>/load', methods=['POST'])
def load(grid_id):
    "Load game state from examples"
    difficulty = request.args['difficulty']

    if grid_id not in grid_data or grid_data[grid_id] == None:
        return 'invalid id', 403

    grid = Grid(load_from=grid_data[grid_id])
    grid.read_file(f'examples/{grid.box_len}/{difficulty}.txt')

    grid_data[grid_id] = repr(grid)
    save_data()

    return 'loaded'

@app.route('/api/<grid_id>/solve', methods=['POST'])
def solve(grid_id):
    "Solve the grid for the given id"
    if grid_id not in grid_data or grid_data[grid_id] == None:
        return 'invalid id', 403

    grid = Grid(load_from=grid_data[grid_id])
    solver = Solver(grid)
    solver.solve()

    grid_data[grid_id] = repr(grid)
    save_data()

    return repr(grid)

def run():
    app.run()
