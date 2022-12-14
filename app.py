import streamlit as st
import pickle
import numpy as np
import pandas as pd

from streamlit_option_menu import option_menu
from PIL import Image

df = pd.read_csv('Data/rainfall.csv')

st.set_page_config(
    page_title='Rainfall Prediction', 
    page_icon='Image/cloud-rain.png',  
    initial_sidebar_state = 'auto')

st.title('Rainfall Prediction')

def home():
    st.write("###### Accuracy of rainfall forecasting has great importance for countries like Bhutan whose economy is largely dependent on hydro-power project and agriculture. ")
    st.title('Machin Learning')
    st.write('Machine learning (ML) is a type of artificial intelligence (AI) that allows software applications to become more accurate at predicting outcomes without being explicitly programmed to do so. Machine learning algorithms use historical data as input to predict new output values.')
    st.title('Prediction Accuracy')
    st.write('The accuracy of the our model is 74.2 percentage on train dataset and it is 64.9 persentage on test dataset.')
    st.write()

    col1, col2 = st.columns(2)

    with col1:

        st.write("###### Pipeline")
        st.write("Train set accuracy: ", 0.742)
        st.write("Test set accuracy : ", 0.649)
        st.write('MSE', 0.602)
        st.write('RMSE', 0.609)
    
    with col2:

        st.write("###### Decision Tree Accuracy")
        st.write("Train set accuracy: ", 0.731)
        st.write("Test set accuracy : ", 0.527)
        st.write('MSE', 0.488)
        st.write('RMSE', 0.698)

    st.write('')

    col1, col2 = st.columns(2)

    with col1:

        st.write("###### KNN Accuracy")
        st.write("Train set accuracy: ", 0.81)
        st.write("Test set accuracy : ", 0.633)
        st.write('MSE', 0.378)
        st.write('RMSE', 0.615)

    with col2:

        st.write("###### Linear Regression")
        st.write("Train set accuracy: ", 0.479)
        st.write("Test set accuracy : ", 0.489)
        

def predict_page():
    st.title('Enter & Predict!')

    model = pickle.load(open('Model/model.pkl', 'rb'))

    location_array = ['Paro','Simkotha','Haa','Kanglung','Mongar',
    'Chamkhar','Deothang','Punakha','Pemagatshel','Tashiyangtse']

    location_array_encoded = [5, 6, 7, 9, 0, 1, 2, 3, 4, 8]
    
    year_array = []
    year_start= 2000
    year_end = 2100

    for i in range(year_start, year_end):
        year_array.append(i)

    month_array = ['JAN','FEB','MAR','APR','MAY',
    'JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    
    location_input = st.selectbox('Location', location_array)

    col1, col2 = st.columns(2)

    with col2:
        month_input = st.selectbox('Month', month_array)
        minT = st.number_input('Min Temperature')
        ws = st.number_input('WS (Wind Speed)')
        
    for i in location_array:
        if location_input == i:
            location_data = location_array_encoded[location_array.index(i)]

    for i in month_array:
        if month_input == i:
            month_data = month_array.index(i)+1

    with col1:
        year = st.selectbox('Year',year_array)
        maxT = st.number_input('Max Temperature (c)')
        rh = st.number_input('RH (Relative Humidity)')

    predict = st.button('Predict')

    if predict:
        input_data = (location_data, year, month_data, maxT, minT, rh, ws)
        input_data_as_numpy_array = np.asarray(input_data)
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        result = model.predict(input_data_reshaped)

        if (result>0):
            st.write('Rainfall', result[0].round(2),'mm')
        else:
            st.write('No rainfall')
    

def explore():
    st.title('Data Exploration & Data Visualization')
    exp = st.expander('Dataset')
    with exp:
        st.write('The dataset is collected from the National Center of Meteorology and Hydrology. The dataset contain features such as location, year, month, maximum temperature, minimum temperature, relative humidity, wind speed, and rainfall. The data was recorded from 2000 to 2021 from 10 different locations. The meteorology station records the values of the environmental variable every day for each year directly from the devices in the station.')
        st.dataframe(df,use_container_width=True)

    exp = st.expander('Heatmap')
    with exp:
        image = Image.open('./Image/heatmap.png')
        st.image(image, 'Heatmap')
    
    exp = st.expander('Data Description')
    with exp:
        image = Image.open('./Image/f1.png')
        st.image(image, 'Rainfall vs Max Temperature')
    
    
    
    


def team():
    st.title('Team Members')

    col1, col2, col3, col4 = st.columns(4)        
    
    with col1:
        image = Image.open('./Image/p1.jpg')
        st.image(image, 'Madav Dewrali')
        
    with col2:
        image = Image.open('./Image/p2.jpg')
        st.image(image, 'Kisan')

    with col3:
        image = Image.open('./Image/p3.jpg')
        st.image(image, 'Namgay Wangchuk')

    with col4:
        image = Image.open('./Image/p4.jpg')
        st.image(image, 'Kinzang Wangchuk')


selected = option_menu(
        menu_title = '',
        options=['Home','Predict','Explore','Team'],
        icons=['house','book','meta','people'] ,
        menu_icon='cast',
        default_index=0,
        orientation='horizontal',          
    )

if selected == 'Home':
    home()
if selected == 'Predict':
    predict_page()
if selected == 'Explore':
    explore()
if selected == 'Team':
    team()