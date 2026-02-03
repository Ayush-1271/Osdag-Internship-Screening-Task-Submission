
import xarray as xr
import pandas as pd

file_path = "d:/Coding/Python/Strivers/screening_task.nc"

try:
    ds = xr.open_dataset(file_path)
    with open("d:/Coding/Python/Strivers/inspect_output.txt", "w") as f:
        f.write("Dataset Info:\n")
        f.write(str(ds))
        f.write("\n\nVariables:\n")
        for var in ds.data_vars:
            f.write(f"{var}: {ds[var].dims}, {ds[var].shape}\n")
        
        f.write("\nChecking for Mz and Vy:\n")
        for expected in ['Mz_i', 'Mz_j', 'Vy_i', 'Vy_j']:
            if expected in ds:
                f.write(f"{expected} found\n")
            else:
                f.write(f"{expected} NOT found\n")
            
        f.write("\nCoordinates:\n")
        for coord in ds.coords:
            f.write(f"{coord}: {ds[coord].shape}\n")
        
    ds.close()

except Exception as e:
    print(f"Error reading file: {e}")
