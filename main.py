import base64
import streamlit as st
import pickle
# from sklearn.metrics import accuracy_score
import pandas as pd
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("background.jpg")
# data:image/png;base64,{img}
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
width: 100%;
height:100%;
background-repeat: no-repeat;
background-attachment: fixed;
background-size: cover;
color: red; /* This changes the text color inside the main app container */
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
color: orange; /* Change sidebar text color */
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
color: red; /* Change header text color */
}}

[data-testid="stToolbar"] {{
right: 2rem;
color: orange; /* Change toolbar text color */
}}

h1, h2, h3, h4, h5, h6 {{
color: orange !important; /* Change all header text colors */
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

cities = ['Mumbai', 'Delhi', 'Chennai', 'Abu Dhabi', 'Visakhapatnam', 'Hyderabad', 'Chandigarh', 
          'Ahmedabad', 'Bangalore', 'Jaipur', 'Kolkata', 'Port Elizabeth', 'Cuttack', 'Navi Mumbai', 
          'Centurion', 'Bengaluru', 'Pune', 'Johannesburg', 'Dubai', 'Cape Town', 'Lucknow', 'Durban', 
          'Dharamsala', 'Indore', 'East London', 'Sharjah', 'Guwahati', 'Raipur', 'Ranchi', 'Nagpur', 
          'Kimberley', 'Bloemfontein']

teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Punjab Kings', 'Rajasthan Royals', 'Mumbai Indians', 
         'Delhi Capitals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Lucknow Super Giants', 
         'Gujarat Titans']

pipe = pickle.load(open('pipe.pkl','rb'))

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("""
    # **IPL VICTORY PREDICTOR**            
""")
# st.title("IPL Victory Predictor")

col1, col2 = st.columns(2)

with col1:
   
   batting_team =  st.selectbox('Select Batting Team',teams)

with col2:
    if batting_team == '--- select ---':
        bowling_team = st.selectbox('Select Bowling Team', teams)
    else:
        filtered_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Select Bowling Team', filtered_teams)

seleted_city = st.selectbox('Select Venue',cities)

target = st.number_input('Target')

col1,col2,col3 = st.columns(3)

with col1:
    score = st.number_input('Score')
with col2:
    overs = st.number_input("Over Completed")
with col3:
    wickets = st.number_input("wicktes down")

if st.button('Predict Winning Probability'):
    try:
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10-wickets
        crr = score/overs
        rrr = runs_left/(balls_left/6)
    
        input_data = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],
                         'city':[seleted_city],'runs_left':[runs_left],'balls_left':[balls_left],
                         'wickets_remaining':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})
       
        
        result = pipe.predict_proba(input_data)
    
        loss = result[0][0]
        win =  result[0][1]
        st.header(batting_team + " = "+str(round(win*100)) + "%")
        st.header(bowling_team + " = "+str(round(loss*100)) + "%")
    except:
        st.header("Some error occured.. Please check you inputs !!")
