#!/usr/bin/env python3

from typing import Type, Callable
import torch
from torch import nn
import torch.nn.functional as F


# NN for demagnetization factor
demag_model = nn.Sequential(
    nn.Linear(3, 128),
    nn.Tanh(),
    nn.Linear(128, 48),
    nn.Tanh(),
    nn.Linear(48, 128),
    nn.Tanh(),
    nn.Linear(128, 1),
    nn.Sigmoid(),
)


# NN for testing
class PINN_network(nn.Module):
    def __init__(
        self,
        in_features,
        activation=nn.SiLU(),
        final_activation=None,
        dropout=False,
        defined_with_dropout=False,
    ):
        super().__init__()
        self.activation = activation
        if final_activation == None:
            final_activation = nn.Identity()
        self.final_activation = final_activation

        if defined_with_dropout:
            self.dropout1 = nn.Identity()
            self.dropout2 = nn.Identity()
            self.dropout3 = nn.Identity()

        if dropout:
            self.dropout1 = nn.Dropout(p=0.5)
            self.dropout2 = nn.Dropout(p=0.5)
            self.dropout3 = nn.Dropout(p=0.5)

        # self.model_simple = nn.Sequential(
        #     nn.Linear(in_features, 128),
        #     nn.ReLU(),
        #     nn.Linear(128, 48),
        #     nn.ReLU(),
        #     nn.Linear(48, 128),
        #     nn.ReLU(),
        #     nn.Linear(128, 3)
        # )

        if dropout or defined_with_dropout:
            self.model = nn.Sequential(
                nn.Linear(in_features, 128),
                self.activation,
                self.dropout1,
                nn.Linear(128, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                self.dropout2,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 128),
                self.activation,
                self.dropout3,
                nn.Linear(128, 3),
                self.final_activation,
            )

        else:
            self.model = nn.Sequential(
                nn.Linear(in_features, 128),
                self.activation,
                nn.Linear(128, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 48),
                self.activation,
                nn.Linear(48, 128),
                self.activation,
                nn.Linear(128, 3),
                self.final_activation,
            )

    def forward(self, dimensions, xyz):
        # xyz as separate input to be able to differentiate wrt xyz but not dimensions
        x1 = torch.cat([dimensions, xyz], dim=1)
        x1 = self.model(x1)
        return x1


class Network(nn.Module):
    def __init__(
        self,
        in_features: int,
        hidden_dim_factor: int,
        out_features: int,
        activation: Callable[[torch.Tensor], torch.Tensor] = F.silu,
        do_output_activation=True,
    ) -> None:
        super().__init__()

        self.linear1 = nn.Linear(
            in_features=in_features,
            out_features=4 * hidden_dim_factor,
        )
        self.linear2 = nn.Linear(
            in_features=4 * hidden_dim_factor,
            out_features=8 * hidden_dim_factor,
        )
        self.linear3 = nn.Linear(
            in_features=8 * hidden_dim_factor,
            out_features=4 * hidden_dim_factor,
        )
        self.linear4 = nn.Linear(
            in_features=4 * hidden_dim_factor,
            out_features=2 * hidden_dim_factor,
        )
        self.linear5 = nn.Linear(
            in_features=2 * hidden_dim_factor,
            out_features=hidden_dim_factor,
        )
        self.output = nn.Linear(
            in_features=1 * hidden_dim_factor,
            out_features=out_features,
        )
        self.activation = activation
        self.do_output_activation = do_output_activation

    def forward(self, x):
        x = self.activation(self.linear1(x))
        x = self.activation(self.linear2(x))
        x = self.activation(self.linear3(x))
        x = self.activation(self.linear4(x))
        x = self.activation(self.linear5(x))

        if self.do_output_activation:
            return self.activation(self.output(x))

        return self.output(x)


class FieldLoss(nn.Module):
    def __init__(self, loss: Type[nn.Module] = nn.L1Loss) -> None:
        super().__init__()
        self.loss = loss()

    def forward(self, B, B_pred):
        B_demag, B_reduced = B[..., :3], B[..., 3:]
        return self.loss(B_demag, B_pred * B_reduced)


# custom loss for multiplicative target
# exclude points where |analytic solution| < minimum value

# class LossExcludeSmallValues(nn.Module):

#     def __init__(self, B_MIN, loss_fn):
#         super(LossExcludeSmallValues, self).__init__()
#         self.B_MIN = B_MIN
#         self.loss_fn = loss_fn()

#     def forward(self, output, target, analytic):
#         mask = (torch.abs(analytic) > self.B_MIN)
#         loss = self.loss_fn(output[mask], target[mask])
#         return loss
