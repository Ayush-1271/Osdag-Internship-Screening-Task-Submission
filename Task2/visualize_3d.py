
import os
import sys
import numpy as np
import xarray as xr
import plotly.graph_objects as go

# Add parent directory to path to import node and element
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import node
    import element
except ImportError:
    sys.path.append(os.getcwd())
    import node
    import element

def get_node_coords(node_id):
    """Fetches coordinates for a given node ID."""
    return node.nodes.get(node_id)

def create_extrusion_trace(p1, p2, v1, v2, scale=1.0, color='blue', name='Force'):
    """
    Creates a Mesh3d trace representing the vertical extrusion of a value along a line segment.
    p1, p2: (x, y, z) tuples for start and end points of the element.
    v1, v2: Scalar values (force/moment) at start and end.
    scale: multiplier for v values to make them visible in 3D.
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    
    # Vertices of the quad (two triangles)
    # 0: P1
    # 1: P2
    # 2: P2_top (shifted by v2)
    # 3: P1_top (shifted by v1)
    
    # "Up" is +Y direction based on the prompt "extruded vertically (y-direction)"
    
    p1_top = (x1, y1 + v1 * scale, z1)
    p2_top = (x2, y2 + v2 * scale, z2)
    
    x = [p1[0], p2[0], p2_top[0], p1_top[0]]
    y = [p1[1], p2[1], p2_top[1], p1_top[1]]
    z = [p1[2], p2[2], p2_top[2], p1_top[2]]
    
    # Vertex indices for two triangles
    # Triangle 1: 0, 1, 2
    # Triangle 2: 0, 2, 3
    i = [0, 0]
    j = [1, 2]
    k = [2, 3]
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color=color,
        opacity=0.8,
        name=name,
        showlegend=False
    )

def visualize_bridge_3d():
    """Generates 3D SFD and BMD plots for the entire bridge."""
    
    # Girder definitions from prompt
    girders = {
        'Girder 1': [13, 22, 31, 40, 49, 58, 67, 76, 81],
        'Girder 2': [14, 23, 32, 41, 50, 59, 68, 77, 82],
        'Girder 3': [15, 24, 33, 42, 51, 60, 69, 78, 83],
        'Girder 4': [16, 25, 34, 43, 52, 61, 70, 79, 84],
        'Girder 5': [17, 26, 35, 44, 53, 62, 71, 80, 85]
    }
    
    all_elements = []
    for g_list in girders.values():
        all_elements.extend(g_list)
        
    # Load dataset
    nc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screening_task.nc')
    try:
        ds = xr.open_dataset(nc_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{nc_path}'.")
        return

    # Scaling factors (adjusted for visual appearance)
    # Moments (Mz) are typically larger or smaller than Shear (Vy). need to tune.
    SCALE_SFD = 0.5 
    SCALE_BMD = 0.2
    
    # Create two figures: one for SFD, one for BMD
    fig_sfd = go.Figure()
    fig_bmd = go.Figure()
    
    print("Generating 3D plots...")
    
    for elem_id in all_elements:
        if elem_id not in element.members:
            continue
            
        conn = element.members[elem_id]
        p1 = get_node_coords(conn[0])
        p2 = get_node_coords(conn[1])
        
        try:
            elem_data = ds.sel(Element=elem_id)
        except KeyError:
            continue
            
        def get_val(comp):
            return float(elem_data['forces'].sel(Component=comp).values)

        mz_i = get_val('Mz_i')
        mz_j = get_val('Mz_j')
        vy_i = get_val('Vy_i')
        vy_j = get_val('Vy_j')
        
        # Add frame line (the structure itself)
        # Using simple line trace
        frame_trace = go.Scatter3d(
            x=[p1[0], p2[0]],
            y=[p1[1], p2[1]],
            z=[p1[2], p2[2]],
            mode='lines',
            line=dict(color='black', width=3),
            name=f'Element {elem_id}',
            showlegend=False
        )
        
        fig_sfd.add_trace(frame_trace)
        fig_bmd.add_trace(frame_trace)
        
        # Add SFD extrusion (Shear Force)
        # We color it based on sign or magnitude. Let's use a fixed color for now but maybe gradient later?
        # Standard structural software uses colors for magnitude. Mesh3d supports intensity.
        
        sfd_trace = create_extrusion_trace(p1, p2, vy_i, vy_j, scale=SCALE_SFD, color='orange', name=f'SFD E{elem_id}')
        fig_sfd.add_trace(sfd_trace)
        
        # Add BMD extrusion (Bending Moment)
        bmd_trace = create_extrusion_trace(p1, p2, mz_i, mz_j, scale=SCALE_BMD, color='cyan', name=f'BMD E{elem_id}')
        fig_bmd.add_trace(bmd_trace)

    ds.close()

    # Layout settings
    layout_settings = dict(
        scene=dict(
            aspectmode='data', # Important to keep proportions
            xaxis_title='X (Longitudinal)',
            yaxis_title='Y (Vertical/Force)',
            zaxis_title='Z (Transverse)'
        ),
        margin=dict(l=0, r=0, b=0, t=50)
    )

    fig_sfd.update_layout(title="3D Shear Force Diagram (SFD)", **layout_settings)
    fig_bmd.update_layout(title="3D Bending Moment Diagram (BMD)", **layout_settings)

    # Save files
    fig_sfd.write_html("3D_SFD_Bridge.html")
    fig_bmd.write_html("3D_BMD_Bridge.html")
    print(f"3D Plots saved to {os.path.abspath('3D_SFD_Bridge.html')} and {os.path.abspath('3D_BMD_Bridge.html')}")

if __name__ == "__main__":
    visualize_bridge_3d()
