#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import logging
import math

import torch
import torch.nn as nn

from bob.bio.spear.embeddings.utils import BasicBlock, Bottleneck, _make_layer

logger = logging.getLogger(__name__)

__all__ = [
    "DltResNet",
    "dltresnet18",
    "dltresnet34",
    "dltresnet50",
    "dltresnet101",
    "dltresnet152",
]


class DltResNet(nn.Module):
    """DltResNet architecture for training the audio embedding extractor"""

    def __init__(
        self, block, layers, num_classes=1000, tp="cls", bn_dim=128, bn_dim2=128
    ):
        """Initialization function

        Parameters
        ----------
            block: :py:class:`torch.nn.Module`
                Residual block in DltResNet architecture.
            layers: list<int32>
                Number of residual blocks and number of CNN layers in each block
            num_classes: int32
                Number of output classes (Default: 1000).
            tp: str
                Type of network for training or embedding extraction
            bn_dim: int32
                Dimension of first segment level layer
            bn_dim2: int32
                Dimension of second segment level layer

        """
        self.net_type = tp
        self.inplanes = 64
        super().__init__()
        self.conv1 = nn.Conv2d(
            1, 16, kernel_size=5, stride=2, padding=2, bias=False
        )
        self.bn1 = nn.BatchNorm2d(16)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(
            16,
            32,
            kernel_size=(5, 1),
            stride=(1, 1),
            padding=(4, 0),
            bias=False,
            dilation=(2, 1),
        )
        self.bn2 = nn.BatchNorm2d(32)
        self.maxpool = nn.MaxPool2d(
            kernel_size=(3, 1), stride=(2, 1), padding=0
        )
        self.conv3 = nn.Conv2d(
            32,
            64,
            kernel_size=(3, 1),
            stride=(1, 1),
            padding=(3, 0),
            bias=False,
            dilation=(3, 1),
        )
        self.bn3 = nn.BatchNorm2d(64)

        self.layer1, self.inplanes = _make_layer(
            block, 64, layers[0], stride=2, inplanes=self.inplanes
        )
        self.layer2, self.inplanes = _make_layer(
            block, 128, layers[1], stride=2, inplanes=self.inplanes
        )
        self.layer3, self.inplanes = _make_layer(
            block, 256, layers[2], stride=2, inplanes=self.inplanes
        )
        self.layer4, self.inplanes = _make_layer(
            block, 512, layers[3], stride=2, inplanes=self.inplanes
        )
        self.conv4 = nn.Conv2d(
            256, 256, kernel_size=(1, 9), stride=1, padding=0, bias=False
        )
        self.bn4 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(
            256, 512, kernel_size=(1, 9), stride=1, padding=0, bias=False
        )
        self.bn5 = nn.BatchNorm2d(512)
        self.fc = nn.Linear(1024, num_classes)
        self.fc1 = nn.Linear(bn_dim, num_classes)
        self.fc2 = nn.Linear(bn_dim2, num_classes)
        self.em = nn.Linear(1024, bn_dim)
        self.em2 = nn.Linear(bn_dim, bn_dim2)
        self.bn = nn.BatchNorm2d(bn_dim2)
        self.drp = nn.Dropout(p=0.2)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2.0 / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        """Derived forward function implementation of :py:class:`torch.nn.Module` class

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        if self.net_type == "prefc":
            return self.forward_cnn(x)
        if self.net_type == "cls":  # without segment layer
            return self.forward_cls(x)
        if self.net_type == "cls2":  # with one segment layer
            return self.forward_cls2(x)
        if self.net_type == "cls3":  # with two segment layers
            return self.forward_cls3(x)
        if self.net_type == "emb":  # embedding from first segment layer
            return self.forward_emb(x)
        if self.net_type == "emb2":  # embedding from second segment layer
            return self.forward_emb2(x)

    def forward_cnn(self, x):
        """Basic forward function for extracting the embeddings

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        try:
            x = self.conv1(x)
        except ValueError:
            logger.error("Error with " + str(x.size()))
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu(x)
        t = torch.std(x, 2)
        m = torch.mean(x, 2)
        x = torch.cat((m, t), 1)
        x = x.view(x.size(0), -1)
        return x

    def forward_cls(self, x):
        """
        Forward pass without segment layer for identification training

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.forward_cnn(x)
        x = self.fc(x)
        return x

    def forward_cls2(self, x):
        """Forward pass with one segment layer for identification training

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.forward_cnn(x)
        x = self.drp(x)
        x = self.em(x)
        x = self.drp(x)
        x = self.fc1(x)
        return x

    def forward_cls3(self, x):
        """Forward pass with two segment layer for identification training

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """

        x = self.forward_cnn(x)
        x = self.forward_cnn(x)
        x = self.drp(x)
        x = self.em(x)
        x = self.em2(x)
        x = self.bn(x)
        x = self.relu(x)
        x = self.drp(x)
        x = self.fc2(x)
        return x

    def forward_emb(self, x):
        """Forward pass for embedding extraction from the first segment layer

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.forward_cnn(x)
        x = self.em(x)
        x = torch.div(x, torch.norm(x, 2, 1).unsqueeze(1).expand_as(x))
        return x

    def forward_emb2(self, x):
        """Forward pass for embedding extraction from the second segment layer

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.forward_cnn(x)
        x = self.em(x)
        x = self.em2(x)
        x = torch.div(x, torch.norm(x, 2, 1).unsqueeze(1).expand_as(x))
        return x

    def forward_emb_test(self, x, step=1):
        """Test forward pass

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
            The data to forward through the BasicBlock
        step: int32
            The step test for returning the result
        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.conv1(x)
        if step == 0:
            return x
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        if step == 1:
            return x
        x = self.maxpool(x)
        if step == 2:
            return x
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        if step == 3:
            return x
        x = self.layer1(x)
        if step == 4:
            return x
        x = self.layer2(x)
        if step == 5:
            return x
        x = self.layer3(x)
        if step == 6:
            return x
        x = self.conv4(x)
        if step == 7:
            return x
        x = self.bn4(x)
        x = self.relu(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu(x)
        if step == 8:
            return x
        t = torch.std(x, 2)
        m = torch.mean(x, 2)
        x = torch.cat((m, t), 1)
        x = x.view(x.size(0), -1)
        return x


def dltresnet18(num_classes=1251, tp="cls", bn_dim=128, bn_dim2=128):
    """Constructs a DltResNet-18 model.

    Parameters
    ----------

    """
    model = DltResNet(
        BasicBlock,
        [2, 2, 2, 2],
        num_classes=num_classes,
        tp=tp,
        bn_dim=bn_dim,
        bn_dim2=bn_dim2,
    )
    return model


def dltresnet34(num_classes=1251, tp="cls", bn_dim=128, bn_dim2=128):
    """Constructs a DltResNet-34 model.

    Parameters
    ----------

    """
    model = DltResNet(
        BasicBlock,
        [3, 4, 6, 3],
        num_classes=num_classes,
        tp=tp,
        bn_dim=bn_dim,
        bn_dim2=bn_dim2,
    )
    return model


def dltresnet50(num_classes=1251, tp="cls", bn_dim=128, bn_dim2=128):
    """Constructs a DltResNet-50 model.

    Parameters
    ----------

    """
    model = DltResNet(
        Bottleneck,
        [3, 4, 14, 3],
        num_classes=num_classes,
        tp=tp,
        bn_dim=bn_dim,
        bn_dim2=bn_dim2,
    )
    return model


def dltresnet101(num_classes=1251, tp="cls", bn_dim=128, bn_dim2=128):
    """Constructs a DltResNet-101 model.

    Parameters
    ----------

    """
    model = DltResNet(
        Bottleneck,
        [3, 4, 23, 3],
        num_classes=num_classes,
        tp=tp,
        bn_dim=bn_dim,
        bn_dim2=bn_dim2,
    )
    return model


def dltresnet152(num_classes=1251, tp="cls", bn_dim=128, bn_dim2=128):
    """Constructs a DltResNet-152 model.

    Parameters
    ----------

    """
    model = DltResNet(
        Bottleneck,
        [3, 8, 36, 3],
        num_classes=num_classes,
        tp=tp,
        bn_dim=bn_dim,
        bn_dim2=bn_dim2,
    )
    return model
