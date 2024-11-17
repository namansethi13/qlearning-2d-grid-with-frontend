# Q-Learning Agent Interactive Web Interface

This project allows you to interact with a Q-Learning model via a web interface. It includes both a backend (Flask API) and a frontend (web interface) to visualize and interact with the model.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used) 
- [Setup Instructions](#setup-instructions)
 - [Frontend](#frontend)
 - [Backend](#backend)
- [Running the Application](#running-the-application)
- [Interacting with the Model](#interacting-with-the-model)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a Q-Learning agent that interacts with an environment grid. The environment contains rewards and obstacles. The agent learns how to navigate the grid to reach the goal state by exploring actions like moving up, down, left, or right.

- **Frontend**: The user interface is built with Svelte, which allows interaction with the Q-Learning model, including setting the grid environment, starting state, and goal state.
- **Backend**: The backend is built using Flask and serves the Q-Learning algorithm. It processes inputs from the frontend, runs the Q-Learning algorithm, and returns the results.

## Technologies Used

- **Frontend**: Svelte, HTML, CSS (Tailwind)
- **Backend**: Flask (Python)
- **Machine Learning**: Q-Learning (NumPy)

## To run the project 
python app.py 
npm i
cd frontend
npm run dev


Make changes and commit them (git commit -am 'Add new feature'). Push to the branch (git push origin feature-branch). 
