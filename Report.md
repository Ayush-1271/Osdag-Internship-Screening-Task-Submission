# SFD and BMD Visualization Project

## Overview
This project processes NetCDF data (`screening_task.nc`) to visual Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for a bridge structure.

## Structure
*   `Task1/`: Contains script and output for 2D visualization of the central girder.
*   `Task2/`: Contains script and output for 3D visualization of the entire bridge.
*   `SFD_BMD_Central_Girder.html`: 2D interactive plots.
*   `3D_SFD_Bridge.html`: 3D SFD visualization.
*   `3D_BMD_Bridge.html`: 3D BMD visualization.

## How to Run: Step-by-Step Guide

Follow these instructions to set up and run the project from scratch.

### 1. Prerequisites (Setup)
Ensure you have Python installed. You can check by running `python --version` in your terminal.

### 2. Install Dependencies
Open your terminal (Command Prompt, PowerShell, or Terminal) and run the following command to install the required Python libraries:
```bash
pip install xarray netcdf4 plotly pandas numpy
```

### 3. Generate 2D Plots (Task 1)
To generate the Shear Force and Bending Moment Diagrams for the central longitudinal girder:
1.  Navigate to the project folder in your terminal.
2.  Run the following command:
    ```bash
    python Task1/visualize_2d.py
    ```
3.  A file named `SFD_BMD_Central_Girder.html` will be created in the main folder.
4.  Open this file in any web browser (Chrome, Edge, Firefox) to view the diagrams. You can hover over the lines to see exact values.

### 4. Generate 3D Plots (Task 2)
To visualize the SFD and BMD for the entire bridge in 3D:
1.  Run the following command:
    ```bash
    python Task2/visualize_3d.py
    ```
2.  Two files will be created in the main folder:
    *   `3D_SFD_Bridge.html` (Shear Force Diagram)
    *   `3D_BMD_Bridge.html` (Bending Moment Diagram)
3.  Open these files in your browser. You can rotate, zoom, and pan the 3D model to inspect forces on different girders.

## Methodology
1.  **Data Loading**: The script uses `xarray` to read the NetCDF file (`screening_task.nc`) containing analysis results. It also imports `node.py` and `element.py` to understand the bridge geometry.
2.  **2D Visualization (Task 1)**:
    *   It filters elements belonging to the central girder.
    *   It extracts shear and moment values at the start and end of each element.
    *   It uses `plotly` to draw continuous filled area plots.
3.  **3D Visualization (Task 2)**:
    *   It iterates through all girders.
    *   It creates a 3D structural frame using node coordinates.
    *   It "extrudes" the force diagrams vertically from the elements, proportional to the force magnitude, creating a 3D effect similar to structural analysis software.

