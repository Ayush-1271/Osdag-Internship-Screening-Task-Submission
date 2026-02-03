# SFD and BMD Visualization for Bridge Structure

A Python project that processes NetCDF structural analysis data to generate interactive Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for a bridge structure in both 2D and 3D formats.

## Overview

This project analyzes force and moment data from a finite element analysis (FEA) of a bridge structure and creates interactive visualizations using Plotly. It includes:
- **2D visualization** of the central girder with SFD and BMD
- **3D visualization** of the entire bridge structure showing force distributions

## What's Used

### Technologies & Libraries
- **Python 3.x** - Programming language
- **xarray** - Reading and processing NetCDF files
- **netCDF4** - NetCDF file format support
- **Plotly** - Interactive 2D/3D visualization
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Data Files
- `screening_task.nc` - NetCDF file containing FEA results (forces, moments, displacements)
- `node.py` - Bridge node coordinates (x, y, z)
- `element.py` - Element connectivity information (member IDs and connected nodes)

## Project Structure

```
├── Task1/
│   └── visualize_2d.py          # 2D SFD/BMD visualization script
├── Task2/
│   └── visualize_3d.py          # 3D bridge visualization script
├── node.py                       # Node coordinate definitions
├── element.py                    # Element connectivity definitions
├── inspect_nc.py                 # Utility to inspect NetCDF file structure
├── SFD_BMD_Central_Girder.html   # 2D interactive plot output
├── 3D_SFD_Bridge.html            # 3D SFD visualization output
├── 3D_BMD_Bridge.html            # 3D BMD visualization output
└── README.md                      # This file
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

Ensure `screening_task.nc` is in the project directory. If not, place it in the root folder.

## How to Operate

### Generate 2D Plots (Central Girder Analysis)

Run the following command to create SFD and BMD plots for the central longitudinal girder:

```bash
python Task1/visualize_2d.py
```

**Output:** `SFD_BMD_Central_Girder.html`

This creates an interactive plot with:
- Shear Force Diagram (filled area)
- Bending Moment Diagram (filled area)
- Hover tooltips showing exact force/moment values at each point

**How to view:** Open the HTML file in any web browser (Chrome, Firefox, Edge, Safari)

### Generate 3D Plots (Full Bridge Analysis)

Run the following command to visualize the entire bridge structure in 3D:

```bash
python Task2/visualize_3d.py
```

**Outputs:** 
- `3D_SFD_Bridge.html` - Shear Force Diagram in 3D
- `3D_BMD_Bridge.html` - Bending Moment Diagram in 3D

**How to view:** Open the HTML files in your browser. You can:
- **Rotate** - Click and drag
- **Zoom** - Scroll wheel
- **Pan** - Right-click and drag
- **Hover** - See values for specific elements

## Methodology

### Data Processing
1. **Load data** from `screening_task.nc` using xarray
2. **Import geometry** from `node.py` and `element.py`
3. **Extract force/moment components** for each structural element
4. **Filter and organize** data by girder location

### 2D Visualization (Task 1)
- Identifies elements of the central girder
- Extracts shear forces and moments at element start/end points
- Plots continuous filled area diagrams using Plotly
- Creates interactive hover information

### 3D Visualization (Task 2)
- Iterates through all girders in the structure
- Creates 3D frame representation using node coordinates
- "Extrudes" force diagrams perpendicular to elements
- Force magnitude determines extrusion height
- Creates realistic 3D effect similar to structural analysis software

## Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`, ensure dependencies are installed:
```bash
pip install --upgrade xarray netcdf4 plotly pandas numpy
```

### NetCDF File Not Found
Ensure `screening_task.nc` is in the same directory as the Python scripts, or update the file path in the scripts.

### HTML Files Won't Open
- Make sure you have a modern web browser installed
- Try opening with a different browser
- Check that the file wasn't corrupted during processing

## Notes

- All HTML outputs are self-contained and can be shared without additional files
- The visualization is interactive - you can zoom, pan, and inspect individual elements
- Force values are in the units specified in your FEA software (typically kN for forces, kN·m for moments)

## License

This project is part of the Osdag Internship Screening Task.

## Contact & Support

For questions or issues, refer to the project documentation or contact the development team.
