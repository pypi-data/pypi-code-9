#!/usr/bin/env python

import click

import numpy as np
import rasterio as rio
from rasterio.warp import reproject, RESAMPLING
from rasterio import Affine

def affaux(up):
    return Affine(1, 0, 0, 0, -1, 0), Affine(up, 0, 0, 0, -up, 0)

def upsample(bidx, up, fr, to):
    upBidx = np.empty((bidx.shape[0] * up, bidx.shape[1] * up), dtype=bidx.dtype)

    reproject(
        bidx, upBidx,
        src_transform=fr,
        dst_transform=to,
        src_crs="EPSG:3857",
        dst_crs="EPSG:3857",
        resampling=RESAMPLING.bilinear)

    return upBidx

def compare(srcpath1, srcpath2, max_px_diff=0, resample=1):
    with rio.drivers():
        src1 = rio.open(srcpath1)
        src2 = rio.open(srcpath2)

        count1 = src1.count
        count2 = src2.count

        props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']

        for prop in props:
            a = src1.__getattribute__(prop)
            b = src2.__getattribute__(prop)
            assert a == b, "prop %s does not match (%s != %s)" % (prop, a, b)

        for bidx in range(1, count1 + 1):
            band1 = src1.read(bidx, masked=False).astype(np.int16)
            band2 = src2.read(bidx, masked=False).astype(np.int16)

            if resample > 1:
                toAff, frAff = affaux(resample)
                band1 = upsample(band1, resample, frAff, toAff)
                band2 = upsample(band2, resample, frAff, toAff)

            diff = np.absolute(band1 - band2)
            threshold = np.zeros(band1.shape)
            outliers = np.where(diff > 16)
            if outliers[0].size > max_px_diff:
                click.echo(outliers[0], err=True)
            assert outliers[0].size <= max_px_diff, "band %s has %d pixels which differ by > 16" % (bidx, outliers[0].size)

        src1.close()
        src2.close()