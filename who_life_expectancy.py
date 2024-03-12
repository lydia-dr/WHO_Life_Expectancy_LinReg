import numpy as np
import streamlit as st

st.set_page_config(page_title=" title :)",
                   page_icon=":hourglass:",
                   layout="centered")

custom_css = """
<style>
    html, body, [class*="css"] {
        font-size: 16px !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def model_selector():
    """
    Allows a selection of model based on consent to using advanced population data, which may include protected information for better accuracy.

    User Inputs:
    Consent y/n
    Returns:
    best_performing_model or minimalistic_model (var): name of the chosen model
    """
    consent = st.radio("Do you consent to using advanced population data, which may include protected information for better accuracy?", ('Yes', 'No'))
    if consent == 'Yes':
        return best_performing_model
    else:
        return limited_model

def get_data_from_user(model):
    """
    Gets needed data from user for model

    Args:
    model (var) : model to use to extract the relevant columns

    Returns:
    scaled_values (list): scaled values to implement in the model
    """
    # values empty list that will be filled with user input
    values = []
    units = {'GDP': '$ per capita', 'Adult Mortality': 'per 1000', 'Infant Deaths': 'per 1000'}
    for col in model['columns']:
        prompt = f'Provide a value for {col} ({units.get(col, "")}):'
        value = st.number_input(prompt, step=0.5, format="%f")
                
        values.append([col, value])
        # for models with GDP, we calculate the log
        if col == 'GDP':
            values[-1][1] = np.log(values[-1][1])
    # scaling the data (MinMaxScaler transformation)
    scaled_values = scale(values, scaler)
    return scaled_values

def scale(values, scaler):
    """
    Scales list of values using MinMaxScaler transformation

    Args:
    values (list) : tuples in the form (column, input value)
    scaler (dic)  : Dictionary with columns as keys and dictionaries of mins and maxes as values

    Returns:
    scaled_list (list): scaled list of input values
    """
    scaled_list = []
    for col, value in values:
        X_std = (value - scaler[col]['min']) / (scaler[col]['max'] - scaler[col]['min'])
        #    X_scaled = X_std * (1 - 0) + 0 #default max is 1, min is 0. It's usually * (max - min) + min
        scaled_list.append(X_std)
    return scaled_list

def life_expectancy_predictor(model, scaled_values):
    """
    Performs Life Expectancy prediction using a specificed model with the data provided by the user.

    Args:
    model (dic) : model to use for the prediction
    scaled_values (list) : scaled values to use for the prediction

    Returns:
    life_expectancy_prediction (float) : predicted life expectancy

    """
    # initialising life_expectancy_prediction with the constant value
    life_expectancy_prediction = model['params'][0]
    # implementing the model
    for p, x in zip(model['params'][1:], scaled_values):
        life_expectancy_prediction += p*x
    # print statement with the final life expectancy prediction
    if 40.639251 < life_expectancy_prediction < 97.072899:  # Predition within 3 standard deviation from the mean
        st.write('The estimated Life Expectancy is ', round(life_expectancy_prediction, 2))
    else:
        # Life Expectancy out of expected ranges
        st.warning('Warning: The estimated Life Expectancy is far out the expected range.')
        # Negative Life Expectancy retuns 0
        if life_expectancy_prediction < 0:
            life_expectancy_prediction = 0
        st.write('The estimated life expectancy is: ', round(life_expectancy_prediction, 2))
    # returns life_expectancy_prediction value (float) in case it is wanted for futher use
    return life_expectancy_prediction

def main ():
    st.image('https://www.icn.ch/sites/default/files/styles/icn_free_ratio/public/2023-06/WHO.jpg?h=960eb3b3&itok=autONhTv', use_column_width=True)
    st.title('WHO Life Expectancy Predictor')
    model = model_selector()
    scaled_values = get_data_from_user(model)
    life_expectancy_predictor(model, scaled_values)

# # This version of the main function where you have to press a button to predict life expectancy
# def main ():
#     st.image('https://www.icn.ch/sites/default/files/styles/icn_free_ratio/public/2023-06/WHO.jpg?h=960eb3b3&itok=autONhTv', use_column_width=True)
#     st.title('WHO Life Expectancy Predictor')
#     model = model_selector()
#     scaled_values = get_data_from_user(model)
    
#     # Add a button to trigger life expectancy prediction
#     if st.button('Predict Life Expectancy'):
#         life_expectancy_predictor(model, scaled_values)

# DATA
best_performing_model = {'columns':['Adult Mortality', 'Infant Deaths', 'GDP'], 'params' : [76.6453, -30.258006, -17.446125, 4.720947]}
limited_model = {'columns':['Adult Mortality', 'GDP'], 'params' : [71.265829, -40.091971, 12.347190]}
scaler = {'GDP': {'max': 11.629979 , 'min': 4.997212}, 'Adult Mortality': {'max': 703.677, 'min': 49.384}, 'Year': {'max': 2015, 'min': 2000},'Infant Deaths': {'max': 135.6, 'min': 1.8}}

if __name__ == "__main__":
    main()