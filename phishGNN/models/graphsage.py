import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
from torch_geometric.nn import global_mean_pool


class GraphSAGE(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, device):
        super(GraphSAGE, self).__init__()

        if hidden_channels is None:
            hidden_channels = 16

        self.device = device
        self.to(device)

        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
        self.embeddings = None

    def forward(self, x, edge_index, batch):
        x = x.float()
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        x = global_mean_pool(x, batch)
        self.embeddings = x

        return x