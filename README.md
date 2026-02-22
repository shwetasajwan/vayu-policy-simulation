# VAYU — Scenario-Based Policy Simulation System

ML-powered decision-support product enabling pre-implementation AQI intervention modelling for urban governance.

## 🚀 Overview

Vayu is a scenario-based simulation product designed to shift urban air quality governance from reactive monitoring to proactive modelling.

It enables decision-makers to:

- Adjust traffic reduction intensity  
- Activate construction bans  
- Combine intervention scenarios  
- Instantly view projected AQI changes  
- Evaluate regulatory category shifts (e.g., Severe → Very Poor)

Built as an exploratory product case study on embedding predictive intelligence into urban decision-making systems.

## 🧠 System Architecture

Vayu operates across three layers:

1. **Data Layer**  
   Historical multi-station AQI + weather dataset (~200K observations)

2. **ML Engine**  
   Random Forest regression model trained to capture nonlinear pollution dynamics

3. **Simulation Layer**  
   Intervention scaling logic that recalculates AQI predictions in real-time based on user inputs

This layered structure ensures prediction stability under intervention scenarios.

## 📊 Model Details

- Dataset: 200K+ observations across 23 monitoring stations  
- Time Range: ~6 years historical AQI data  
- Model: Random Forest Regressor  
- R²: 0.96  
- MAE: 24.7 AQI points  

The simulation engine recalculates AQI predictions under modified intervention inputs using structured scenario scaling logic.

## Product Interface
<img width="1876" height="849" alt="image" src="https://github.com/user-attachments/assets/95f50dc6-3029-4b16-9738-094178912a2e" />

Interactive sliders enable rapid scenario exploration under seasonal constraints, supporting fast comparison of intervention strategies.

## Tech Stack

- Python  
- Scikit-learn  
- Pandas  
- NumPy  
- Gradio (Blocks Interface)  
- Matplotlib  
- Plotly  
- Seaborn  
- FPDF2  

## Future Improvements

- Real-time AQI API integration  
- Multi-city support  
- Uncertainty band visualization  
- Health impact overlay  
- Cross-border pollution modelling  

## 💡 Key Insight

Decision clarity and threshold visibility mattered more than marginal predictive accuracy.

## ▶️ Running the Application

To run the application locally:
1. Open model_training.ipynb
2. Run all cells to generate:
   - aqi_prediction_model.pkl
   - season_encoder.pkl
   - dow_encoder.pkl
   - model_features.pkl
3. Then run app.py

© 2026 Shweta Sajwan. Shared for portfolio and research purposes.

