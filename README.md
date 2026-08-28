# THERMALYTIC AI

## Heat-Aware Operations Intelligence

THERMALYTIC AI is a thermal intelligence and operational decision-support platform that transforms real thermal data from the FortyGuard Temperature API into explainable risk assessments, hotspot insights, operational recommendations, and interactive 3D thermal visualization.

## 🚀 Live Demo

https://thermalytic-ai.streamlit.app/

## 💻 GitHub

https://github.com/sriharshamagapu/THERMALYTIC-AI

---

## 🎯 Problem

Outdoor operations can be significantly affected by high thermal exposure.

Raw temperature information alone does not provide enough operational context to answer:

- Where is thermal exposure concentrated?
- How severe is the current thermal risk?
- Are there thermal hotspots?
- What operational action should be considered?
- When should demanding outdoor activities be scheduled?

THERMALYTIC AI bridges the gap between thermal intelligence and operational decision-making.

---

## 💡 Solution

THERMALYTIC AI combines real FortyGuard thermal intelligence with an explainable thermal analysis and operational recommendation pipeline.

Users configure:

- Operation type
- Analysis date
- Analysis time
- Operational area
- Center latitude and longitude
- Area width and height

The platform sends the configured analysis request to the FortyGuard Temperature API, receives real thermal cells, analyzes the returned temperature data, and converts the results into operational decision support.

---

## 🔥 Key Features

### Real FortyGuard Thermal Intelligence

Uses the FortyGuard Temperature API as the real thermal data source rather than simulated temperature data.

### Thermal Exposure Analysis

Analyzes returned thermal cells to calculate:

- Minimum temperature
- Maximum temperature
- Mean temperature
- Temperature difference

### Risk Assessment

THERMALYTIC AI evaluates thermal exposure and produces a standardized operational risk assessment.

Example:

**MODERATE RISK**

### Hotspot Detection

Analyzes thermal cells to identify potential thermal hotspots using the ThermalAnalyzer.

### Explainable Decision Intelligence

The platform explains the factors contributing to the current thermal assessment, including:

- Mean temperature
- Maximum temperature
- Thermal hotspots
- Temperature range
- Overall thermal exposure

### Operational Recommendations

The Operations Recommender converts the thermal assessment into practical operational guidance.

Example:

> Schedule demanding field activities during cooler periods and use work-rest planning.

### Interactive 3D Thermal Environment

Provides an interactive 3D visualization of the returned FortyGuard thermal cells.

Users can explore the thermal environment and inspect individual cells.

---

## 🧠 How It Works

```text
Operational Planning
        ↓
Area + Date + Time
        ↓
FortyGuard Temperature API
        ↓
Real Thermal Cells
        ↓
ThermalAnalyzer
        ↓
Temperature Exposure
Hotspot Detection
Risk Classification
Risk Score
        ↓
Decision Intelligence
        ↓
Operations Recommender
        ↓
Operational Recommendation
        ↓
Interactive 3D Thermal Environment