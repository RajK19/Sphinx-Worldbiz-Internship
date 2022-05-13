import streamlit as st
import pickle
import pandas as pd

st.title('Cricket Win Probability Predictor - IPL')
st.subheader('In this Project, we will be predicting the win probabilities of IPL Teams, '
             'where the input values are given by user for the team batting (i.e 2nd innings)')

teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah','Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
col1,col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select a Batting Team',sorted(teams, reverse=True))

with col2:
    bowling_team = st.selectbox('Select a Bowling Team', sorted(teams, reverse=True))

selected_city = st.selectbox('Select Host City', sorted(cities, reverse=True))

target = st.number_input('Target Score')

col3,col4,col5 = st.columns(3)

with col3:
    curr_score = st.number_input('Current Score')

with col4:
    comp_overs = st.number_input('Overs Completed')

with col5:
    wickets_fallen = st.number_input('Wickets Fallen')


if st.button('Show Win Probabilities'):
    runs_left = target - curr_score
    balls_left = 120 - (comp_overs*6)
    wickets_left = 10 - wickets_fallen
    crr = curr_score/comp_overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team],
                  'bowling_team':[bowling_team],
                  'city':[selected_city],
                  'runs_left': [runs_left],
                  'balls_left': [balls_left],
                  'wickets_left': [wickets_left],
                  'actual_target_score':[target],
                  'crr':[crr],
                  'rrr':[rrr]})

    #st.table(input_df)

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result [0][1]
    #st.text (result)
    st.subheader(batting_team + " -     " + str(round(win*100)) + '%')
    st.subheader(bowling_team + " -     " + str(round(loss*100)) + '%')

