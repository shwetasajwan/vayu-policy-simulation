# ==============================
# PHASE 3: SCENARIO SIMULATION
# ==============================

import pandas as pd
import numpy as np
import pickle

# Load dataset
df = pd.read_csv("delhi_ncr_aqi_dataset.csv")

# Load model and encoders
with open("aqi_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("season_encoder.pkl", "rb") as f:
    le_season = pickle.load(f)
with open("dow_encoder.pkl", "rb") as f:
    le_dow = pickle.load(f)
with open("model_features.pkl", "rb") as f:
    features = pickle.load(f)

print("Model loaded successfully.")


# ==============================
# TRAFFIC REDUCTION SIMULATION
# ==============================

def simulate_traffic_reduction(row, reduction_percent):
    row = row.copy()

    row["season_encoded"] = le_season.transform([row["season"]])[0]
    row["dow_encoded"] = le_dow.transform([row["day_of_week"]])[0]

    baseline_input = pd.DataFrame([row[features]])
    baseline_aqi = model.predict(baseline_input)[0]

    lockdown_traffic_drop = 80
    lockdown_aqi_improvement = 50

    scaled_improvement = (reduction_percent / lockdown_traffic_drop) * lockdown_aqi_improvement
    scaled_improvement = min(scaled_improvement, 50)

    adjusted_aqi = baseline_aqi * (1 - scaled_improvement / 100)

    return round(baseline_aqi, 2), round(adjusted_aqi, 2), round(scaled_improvement, 2)


# ==============================
# CONSTRUCTION BAN SIMULATION
# ==============================

def simulate_construction_ban(row):
    row = row.copy()

    row["season_encoded"] = le_season.transform([row["season"]])[0]
    row["dow_encoded"] = le_dow.transform([row["day_of_week"]])[0]

    baseline_input = pd.DataFrame([row[features]])
    baseline_aqi = model.predict(baseline_input)[0]

    # Construction ban reduces PM10 (dust) by ~15% AQI improvement
    construction_improvement = 15
    adjusted_aqi = baseline_aqi * (1 - construction_improvement / 100)

    return round(baseline_aqi, 2), round(adjusted_aqi, 2), construction_improvement


# ==============================
# COMBINED SCENARIO SIMULATION
# ==============================

def simulate_combined(row, traffic_reduction_percent):
    row = row.copy()

    row["season_encoded"] = le_season.transform([row["season"]])[0]
    row["dow_encoded"] = le_dow.transform([row["day_of_week"]])[0]

    baseline_input = pd.DataFrame([row[features]])
    baseline_aqi = model.predict(baseline_input)[0]

    lockdown_traffic_drop = 80
    lockdown_aqi_improvement = 50

    traffic_improvement = (traffic_reduction_percent / lockdown_traffic_drop) * lockdown_aqi_improvement
    traffic_improvement = min(traffic_improvement, 50)

    construction_improvement = 15

    # Combined effect with diminishing returns
    total_improvement = traffic_improvement + construction_improvement * (1 - traffic_improvement / 100)
    total_improvement = min(total_improvement, 60)

    adjusted_aqi = baseline_aqi * (1 - total_improvement / 100)

    return round(baseline_aqi, 2), round(adjusted_aqi, 2), round(total_improvement, 2)


# ==============================
# TEST 1: CURRENT CONDITIONS
# ==============================

current_row = df.iloc[-1].copy()

print("\nCurrent Conditions Simulation")
print("-" * 40)

for reduction in [10, 30, 50, 70]:
    baseline, adjusted, improvement = simulate_traffic_reduction(current_row, reduction)
    print(f"\nTraffic Reduction : {reduction}%")
    print(f"Baseline AQI      : {baseline}")
    print(f"Adjusted AQI      : {adjusted}")
    print(f"Improvement       : {improvement}%")


# ==============================
# TEST 2: WINTER vs SUMMER
# ==============================

winter_sample = df[df["season"] == "winter"].iloc[0].copy()
summer_sample = df[df["season"] == "summer"].iloc[0].copy()

print("\nWinter Scenario (30% Reduction)")
print("-" * 40)
b, a, i = simulate_traffic_reduction(winter_sample, 30)
print(f"Baseline   : {b}")
print(f"Adjusted   : {a}")
print(f"Improvement: {i}%")

print("\nSummer Scenario (30% Reduction)")
print("-" * 40)
b, a, i = simulate_traffic_reduction(summer_sample, 30)
print(f"Baseline   : {b}")
print(f"Adjusted   : {a}")
print(f"Improvement: {i}%")


# ==============================
# TEST 3: ALL SCENARIOS COMPARED
# ==============================

print("\nFull Scenario Comparison (Winter, 30% Traffic)")
print("-" * 50)

b1, a1, i1 = simulate_traffic_reduction(winter_sample, 30)
b2, a2, i2 = simulate_construction_ban(winter_sample)
b3, a3, i3 = simulate_combined(winter_sample, 30)

print(f"Baseline AQI               : {b1}")
print(f"Traffic 30% only           : {a1}  ({i1}% improvement)")
print(f"Construction ban only      : {a2}  ({i2}% improvement)")
print(f"Traffic 30% + Construction : {a3}  ({i3}% improvement)")