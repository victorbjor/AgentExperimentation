import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from tqdm import tqdm

from FunctionPlotter import plot_function_comparison

# Choose your favorite function here
from FuncsToEmulate import polynomial_function as target_func


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(2, 64)
        self.layer2 = nn.Linear(64, 64)
        self.layer3 = nn.Linear(64, 1)
        self.activation = nn.GELU()

    def forward(self, x: Tensor) -> Tensor:
        x = self.layer1(x)
        x = self.activation(x)
        x = self.layer2(x)
        x = self.activation(x)
        x = self.layer3(x)
        return x


# The mapping we are learning is 2D point to 1D value
# Thus, we will be feeding tensors of size [BatchSize, 2] to the neural net and target function

# We are keeping input range to [-1, 1] for convenience.

net = Net()
optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

# Plot the output of the untrained net
plot_function_comparison(target_func, net, "Untrained Neural Net")


for _ in tqdm(range(1000)):
    x = np.random.uniform(-1, 1, 1000)
    y = np.random.uniform(-1, 1, 1000)
    z = [target_func(xi, yi) for xi, yi in zip(x, y)]

    xy = torch.tensor(np.column_stack((x, y)), dtype=torch.float32)
    z = torch.tensor(z, dtype=torch.float32).unsqueeze(1)

    loss = F.mse_loss(net(xy), z)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Plot the output of the trained net
plot_function_comparison(target_func, net, "Trained Neural Net")
