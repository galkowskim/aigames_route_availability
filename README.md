# Route Availability - AIGAMES

### Authors: 
- Mikolaj Galkowski
- Lukasz Tomaszewski
- Hubert Bujakowski
- Wiktor Jakubowski
- Maja Andrzejczuk

------------------

## Data structure:
- **data** - main folder to store data and model
  - **statuses** - folder containg raw data (excluding weather data)
    - **preprocessed** - output of preprocessing scripts
  - **VIL_merc** - folder containing weather data
------------------

## Data preparation

Data prepraration modules available in preprocessor.py.


## Model training

`python3 model_training.py` - it trains model, runs evaluation, saves model and saves results from testset


------------------

## How to run demo

`streamlit run app.py` - web app
