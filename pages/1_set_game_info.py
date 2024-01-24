import streamlit as st
import pandas as pd
from functions import *

st.set_page_config(
    page_title="Set game info",
    page_icon="🤝")
st.title("Set game info")

opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)


#game start stats
st.markdown('Game-start settings:')

if 'opponent_name' not in st.session_state:
    st.session_state.opponent_name = ''
if st.session_state.opponent_name is '':
    opponent_name = st.text_input("Opponent name:")

else:
    opponent_name = st.text_input("Opponent name:",value=opponent_name,key='user')

if opponent_name is not '':
    st.success("Opponent name set as: " + opponent_name)
st.session_state['opponent_name'] = opponent_name



with st.form('Game start options:'):
    first_point_gender = st.radio('Gender of first point:',['F','M'],horizontal = True)
    first_point_line_type = st.radio('First point:',['O','D'], horizontal = True)
    half_score = st.number_input('Half taken at:',min_value=0, step=1,value=7)
    if st.form_submit_button():
    #save game start stats as session state
        save_session_states(first_point_gender,first_point_line_type,us_score,them_score,half_score)
        st.success('Submitted game start options (note: options will refresh when re-navigating to this page)')

#initialise team_df 
if 'team_df' not in st.session_state:
    st.session_state.team_df = None
else:
    team_df = st.session_state.team_df
if team_df is None:
    #set roster
    roster_options = st.radio("Roster options: ",['','load Euphoria roster','load Euphoric roster','load Manuka roster','load roster from csv'])

    if roster_options == 'load Euphoria roster':
        team_df = make_euphoria_roster()
        st.dataframe(team_df,use_container_width=True)
        st.session_state.team_df = team_df.sort_values(by=['gender match','name'])

    elif roster_options == 'load Euphoric roster':
        team_df = make_euphoric_roster()
        st.dataframe(team_df,use_container_width=True)
        st.session_state.team_df = team_df.sort_values(by=['gender match','name'])

    elif roster_options == 'load Manuka roster':
        team_df = pd.read_csv('C:\\Users\\ehuns\\OneDrive\\Documents\\Personal\\Ulti App\\manuka_roster.csv')
        st.dataframe(team_df,use_container_width=True)
        st.session_state.team_df = team_df.sort_values(by=['gender match','name'])

    elif roster_options == 'load roster from csv':
        uploaded_file = st.file_uploader("Upload roster as csv (columns: name, number, gender match, position, line)", type=["csv"])
        
        if uploaded_file is not None:
            uploaded_file = pd.read_csv(uploaded_file)
            #set all points
            team_df = pd.DataFrame(uploaded_file)
            team_df = team_df.sort_values(by=['gender match','name'])
            st.session_state.team_df = team_df

else: 
    st.warning('Team roster has already been set. To reset, click the refresh roster button below.')       

refresh_roster = st.button('Refresh roster')
if refresh_roster == True:
    st.session_state.team_df = None
    st.rerun()





