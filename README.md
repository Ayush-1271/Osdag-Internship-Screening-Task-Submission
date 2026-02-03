# SFD and BMD Visualization for Bridge Structure

A Python project that processes NetCDF structural analysis data to generate interactive Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for a bridge structure in both 2D and 3D formats.

## Overview

This project analyzes force and moment data from a finite element analysis (FEA) of a bridge structure and creates interactive visualizations using Plotly. The project is organized into two main tasks:

- **Task 1: 2D Visualization** - Analyze and visualize the central longitudinal girder
- **Task 2: 3D Visualization** - Create 3D visualizations for the entire bridge structure

## What's Used

### Technologies & Libraries
- **Python 3.x** - Programming language
- **xarray** - Reading and processing NetCDF files
- **netCDF4** - NetCDF file format support
- **Plotly** - Interactive 2D/3D visualization
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation and analysis

### Data Files & Geometry
- `screening_task.nc` - NetCDF file containing FEA results with forces and moments for 85 elements
- `node.py` - Defines 50 bridge node coordinates in 3D space (x, y, z)
- `element.py` - Defines 85 structural elements with their connectivity (start node, end node)

## Project Structure

```
.
├── Task1/
│   └── visualize_2d.py              # Task 1: 2D visualization script
├── Task2/
│   └── visualize_3d.py              # Task 2: 3D visualization script
├── node.py                          # Node coordinate definitions (50 nodes)
├── element.py                       # Element connectivity definitions (85 elements)
├── screening_task.nc                # NetCDF file with FEA results
├── inspect_nc.py                    # Utility script to inspect NetCDF structure
├── SFD_BMD_Central_Girder.html      # Output: Task 1 - 2D interactive plots
├── 3D_SFD_Bridge.html               # Output: Task 2 - 3D SFD visualization
├── 3D_BMD_Bridge.html               # Output: Task 2 - 3D BMD visualization
├── Report.md                         # Original project report
└── README.md                         # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install xarray netcdf4 plotly pandas numpy
```

### Step 2: Verify Data Files

Ensure all required files are in the project directory:
- `screening_task.nc` - FEA results file
- `node.py` - Node definitions
- `element.py` - Element definitions

---

## Task 1: 2D Visualization (Central Girder)

### Overview
Task 1 analyzes and visualizes the Shear Force and Bending Moment Diagrams for the **central longitudinal girder** of the bridge. The central girder consists of 9 elements spanning the length of the bridge.

**Central Girder Elements:** [15, 24, 33, 42, 51, 60, 69, 78, 83]

### How to Run

Execute the following command:
```bash
python Task1/visualize_2d.py
```

### Output
**File:** `SFD_BMD_Central_Girder.html`

This generates an interactive 2D plot containing:
- **Shear Force Diagram (SFD)** - Blue filled area showing shear forces along the girder
- **Bending Moment Diagram (BMD)** - Orange filled area showing bending moments along the girder
- X-axis: Distance along the girder (in structural units)
- Y-axis: Force magnitude (SFD in kN, BMD in kN·m)

### Features
- **Interactive hover** - Move your cursor over the plot to see exact values
- **Zoom** - Scroll wheel to zoom in/out
- **Pan** - Click and drag to move around the plot
- **Legend** - Click legend items to toggle diagram visibility

### How It Works
1. Identifies the 9 central girder elements from `element.py`
2. Reads force and moment data from `screening_task.nc` for each element
3. Extracts shear force values (Vy_i, Vy_j) at element start and end nodes
4. Extracts bending moment values (Mz_i, Mz_j) at element start and end nodes
5. Calculates element lengths using 3D node coordinates from `node.py`
6. Creates continuous diagrams by combining all elements sequentially
7. Generates Plotly visualization with both diagrams overlaid

### Data Mapping
- **Vy_i** - Shear force at element start node
- **Vy_j** - Shear force at element end node
- **Mz_i** - Bending moment at element start node
- **Mz_j** - Bending moment at element end node

---

## Task 2: 3D Visualization (Entire Bridge)

### Overview
Task 2 creates comprehensive 3D visualizations of the entire bridge structure, showing force distributions across all 5 longitudinal girders. Each girder contains 9 elements, making a total of 45 elements analyzed.

**Bridge Girders:**
- Girder 1: [13, 22, 31, 40, 49, 58, 67, 76, 81]
- Girder 2: [14, 23, 32, 41, 50, 59, 68, 77, 82]
- Girder 3: [15, 24, 33, 42, 51, 60, 69, 78, 83] (Central)
- Girder 4: [16, 25, 34, 43, 52, 61, 70, 79, 84]
- Girder 5: [17, 26, 35, 44, 53, 62, 71, 80, 85]

### How to Run

Execute the following command:
```bash
python Task2/visualize_3d.py
```

### Outputs
Two separate HTML files are generated:

**File 1:** `3D_SFD_Bridge.html` - Shear Force Diagram in 3D
**File 2:** `3D_BMD_Bridge.html` - Bending Moment Diagram in 3D

### Features
- **3D Visualization** - Full bridge geometry with force extrusions
- **Interactive Controls:**
  - **Rotate** - Click and drag to rotate the view
  - **Zoom** - Scroll wheel to zoom in/out
  - **Pan** - Right-click and drag to pan
  - **Hover** - See values for individual elements
- **Color Coding** - Different colors for SFD and BMD
- **Scalable Extrusions** - Force magnitudes are scaled for visibility

