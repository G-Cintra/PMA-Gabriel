# Applied Macroeconometrics and Computational Economics – UDESC

This repository hosts the **open-source code** developed by the **Applied Macroeconometrics and Computational Economics Study Group**, part of the **Undergraduate Economics Program** at **UDESC University**, Brazil.

## 📚 About

The goal of this repository is to consolidate and share computational tools, simulation models, empirical analysis, and other resources related to applied macroeconometrics and computational economics, created by students and collaborators of the study group.

The group is dedicated to the practical exploration of economic models using modern computational techniques, with a strong focus on open science and collaborative development.

## 📅 Status

- **Repository created:** March 2025  
- **Current status:** Under active development  
- **Contributions:** Open to members of the study group. Future contributions from the broader community may be welcomed as the project evolves.

## 📓 Notebooks

This repository contains Jupyter notebooks developed by us. Each notebook serves as a self-contained tool as detailed below.

### Data Retrieval Interfaces

- [BCB - Brazilian Central Bank](./notebooks/BCB.ipynb)
- [IBGE - Brazilian Institute of Geography and Statistics](./notebooks/IBGE.ipynb)
- [FRED - US Federal Reserve Economic Data ](./notebooks/FRED.ipynb)

These notebooks provides a user-friendly interface for retrieving time series data from the BCB, IBGE and FRED. It enables users to:

- Select a macroeconomic time series from a curated list
- Define a custom date range for data retrieval
- Automatically log all activity for transparency and debugging
- Save the resulting dataset with a unique filename and hash for reproducibility
- Visualize the data directly within the notebook using Seaborn

The notebook is designed to ensure data integrity, traceability, and ease of use, especially for academic or research purposes.

### [GDP Filtering Notebook](./notebooks/Filtering.ipynb)

This notebook scans the data/raw/ folder to identify the **latest available PIB (GDP) series** downloaded from IBGE.  
It matches each file to its metadata and presents an interface where users can select between:

- Real or Nominal GDP  
- Seasonally Adjusted or Not  
- Quarterly or Annual Frequency  

Once a series is selected, the notebook applies a series of common transformations and filters used in macroeconomic analysis, including:

- Log transformation (NumPy)
- First difference and percentage change (pandas)
- HP, Baxter-King, and Christiano-Fitzgerald filters (statsmodels)

These operations rely on well-established Python libraries and provide an interactive interface for visual exploration of trends and cycles in GDP data.

> Additional notebooks will be added as the project evolves.


## ⚙️ Dependencies

All required Python packages for this project are listed in the `requirements.txt` file. This ensures consistent environments across different machines and collaborators.

We recommend using a **virtual environment** (e.g., `venv`) to isolate project dependencies.

To install all required packages, run:

```
pip install -r requirements.txt
```
## 📄 License

This project is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](license) file for more details.

## 🤝 Acknowledgments

This initiative is part of the academic activities within the Economics undergraduate program at UDESC (Universidade do Estado de Santa Catarina).

---

> For more information or to get involved, please open an issue in the repository.
