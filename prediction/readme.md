# Prediction module

Build docker image

```
docker build -t  prediction_module .
```

Run the image

```
docker run -d -p 5000:5000 prediction_module
```

Test it

```
curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/predict
```

Kill the container:

```
docker kill <container id>
```

## Models data directory

This directory contains data with ML models and features. Directory structure:

```
models_data
├── model name (example: autoencoder)
│    ├── carBodyId (example: CG33)
│    │   ├── voltageProgramType(example: 2000)
│    │   │   ├── models
│    │   │   │     ├── model file for bus 1
│    │   │   │     ├── model file for bus 2
│    │   │   │     ├── model file for bus 3
│    │   │   │     └── model file for bus 4
│    │   │   └── features
│    │   │         └── file containing features
│    │   └── ...
│    ├── ...
│    └── general (directory with general model - support all cases when carBodyId or voltageProgramType not in path-tree)        
│         ├── models
│         ├── features
│         └── body_voltage_pair_encoder
│                  └── file containing transformer for body-voltage pair
└── ...
```

### Models files

This is standalone model for specific bus. Contains all models information and structure - required to support
model-specific functions for predicting.

### Features file

It is dictionary which contains information required for good data preparing. It also contains threshold required for
anomaly detection. 

It is two-leveled dictionary. 

First keys contains bus names (each of K1, K2, K3, K4).

Second keys and values:
- threshold - required. Contains the threshold based on which the decision about the anomaly is made.
- model_file_name - required. It is a name of model attendant a specific bus - same as one from 'models' directory.
- payload_field_name_for_prediction_making - required. Payload field (preprocessing result on raw waveform) on the basis of which the prediction is made.
- encoder_file_name - required. It is a name of encoder attendant a specific bus.
- scaler_mean - optional. Mean of training data. Filled if data should be scaled before feeding the model. 
- scaler_var - optional. Variation of training data. Filled if data should be scaled before feeding the model. 
- result_mean - optional. Mean of output result in training phase. Filled if model result should be normalized. 
- result_var - optional. Variation of output result in training phase. Filled if model result should be normalized.  
- result_upper_bound - optional. If result has no upper-bound, this will be used to normalize the output.

### Body voltage pair encoder
File containing an encoder which is used with general model - car body type and voltage program type are encoded
to provide additional information to model. At the moment the encoder used is a one-hot transformer.    

### To run tests:
```
python -m pytest
```
