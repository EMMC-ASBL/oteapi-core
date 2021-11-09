#!/usr/bin/env python3
#
# Run as:
#
#     python porefraction.py batch1-3_40x.jpg -c 440,8056,668,1640
#

# pylint: disable=W0612
import argparse

import numpy as np
from matplotlib import pyplot as plt

import skimage
from skimage.io import imread
from skimage.color import rgba2rgb, rgb2gray
from skimage.filters import try_all_threshold


class ImageProcessing:
    """Performs image processing.

    For now it just calculates the pore fraction using simple tresholding.
    """

    def __init__(self, filename):
        self.filename = filename
        self.data = imread(filename)  # image data, shape (ny, nx, C)
        if len(self.data.shape) == 3 and self.data.shape[2] == 4:
            self.data = rgba2rgb(self.data)  # rgb image, shape (ny, nx, 3)
        self.gray = rgb2gray(self.data)  # grayscale data; shape (ny, nx)

    def crop(self, x1, x2, y1, y2):
        """Crop the image."""
        self.data = self.data[y1:y2, x1:x2]
        self.gray = self.gray[y1:y2, x1:x2]

    def test_threshold_algorithms(self):
        """Test different thresholding algorithms and return a matplotlib
        figure comparing them."""
        fig, ax = try_all_threshold(self.gray, verbose=True)
        return fig

    def pore_fraction(self, algorithm="triangle"):
        """Returns the pore fraction using the specified thresholding
        algorithm."""
        fun = getattr(skimage.filters, "threshold_" + algorithm)
        thresholded = fun(self.gray)
        bw = self.gray < thresholded
        pore_fraction = bw.sum() / np.prod(bw.shape)
        return pore_fraction


def main():
    parser = argparse.ArgumentParser(description="Calculate pore fraction.")
    parser.add_argument("input", help="Filename of input image.")
    parser.add_argument(
        "--crop",
        "-c",
        help="Crop the image before processing.  Coordinates are specified "
        "as `x1,x2,y1,y2`.",
    )
    parser.add_argument(
        "--algorithm", "-a", default="triangle", help="Thresholding algorithm."
    )
    parser.add_argument(
        "--test-algorithms",
        "-t",
        action="store_true",
        help="Compare and plot thresholding algorithms.",
    )
    args = parser.parse_args()

    p = ImageProcessing(args.input)

    if args.crop:
        coords = [int(c) for c in args.crop.split(",")]
        p.crop(*coords)

    pore_fraction = p.pore_fraction(args.algorithm)

    print(pore_fraction)

    if args.test_algorithms:
        fig = p.test_threshold_algorithms()
        plt.show()


if __name__ == "__main__":
    main()
