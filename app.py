import pickle
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


pickle_in = open('regressor.pkl', 'rb') 
model = pickle.load(pickle_in)

def ret_province(city):
    if city == 'Karachi':
        return ['Sindh']
    elif city == 'Islamabad':
        return ['Islamabad Capital']
    elif city == 'Lahore' or 'Rawalpindi' or 'Faisalabad':
        return ['Punjab']
 

def predict(model, input_df):
    prediction_array = np.array([input_df['property_type'][0], input_df['city'][0], input_df['province_name'][0],input_df['baths'][0], input_df['purpose'][0], input_df['bedrooms'][0],input_df['area_yard'][0]])              
    final_array = [prediction_array[0],prediction_array[1],prediction_array[2],prediction_array[3],prediction_array[4],prediction_array[5],prediction_array[6]]
    predictions = model.predict([final_array])
    return predictions

def run():   
    st.set_page_config(page_title='House Price Analysis App')
    st.sidebar.header('House Price Analysis App')
    image_loan = Image.open('house.png')

    # st.sidebar.image(image_loan,use_column_width=True)
    nav_value = st.sidebar.selectbox('Navigation',('Estimate House Rates', 'See the Trends', 'About Me'))
    st.sidebar.info('This app is analysis of housing dataset that contains information extracted from Pakistan\'s biggest property portal, Zameen.com')
    st.sidebar.success('http://saeed.js.org')
    if nav_value == 'See the Trends':
        st.title("Trends in House prices")
    if nav_value == 'About Me':
        st.title("About Me")
    if nav_value == 'Estimate House Rates':
        st.title("Estimate the market price using AI!")
        property_type = st.selectbox('Property Type', ['Flat', 'House'])
        property_cat = 0 if property_type == 'Flat' else 1

        col1, col2 = st.beta_columns(2)

        with col1:
            city = st.selectbox('City', ['Islamabad', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Karachi'])
            city_cat = 0 if city == 'Faisalabad' else 1 if city == 'Islamabad' else 2 if city == 'Karachi' else 3 if city == 'Lahore' else 4 
            baths = st.number_input('Baths', min_value=0, max_value=3, value=1)
            area_yard = st.number_input('Area (Yards)', min_value=60, max_value=1500, value=120)

        with col2:
            prov_arr =  ['Sindh', 'Punjab', 'Islamabad Capital']
            province_name = st.selectbox('Province',options = ret_province(city))
            prov_cat = 0 if province_name == 'Islamabad Capital' else 1 if province_name == 'Punjab' else 2
            bedrooms = st.selectbox('Bedrooms', [0,1,2,3])
            purpose = st.selectbox('Purpose', ['Sale', 'Rent'])
            purpose_cat = 0 if purpose == 'Rent' else 1

        output=""

        input_dict = {
                        'property_type' : property_cat,
                        'city' : city_cat,
                        'province_name' : prov_cat, 
                        'baths' : baths,
                        'purpose' : purpose_cat,
                        'bedrooms': bedrooms,
                        'area_yard': area_yard
                    }
        input_df = pd.DataFrame([input_dict])

        col3 = st.beta_columns(2)
        if st.button("Predict", ):
            output = predict(model=model, input_df=input_df)
            st.success('The estimated price is '+ str(int(output[0])) + ' PKR')

if __name__ == '__main__':
    run()