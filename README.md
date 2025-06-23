# UDISE Data Analysis

This project provides tools and scripts for analyzing UDISE (Unified District Information System for Education) data, including statistical analysis, geospatial processing, and reporting.

## Project Structure

- `src/` — Main analysis scripts
- `src/utils/` — Utility modules (CSV helpers, geometry functions, etc.)
- `data/` — Input data files (CSV, GeoJSON, etc.)
- `output/` — Output files (results, processed data)
- `Averages/` — Scripts for average calculations
- `Shapefiles/` — GIS shapefiles for mapping
- `notebooks/` — Jupyter notebooks for exploration and prototyping
- `config.py` — Central configuration for file paths and parameters

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/DevanshSharma867/UDISE-data-analysis.git
   cd UDISE-data-analysis
   ```
2. **Install dependencies:**
   - This project uses only standard Python libraries, but for geospatial or data science tasks, you may need:
     ```sh
     pip install -r requirements.txt
     ```
3. **Prepare your data:**
   - Place all input files (CSVs, GeoJSONs, etc.) in the `data/` directory.
   - Update `config.py` with correct file paths and parameters as needed.

4. **Run analysis scripts:**
   - From the `src/` directory, run scripts as needed, for example:
     ```sh
     python src/qgis.py
     ```

## Features
- Statistical analysis of UDISE data
- Calculation of means, medians, and similarities
- Geospatial processing and mapping
- Modular utility functions for CSV and geometry operations
- Output generation for QGIS and other tools

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements
- UDISE+ data and documentation
- Python open-source community
