import streamlit as st
import numpy as np
import pickle
from zipfile import ZipFile

# Load the model
dataset = './ipl_model.zip'
with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('The dataset is extracted')

model_filename = "ipl_model.pkl"
loaded_model = pickle.load(open(model_filename, "rb"))

# Function to predict score
def score_predict(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5, model=loaded_model):
    prediction_array = []

    # Batting Team Encoding
    teams = ['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 
             'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
             'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

    prediction_array += [1 if batting_team == team else 0 for team in teams]
    
    # Bowling Team Encoding
    prediction_array += [1 if bowling_team == team else 0 for team in teams]

    # Add match details
    prediction_array += [runs, wickets, overs, runs_last_5, wickets_last_5]
    prediction_array = np.array([prediction_array])
    
    pred = model.predict(prediction_array)
    return int(round(pred[0]))

# Streamlit app layout
st.title("IPL Score Prediction")
st.write("Enter match details:")

# User inputs
batting_team = st.selectbox("Select Batting Team", ['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 
                                                      'Kolkata Knight Riders', 'Mumbai Indians', 
                                                      'Rajasthan Royals', 'Royal Challengers Bangalore', 
                                                      'Sunrisers Hyderabad'])

bowling_team = st.selectbox("Select Bowling Team", ['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 
                                                      'Kolkata Knight Riders', 'Mumbai Indians', 
                                                      'Rajasthan Royals', 'Royal Challengers Bangalore', 
                                                      'Sunrisers Hyderabad'])

runs = st.number_input("Enter Runs Scored", min_value=0)
wickets = st.number_input("Enter Wickets Lost", min_value=0)
overs = st.number_input("Enter Overs Bowled", min_value=0.0, step=0.1)
runs_last_5 = st.number_input("Enter Runs Scored in Last 5 Overs", min_value=0)
wickets_last_5 = st.number_input("Enter Wickets Lost in Last 5 Overs", min_value=0)

if st.button("Predict Score"):
    predicted_score = score_predict(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5)
    st.success(f'Predicted Score: {predicted_score}')
