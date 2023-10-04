import streamlit as st
import pandas as pd
from functions import *

st.set_page_config(
    page_title="Set game info",
    page_icon="🤝")
st.title("Set game info")

opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)


#game start stats
st.markdown('Game-start stats:')

if 'opponent_name' not in st.session_state:
    opponent_name = st.text_input("Opponent name:")
else:
    opponent_name = st.text_input("Opponent name:",value=opponent_name,key='user')

st.session_state['opponent_name'] = opponent_name
first_point_gender = st.radio('Gender of first point:',['F','M'],horizontal = True)
first_point_line_type = st.radio('First point:',['O','D'], horizontal = True)
half_score = st.number_input('Half taken at:',min_value=0, step=1,value=7)
#save game start stats as session state
save_session_states(first_point_gender,first_point_line_type,us_score,them_score,half_score)


#set roster
roster_options = st.radio("Roster options: ",['load Euphoria roster','load roster from csv'])

if roster_options == 'load Euphoria roster':
    team_df = make_euphoria_roster()
    st.dataframe(team_df,use_container_width=True)
    st.session_state.team_df = team_df


else:
    st.warning("Option to load roster from csv not yet available",icon="⚠️")
        







