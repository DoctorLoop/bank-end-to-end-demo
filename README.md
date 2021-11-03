# bank-end-to-end-demo
## Overview
Overly simple example end-to-end solution for both predicting likelihoods of new customers subscribing to a product and the bulk upload of new tabular data for training further models

- Flask web app accepting, validating and correcting (potentially corrupted/incomplete) csv data and form input 
- Basic TensorFlow model trained on Bank Marketing Data Set (https://archive.ics.uci.edu/ml/datasets/bank+marketing)
- Coercion of csv data including NaN/missing values, incorrect types, missing or incorrectly named columns and filtering of unsolicited columns
- SQLite database for storing data parsed from uploaded csv files
- Jupyter notebook showing training of model

## Production Optimisations 
- Model optimisation (priority dependant i.e. compile to tf lite, deploy with TensorFlow Extended (TFX) framework)
- Feature selection / feature sensitivity analysis (linear feature selection through eigenvalues via PCA/random forest and other methods)
- Data augmentation
- Formal OpenAPI definition
- Prediction confidence intervals
- Error and usage logging
- Auditing framework

## Limitations/missing features/potential areas for improvement:
- No current facility to fine tune or retrain new models on additional data
- No current estimates of confidence/uncertainty of predictions
- No current checks for duplicate representation of records in uploaded csv data
 


