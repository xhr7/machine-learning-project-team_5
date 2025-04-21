#  Two-Stage Network Intrusion Detection System

This project implements a two-stage machine learning pipeline for detecting network intrusions.  

- **Stage 1:** An ANN-based binary classifier determines whether a given network flow is **benign or malicious**.  
- **Stage 2:** If a flow is flagged as malicious, a multi-class classifier identifies the specific **attack type** (from 14 possible categories).  

This two-step approach improves accuracy by first filtering out benign traffic and then performing detailed attack classification only on the suspicious flows.  

Developed by **Team 5** as part of an AI Bootcamp, the project covers the complete workflow — from data preprocessing and model training to deployment.  
It includes Jupyter notebooks for development, a ready-to-use **FastAPI backend**, and a **Streamlit frontend** for interacting with the system in real-time.

---

## 👥 Team Members

- Yousef Al‑Dayhan  
- Alhanouf Al‑Suwaid  
- Ezdhar Al‑Tamimi  
- Rahaf Masmali  
- Omar AlSuraia  

---

## Data Source

We used the **CyberBERT Dataset** from Hugging Face, which is derived from the **CICIDS2017 benchmark**.  
It provides rich network flow records for training and evaluating the IDS.

###  Key features of the dataset:
- Covers both benign and malicious network traffic  
- Includes multiple attack types: DoS, DDoS, PortScan, Infiltration, Botnet, and others  
- Contains detailed statistical features like flow duration, packet length, header size, etc.  
- Loaded directly using the Hugging Face `datasets` library  

---

## Project Structure

```plaintext
├── 01_project.ipynb      # Data cleaning, preprocessing, model training and evaluation
├── README.md             # Project overview and setup instructions (this file)
├── deployment/
│   ├── app.py            # Streamlit frontend
│   └── api.py            # FastAPI backend
├── models/               # Saved ML models (e.g., model_80.99.h5)
├── config.toml           # Configuration for Streamlit



----------------------------------



## Tools & Libraries

This project leverages a variety of tools and libraries in the Python ecosystem:

- **Python** – Programming language used for all project components  
- **pandas** – Data manipulation and analysis (handling DataFrames of network traffic features)  
- **numpy** – Numerical computations and array operations  
- **datasets (Hugging Face)** – Easy download and management of the CyberBERT dataset  
- **scikit-learn** – Data preprocessing (train/test splitting, scaling), and baseline models/metrics  
- **TensorFlow** – Building and training the Artificial Neural Network models (binary and multi-class)  
- **matplotlib & seaborn** – Plotting and visualizing data distributions, training progress, and evaluation results (e.g., confusion matrices)  
- **FastAPI** – Creating a RESTful API for serving the trained models (backend deployment)  
- **Streamlit** – Building an interactive web application frontend for live model interaction


## 🚀 Usage Instructions

Follow these steps to set up and run the project on your local machine:

###  1. Clone the Repository

```bash
git clone https://github.com/AI-bootcamp/machine-learning-project-team_5.git
cd machine-learning-project-team_5
```

###  2. Install Python Dependencies

Make sure you have Python 3.10+ installed.

You can install all the required Python packages with:

```bash
pip install -r requirements.txt
```

(Optional but recommended) create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

###  3. Run the Streamlit Frontend

In a terminal, run the Streamlit app with:

```bash
streamlit run deployment/app.py
```

This will start the **Streamlit web application** on your local machine.  
The Streamlit UI allows you to interact with the intrusion detection system — for example, you could upload or input network flow feature data and get a prediction (`Benign` or a specific attack type) from the model, along with visualizations.

###  4. Run the FastAPI Backend

In another terminal window, start the FastAPI server with Uvicorn:

```bash
uvicorn deployment.api:app --reload
```

This launches the **FastAPI backend** at `http://localhost:8000` by default.  
The `--reload` flag is helpful during development, as it automatically reloads the server upon code changes.

You can access the interactive API documentation via Swagger UI here:

👉 http://localhost:8000/docs

The FastAPI app provides endpoints for predictions and can be extended with additional functionality.

###  Important Notes

- Make sure both the **Streamlit frontend** and **FastAPI backend** are running simultaneously in separate terminal windows or processes.
- The Streamlit app is configured to communicate with the FastAPI backend to retrieve model predictions in real time.