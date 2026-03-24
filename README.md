# Python Control Panel - Vehicle Data Analysis

A comprehensive Streamlit web application for interactive analysis and visualization of US vehicle data. This data science project provides real-time insights into vehicle characteristics, market trends, and comparative analysis across manufacturers.

## 📋 Project Overview

This control panel allows users to explore and visualize vehicle data through an intuitive interactive dashboard. It enables quick filtering, aggregation, and statistical analysis of vehicle information including brand, type, condition, model year, and pricing.

## ✨ Features

- **Data Viewer**: Browse and filter vehicle data with dynamic filtering options
  - Filter vehicles by manufacturer with a threshold toggle (less than 100 ads)
  - Interactive data table display
  
- **Manufacturer Analysis**: Stacked bar chart visualization
  - Compare vehicle types across manufacturers
  - View distribution of vehicle models by brand
  
- **Temporal Analysis**: Vehicle condition trends over time
  - Line chart showing condition distribution by model year
  - Stacked area visualization for aggregate insights
  
- **Price Comparison**: Comparative analysis tool
  - Select and compare price distributions between two manufacturers
  - Identify market positioning and pricing strategies

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone or download this project
2. Create and activate a virtual environment:
   ```bash
   python -m venv vehicles_env
   source vehicles_env/Scripts/activate  # On Windows
   source vehicles_env/bin/activate      # On macOS/Linux
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit development server:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Data Source

- **File**: `vehicles_us.csv`
- **Contents**: US vehicle data with attributes including:
  - Model, brand, type, year, condition, price, etc.
  
## 🛠️ Tech Stack

- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Advanced interactive visualizations
- **NumPy/SciPy**: Statistical analysis
- **Python**: Core programming language

## 📁 Project Structure

```
Python_Control_Panel/
├── app.py                  # Main Streamlit application
├── vehicles_us.csv         # Dataset
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── vehicles_env/          # Virtual environment
└── notebooks/
    └── EDA.ipynb          # Exploratory Data Analysis notebook
```

## 📝 Key Functions

- **Brand Extraction**: Automatically extracts brand name from vehicle model
- **Conditional Filtering**: Filter data based on advertisement volume thresholds
- **Interactive Charts**: Dynamic visualizations with hover information
- **Session State Management**: Persistent selection handling across user interactions

## 🔧 Configuration

The application uses the following Streamlit configurations:
- Wide layout (80rem max-width)
- Responsive design for different screen sizes
- Interactive buttons and select dropdowns for user input

## 📚 Exploratory Data Analysis

Additional analysis and data exploration can be found in the `notebooks/EDA.ipynb` Jupyter notebook.

## 💡 Usage Tips

- Use the checkbox to toggle filtering of manufacturers with fewer than 100 listings
- Clear selections with the "Clear" buttons for refined comparisons
- Hover over charts for detailed data points and statistics
- Sort manufacturer comparisons by total descending order

## 📄 License

This project is part of a data science course (Sprint 7).

## 👤 Author

Jose Cabrera

---

**Last Updated**: March 2026