### How It Works
1. Loads all 5 girders with their element definitions from `element.py`
2. Reads force and moment data from `screening_task.nc` for all elements
3. Retrieves 3D node coordinates from `node.py` for each element
4. For each element:
   - Creates a line segment between start and end nodes
   - **Extrudes** the element perpendicular to the bridge plane (Y-direction)
   - Extrusion height represents force/moment magnitude (scaled for visibility)
   - Creates a 3D mesh surface showing the force distribution
5. Generates two separate figures:
   - **SFD Figure:** Shows Vy (shear force) extrusions with blue coloring
   - **BMD Figure:** Shows Mz (bending moment) extrusions with orange coloring
6. Combines all girders into a complete bridge visualization

### Scale Factors
- **SFD Scale:** 0.5 (adjusts shear force visibility)
- **BMD Scale:** 0.2 (adjusts moment visualization)

These factors can be modified in `Task2/visualize_3d.py` if diagrams appear too small or too large.

### Interpretation
- **Higher extrusions** indicate larger force or moment values
- **Negative values** extend in the opposite direction
- **Smooth transitions** between elements show force flow through the structure
- **Multiple girders** can be compared visually in a single 3D view

---

## How to Operate

### Quick Start
```bash
# Task 1: Generate 2D plots
python Task1/visualize_2d.py

# Task 2: Generate 3D plots
python Task2/visualize_3d.py
```

### Viewing Results
1. Open the generated HTML files in any modern web browser (Chrome, Firefox, Edge, Safari)
2. Use mouse interactions to explore:
   - For 2D plots: Hover, zoom, pan
   - For 3D plots: Rotate, zoom, pan
3. All data is embedded in the HTML - no internet connection required

### Inspecting NetCDF Data
To examine the raw NetCDF file structure:
```bash
python inspect_nc.py
```

This creates `inspect_output.txt` with variable names, dimensions, and available data components.

---

## Methodology

### Data Processing Pipeline
1. **Load NetCDF File** → Read FEA results using xarray
2. **Import Geometry** → Parse node coordinates and element connectivity
3. **Extract Values** → Retrieve Vy and Mz components for each element
4. **Calculate Properties** → Compute element lengths from node coordinates
5. **Generate Visualization** → Create Plotly plots with appropriate scaling

### 2D Visualization Algorithm (Task 1)
```
For each central girder element:
  1. Get start and end node IDs
  2. Retrieve Vy_i, Vy_j (shear forces)
  3. Retrieve Mz_i, Mz_j (bending moments)
  4. Calculate element length from coordinates
  5. Accumulate distance along girder
  6. Plot continuous filled areas
```

### 3D Visualization Algorithm (Task 2)
```
For each bridge element:
  1. Get start and end node positions
  2. Retrieve force/moment values
  3. Create extrusion mesh:
     - Bottom face: element line
     - Top face: element line + force offset
     - Height: proportional to force magnitude
  4. Apply color based on force type (SFD/BMD)
  5. Combine all element meshes in 3D plot
```

---

## Troubleshooting

### Python/Import Errors
**Error:** `ModuleNotFoundError: No module named 'xarray'`

**Solution:** Reinstall all dependencies
```bash
pip install --upgrade xarray netcdf4 plotly pandas numpy
```

### NetCDF File Issues
**Error:** `FileNotFoundError: screening_task.nc`

**Solution:** Ensure the NetCDF file is in the root directory where the scripts run from. Check with:
```bash
python inspect_nc.py
```

### HTML Files Won't Display
**Issue:** Browser shows blank page or error

**Solutions:**
- Try a different browser (Chrome is recommended)
- Disable browser extensions that might block scripts
- Check browser console (F12) for error messages
- Ensure JavaScript is enabled

### Diagrams Appear Too Small/Large
**Issue:** Force extrusions aren't visible or too extreme

**Solution:** Modify scale factors in the scripts:
- **Task 1:** Adjust plot ranges in `visualize_2d.py`
- **Task 2:** Change `SCALE_SFD` and `SCALE_BMD` variables in `visualize_3d.py`

### Missing Components in Data
**Error:** "Vy_i NOT found" or similar when running inspect

**Note:** The NetCDF file contains force components. If certain components are missing, they may not be part of the analysis. Check the actual components using:
```bash
python inspect_nc.py
```

---

## Technical Details

### Bridge Geometry
- **Span Length:** 25 units (in structure)
- **Total Nodes:** 50
- **Total Elements:** 85 (including vertical and transverse members)
- **Longitudinal Girders:** 5 (each with 9 elements)
- **Coordinate System:** 3D Cartesian (x, y, z)

### Data Structure (screening_task.nc)
- **Dimensions:** Element (85), Component (30)
- **Variable:** forces (Element, Component) → float64 array
- **Components:** Include Vy_i, Vy_j, Mz_i, Mz_j, and others
- **Units:** Typically kN (kilonewtons) and kN·m (kilonewton-meters)

### File Dependencies
| File | Purpose | Used By |
|------|---------|---------|
| `node.py` | 3D coordinates of 50 bridge nodes | Both tasks |
| `element.py` | Connectivity of 85 structural elements | Both tasks |
| `screening_task.nc` | FEA analysis results | Both tasks |

---

## Notes

- All HTML outputs are **self-contained** and can be shared without additional files
- Visualizations are fully **interactive** - no external internet required
- Force units depend on your FEA software (typically kN and kN·m)
- The 3D extrusion method provides an intuitive representation similar to professional structural analysis software

---

## License

This project is part of the Osdag Internship Screening Task.

## Contact & Support

For questions or issues, refer to the project documentation or contact the development team.
