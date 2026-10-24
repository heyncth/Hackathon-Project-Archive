---
id: storm-prophet
name: Storm Prophet
description: LSTM model that predicts geomagnetic storm levels from DSCOVR satellite data.
domain: science
tags: [space-weather, ai-ml, nasa-space-apps]
event:
  name: NASA Space Apps Challenge
  year: 2023
  award: Best Use of Data
evidence:
  - url: https://www.spaceappschallenge.org/blog/the-nasa-space-apps-challenge-live-global-winners-announcement/
    supports: "Space Apps 2023 Best Use of Data award"
verified_at: 2026-10-24
---

## What it is

Storm Prophet is a machine learning model that predicts geomagnetic storm levels. It reads solar wind data from the DSCOVR satellite.

## The problem

A geomagnetic storm can disrupt satellites, GPS, and power grids. Forecasters need lead time, and the solar wind gives only about an hour.

## What makes it interesting

It won Best Use of Data at NASA Space Apps 2023. The project uses an LSTM on a time series, which is a sensible fit for a signal that unfolds over time.

## What you can learn

In forecasting, the baseline matters more than the model. A prediction is useful only if it beats the current operational method.

## Limitations of this analysis

The record does not report accuracy or comparison against existing forecasts.
