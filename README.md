# LuminexDataPipeline Documentation

Last updated: 17.03.2018<br>
Version: 0.02<br>
Python version: 3.5<br>

## Contents
[Overview](#overview)<br>
[Quick Start](#quick-start)<br>
[The Pipeline](#the-pipeline)<br>


## Overview
The LuminexDataPipeline repository contains software for the automated
processing of Luminex data for statistical genomics.

## Quick Start
Checkout stable-req.txt to make sure you have the correct versions of
the Python package requirements. Pandas .xls parsing is quite specific
per version number.

Edit run.py for your own source directory, destination directory and
the number of bio-sheets to concatenate across.

Run run.py.

## The Pipeline
For each .xls file a model (up to a third order polynomial) is fitted
for each analyte (bio-marker) of standard fluorescence. This model is
then applied to the remaining samples in the plate as a calibrator.

The output files are .xlsx, with the option to include the model
fits as .png images.
