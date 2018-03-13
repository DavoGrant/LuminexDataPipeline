# LuminexDataPipeline Documentation

Last updated: 13.03.2018<br>
Version: 0.02<br>
Python version: 3.5<br>

## Contents
[Overview](#overview)<br>
[Quick Start](#quick_start)<br>
[Functions](#functions)<br>


## Overview
The LuminexDataPipeline repository contains software for the automated
processing of Luminex data for statistical genomics.

## Quick Start
Checkout stable-req.txt to make sure you have the correct versions of
the Python package requirements.

Edit run.py with your source and destination directories, and the
number of bio-sheets to concatenate across.

Run run.py.

## Functions
The pipeline fits a model - up to a third order polynomial - to
analytes (biomarkers) of standard fluorescence. This model is then
applied to the remaining samples in the plate as a calibrator.

The input files are .xls and the output files are .xlsx. The model
fits can also be save as .png images at the users request.
