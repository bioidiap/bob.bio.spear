#!/usr/bin/env python
# encoding: utf-8


import torch

from torch import nn


def make_conv_layers(cfg, input_c=3):
    """builds the convolution / max pool layers

    The network architecture is provided as a list, containing the
    number of feature maps, or a 'M' for a MaxPooling layer.

    Example for Casia-Net:
    [32, 64, 'M', 64, 128, 'M', 96, 192, 'M', 128, 256, 'M', 160, 320]

    Parameters
    ----------
    cfg: list
      Configuration for the network (see above)
    input_c: int
      The number of channels in the input (1 -> gray, 3 -> rgb)

    """
    layers = []
    in_channels = input_c
    for v in cfg:
        if v == "M":
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            layers += [conv2d, nn.ReLU()]
            in_channels = v
    return nn.Sequential(*layers)


def weights_init(m):
    """Initialize the weights

    Initialize the weights in the different layers of
    the network.

    Parameters
    ----------
    m : :py:class:`torch.nn.Conv2d`
      The layer to initialize

    """

    classname = m.__class__.__name__
    if classname.find("Conv") != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find("BatchNorm") != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


class MaxFeatureMap(nn.Module):
    """Class defining the max feature map

    Attributes
    ----------
    out_channels: int
      the number of output channels ?
    filter: either :py:class:`torch.nn.Conv2D` or :py:class:`torch.nn.Linear`

    """

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size=3,
        stride=1,
        padding=1,
        type=1,
    ):
        """Init function

        Parameters
        ----------
        in_channels: int
          the number of input channels
        out_channels: int
          the number of output channels
        kernel_size: int
          The size of the kernel in the convolution
        stride: int
          The stride in the convolution
        padding: int
          The padding (default to)
        type: int
          ??

        """

        super().__init__()
        self.out_channels = out_channels
        if type == 1:
            self.filter = nn.Conv2d(
                in_channels,
                2 * out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
            )
        else:
            self.filter = nn.Linear(in_channels, 2 * out_channels)

    def forward(self, x):
        """Forward function

        Propagates data through the Max Feature Map

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
          The data to forward through the MFM

        Returns
        -------
        py:class:`torch.Tensor`


        """
        x = self.filter(x)
        out = torch.split(x, self.out_channels, 1)
        return torch.max(out[0], out[1])


class group(nn.Module):
    """Class implementing ...

    Attributes
    ----------

    """

    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        """Init function


        Parameters
        ----------
        in_channels: int
          the number of input channels
        out_channels: int
          the number of output channels
        kernel_size: int
          The size of the kernel in the convolution
        stride: int
          The stride in the convolution
        padding: int
          The padding (default to)

        """
        super().__init__()
        self.conv_a = MaxFeatureMap(in_channels, in_channels, 1, 1, 0)
        self.conv = MaxFeatureMap(
            in_channels, out_channels, kernel_size, stride, padding
        )

    def forward(self, x):
        """Forward function

        Propagates data through the Max Feature Map

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
          The data to forward through the MFM

        Returns
        -------
        py:class:`torch.Tensor`

        """
        x = self.conv_a(x)
        x = self.conv(x)
        return x


class resblock(nn.Module):
    """Class implementing ..."""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = MaxFeatureMap(
            in_channels, out_channels, kernel_size=3, stride=1, padding=1
        )
        self.conv2 = MaxFeatureMap(
            in_channels, out_channels, kernel_size=3, stride=1, padding=1
        )

    def forward(self, x):
        res = x
        out = self.conv1(x)
        out = self.conv2(out)
        out = out + res
        return out


class BasicBlock(nn.Module):
    """Basic block for making ResNet architecture

    Attributes
    ----------
    expansion: int32
      Expansion factor for connection of residual blocks

    """

    expansion = 1

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        """Init function

        Parameters
        ----------
        inplanes: int32
          The number of input channels
        planes: int32
          The number of output channels
        stride: int32
          The stride in the convolution (Default: 1)
        downsample: bool
          Apply downsampling for skip connection (Default: None)

        """
        super().__init__()
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        """Forward function

        Propagates data through the BasicBlock architecture

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
          The data to forward through the BasicBlock

        Returns
        -------
        py:class:`torch.Tensor`

        """
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class Bottleneck(nn.Module):
    """Bottleneck block for making ResNet architecture

    Attributes
    ----------
    expansion: int32
      Expansion factor for connection of residual blocks

    """

    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        """Init function

        Parameters
        ----------
        inplanes: int32
          The number of input channels
        planes: int32
          The number of output channels
        stride: int32
          The stride in the convolution (Default: 1)
        downsample: bool
          Apply downsampling for skip connection (Default: None)

        """
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(
            planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        """Forward function

        Propagates data through the Bottleneck architecture

        Parameters
        ----------
        x: :py:class:`torch.Tensor`
          The data to forward through the Bottleneck

        Returns
        -------
        py:class:`torch.Tensor`

        """
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


def conv3x3(in_planes, out_planes, stride=1):
    """3x3 convolution with padding

    Parameters
    ----------
    inplanes: int32
      The number of input channels
    out_planes: int32
      The number of output channels
    stride: int32
      The stride in the convolution (Default: 1)

    Returns
    -------
    py:class:`torch.Tensor`

    """
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=1,
        bias=False,
    )


def _make_layer(block, planes, blocks, stride=1, inplanes=1):
    """Make layers of architecture based on the input blocks

    Parameters
    ----------
    block: :py:class:`torch.nn.Module`
        Residual block in ResNet architecture.
    planes: int32
        The number of output channels.
    blocks: int32
        Number of CNN layers in current block.
    stride: int32
        The stride in the convolution (Default: 1).
    inplanes: int32
        The number of input channels (Default: 1).

    Returns
    -------
    py:class:`torch.nn.Sequential`
    inplanes: int32
        The number of new input channels based on expansion.
    """
    downsample = None
    if stride != 1 or inplanes != planes * block.expansion:
        downsample = nn.Sequential(
            nn.Conv2d(
                inplanes,
                planes * block.expansion,
                kernel_size=1,
                stride=stride,
                bias=False,
            ),
            nn.BatchNorm2d(planes * block.expansion),
        )

    layers = []
    layers.append(block(inplanes, planes, stride, downsample))
    inplanes = planes * block.expansion
    layers.extend([block(inplanes, planes) for _ in range(blocks - 1)])

    return (nn.Sequential(*layers), inplanes)
