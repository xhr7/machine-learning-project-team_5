## Two-Stage Network Intrusion Detection System

This project implements a two-stage machine learning pipeline for detecting network intrusions. In the first stage, an ANN-based binary classifier determines whether a given network flow is benign or malicious.

If a flow is flagged as malicious, the second stage uses a multi-class classifier to identify the specific attack type (out of 14 possible categories).
This two-step approach improves accuracy by filtering out benign traffic first and then performing detailed attack classification on the suspicious traffic. Developed by Team 5 as part of an AI bootcamp, the project covers the entire workflow from data preprocessing and model training to deployment. We provide Jupyter notebooks for data handling and model development, as well as a ready-to-run FastAPI backend and Streamlit frontend for demonstrating the intrusion detection system in action.

# Team Members:

Yousef Al‑Dayhan
Alhanouf Al‑Suwaid
Ezdhar Al‑Tamimi
Rahaf Masmali
Omar AlSuraia
Data Source

We used the CyberBERT Dataset from Hugging Face as our source of network traffic data.

This dataset is derived from the well-known CICIDS2017 benchmark and provides extensive network flow records for training and evaluating the IDS.

# Key features of the dataset include:

A wide range of network traffic features for cybersecurity threat detection (e.g., packet lengths, flow durations, header sizes, etc.).
Both normal benign traffic and various attack types (e.g., DoS, PortScan, DDoS, Infiltration, Botnet, and more) are represented.

Each record corresponds to a single network flow with detailed statistical features, labeled as Benign or as one of 14 malicious attack categories.
We loaded the dataset directly using the Hugging Face datasets library,

# Project Structure

For clarity and modularity, our repository is organized as follows:
├── 01_project.ipynb # Data cleaning and preprocessing and Model training and evaluation notebook
├── README.md # Project overview and instructions (this file)

# Tools & Libraries

This project leverages a variety of tools and libraries in the Python ecosystem:
Python – Programming language used for all project components.
pandas – For data manipulation and analysis (handling data frames of network traffic features).
numpy – For numerical computations and array operations.
datasets (Hugging Face) – To easily download and manage the CyberBERT dataset.
scikit-learn – For data preprocessing (train/test splitting, scaling) and as a baseline for some models/metrics.
tensorflow – Used to build and train the Artificial Neural Network models for both binary and multi-class classification.
matplotlib & seaborn – For plotting and visualizing data distributions, training progress, and evaluation results (e.g., confusion matrices).
FastAPI – To create a RESTful API for serving the trained models (backend deployment).
Streamlit – To build an interactive web application as a frontend, allowing users to input data and see predictions in real time.
Make sure to install all these dependencies (listed in requirements.txt) before running the project.
Usage Instructions
Follow these steps to set up and run the project on your local machine:

# Clone the repository from GitHub

$ git clone https://github.com/AI-bootcamp/machine-learning-project-team_5.git

# Navigate into the project directory

$ cd machine-learning-project-team_5

# Install all required Python dependencies

$ pip install -r requirements.txt

To run the Streamlit frontend:
In a terminal, run the Streamlit app with:

$ streamlit run deployment/app.py
This will start the Streamlit web application on your local machine. The Streamlit UI allows you to interact with the intrusion detection system — for example, you could upload or input network flow feature data and get a prediction (Benign or specific attack type) from the model, with some nice visualizations.

To run the FastAPI backend:
In another terminal, start the FastAPI server with Uvicorn:

$ uvicorn deployment.api:app --reload
This launches the FastAPI backend at http://localhost:8000 (default). The --reload flag is useful during development, as it auto-reloads the server on code changes. The FastAPI app provides endpoints for predictions (and could be extended with more functionality). You can visit http://localhost:8000/docs to see the interactive API documentation (powered by Swagger UI) for testing the endpoints. The Streamlit frontend is configured to communicate with this backend to retrieve model predictions. Note: Ensure that both the Streamlit frontend and FastAPI backend are running simultaneously (in separate windows or processes). The Streamlit app will make requests to the FastAPI API to get predictions for input data.