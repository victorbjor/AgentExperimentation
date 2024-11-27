import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import torch


def plot_function_comparison(target_func, neural_net, title):
    # Generate input data (x, y grid)
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    x, y = np.meshgrid(x, y)
    xy = torch.tensor(np.column_stack((x.ravel(), y.ravel())), dtype=torch.float32)

    z_emulated = target_func(x, y)
    z_nn = neural_net(xy).cpu().detach().numpy()

    # Convert to 1D arrays for better visualization
    x_flat = x.ravel()
    y_flat = y.ravel()
    z_emulated_flat = z_emulated.ravel()
    z_nn_flat = z_nn.ravel()

    # Create the subplot figure
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scene'}, {'type': 'scene'}]],  # Set both subplots to 3D
        subplot_titles=("Emulated Function", "Neural Network Output")
    )

    # Add the emulated function to the first graph
    fig.add_trace(
        go.Scatter3d(
            x=x_flat, y=y_flat, z=z_emulated_flat,
            mode='markers',
            marker=dict(size=3, color=z_emulated_flat, colorscale='Viridis', showscale=True),
            name="Emulated Function"
        ),
        row=1, col=1
    )

    # Add the neural network output to the second graph
    fig.add_trace(
        go.Scatter3d(
            x=x_flat, y=y_flat, z=z_nn_flat,
            mode='markers',
            marker=dict(size=3, color=z_nn_flat, colorscale='Viridis', showscale=True),
            name="NN Output"
        ),
        row=1, col=2
    )

    # Update layout
    fig.update_layout(
        height=600, width=1200,
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
    )

    # Show the plot
    fig.show()
