from flask import Flask, request, jsonify
from server.main import QLearningAgent
from flask_cors import CORS 
import json

app = Flask(__name__)
agent = None

CORS(app)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Pong!'})

@app.route('/reset', methods=['GET'])
def reset():
    global agent
    agent = None
    return jsonify({'message': 'Agent reset successfully'})

@app.route('/' , methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Q-Learning API!'})

@app.route('/init', methods=['POST'])
def initialize():
    data = request.json
    global agent
    
    print(data)

    agent = QLearningAgent(
        discount_factor=data['discount_factor'],
        learning_rate=data['learning_rate'],
        grid_size= tuple(int(num) for num in data['grid_size']),
        environment=data['environment'],
        start_state=list(data['start_state']),
        goal_state=list(int(num) for num in data['goal_state'])
    )
    return jsonify({'message': 'Agent initialized successfully'})

@app.route('/train', methods=['POST'])
def train():
    episodes = request.json.get('episodes', 1000)
    q_table = agent.train(episodes)
    return jsonify({'message': 'Training complete', 'q_table': q_table.tolist()})

@app.route('/policy', methods=['GET'])
def policy():
    policy = agent.get_optimal_policy()
    return jsonify({'optimal_policy': policy})

if __name__ == '__main__':
    app.run(debug=True)
