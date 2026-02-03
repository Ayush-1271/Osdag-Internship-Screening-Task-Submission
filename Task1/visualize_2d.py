
import os
import sys
import numpy as np
import xarray as xr
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path to import node and element
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import node
    import element
except ImportError:
    # If running from different context, try adding the current directory
    sys.path.append(os.getcwd())
    import node
    import element

def get_node_coords(node_id):
    """Fetches coordinates for a given node ID."""
    return node.nodes.get(node_id)

def get_element_length(n1, n2):
    """Calculates length between two nodes (assuming 3D)."""
    c1 = np.array(n1)
    c2 = np.array(n2)
    return np.linalg.norm(c2 - c1)

def visualize_central_girder_2d():
    """Generates 2D SFD and BMD plots for the central girder."""
    
    # Define central girder elements as specified
    central_girder_elements = [15, 24, 33, 42, 51, 60, 69, 78, 83]
    
    # Load the NetCDF data
    nc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screening_task.nc')
    try:
        ds = xr.open_dataset(nc_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{nc_path}'. Make sure the file exists.")
        return

    # Data containers
    x_coords = []
    
    # Continuous arrays for plotting
    plot_x = []
    plot_sfd = []
    plot_bmd = []
    
    current_distance = 0.0
    
    print("Processing central girder elements...")
    
    for count, elem_id in enumerate(central_girder_elements):
        conn = element.members[elem_id]
        node_i_id = conn[0]
        node_j_id = conn[1] # End node
        
        # Get element data from Xarray
        # The prompt says: _i = start, _j = end. 
        # Variable 'forces' has dims (Element, Component). 
        # Check if Element coord matches ID or index. 
        # Based on index output, element start from 1.
        
        # We need to find the index of the element in the dataset
        try:
            # Assuming 'Element' coordinate matches the element IDs
            elem_data = ds.sel(Element=elem_id)
        except KeyError:
            print(f"Warning: Element {elem_id} not found in dataset. Skipping.")
            continue
            
        # Extract forces
        # We access 'forces' variable, then select specific components
        # Note: The component names are strings in the coordinate 'Component'
        
        # Helper to safely get value. Values are numpy arrays or scalars
        def get_val(comp):
            return float(elem_data['forces'].sel(Component=comp).values)

        mz_i = get_val('Mz_i')
        mz_j = get_val('Mz_j')
        vy_i = get_val('Vy_i')
        vy_j = get_val('Vy_j')
        
        # Calculate length to increment x-axis
        coords_i = get_node_coords(node_i_id)
        coords_j = get_node_coords(node_j_id)
        length = get_element_length(coords_i, coords_j)
        
        # Start and End x for this element
        start_x = current_distance
        end_x = current_distance + length
        
        # Append to plot data
        # For a beam element, values are typically linear or constant depending on loading.
        # Given just end values, we assume linear variation for Moment, constant/linear for Shear.
        # The prompt implies end values: "Use Mz_i and Mz_j -> to create the Bending Moment Diagram"
        # So we plot a line from (start_x, val_i) to (end_x, val_j)
        
        # Avoid gaps by not repeating the exact same point if it's the same as previous, 
        # but for SFD abrupt changes can happen at nodes (support reactions). 
        # For BMD, it should be continuous usually.
        
        plot_x.extend([start_x, end_x])
        plot_sfd.extend([vy_i, vy_j])
        plot_bmd.extend([mz_i, mz_j])
        
        current_distance += length

    ds.close()
    
    # Create plots using Plotly
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.1,
                        subplot_titles=("Shear Force Diagram (SFD)", "Bending Moment Diagram (BMD)"))

    # SFD Trace
    fig.add_trace(go.Scatter(
        x=plot_x, y=plot_sfd,
        mode='lines+markers',
        name='Shear Force (Vy)',
        fill='tozeroy',
        line=dict(color='blue'),
        hovertemplate='Dist: %{x:.2f} m<br>Shear: %{y:.2f} kN<extra></extra>'
    ), row=1, col=1)

    # BMD Trace
    fig.add_trace(go.Scatter(
        x=plot_x, y=plot_bmd,
        mode='lines+markers',
        name='Bending Moment (Mz)',
        fill='tozeroy',
        line=dict(color='red'),
        hovertemplate='Dist: %{x:.2f} m<br>Moment: %{y:.2f} kNm<extra></extra>'
    ), row=2, col=1)

    # Layout updates
    fig.update_layout(
        title_text="Central Longitudinal Girder Analysis",
        height=800,
        showlegend=False,
        template="plotly_white"
    )
    
    fig.update_xaxes(title_text="Distance along Girder (m)", row=2, col=1)
    fig.update_yaxes(title_text="Shear Force (kN)", row=1, col=1)
    fig.update_yaxes(title_text="Bending Moment (kNm)", row=2, col=1)

    # Save to file
    output_file = "SFD_BMD_Central_Girder.html"
    fig.write_html(output_file)
    print(f"2D Plots saved to {os.path.abspath(output_file)}")

if __name__ == "__main__":
    visualize_central_girder_2d()
