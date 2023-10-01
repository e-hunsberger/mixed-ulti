import streamlit as st
import pandas as pd
from functions import *

st.set_page_config(
    page_title="Make team",
    page_icon="🤝")
st.markdown("Make team page")

opponent_name, team_df, first_point_gender, first_point_line_type, line, point_data, us_score, them_score, point_gender, line_type, current_O_D = load_session_states(st.session_state)
load_euphoria_roster = st.toggle("load euphoria roster?",True)

if (team_df is None or len(team_df) == 0) and (load_euphoria_roster == False):
    
    team_df = pd.DataFrame(
        [
        {"name": "Anon", "number": 00, "gender match":'',"position":'',"line":''},
    ]
    )

    team_df['gender match'] = team_df['gender match'].astype(pd.CategoricalDtype(['female','male']))
    team_df['position'] = team_df['position'].astype(pd.CategoricalDtype(['handler','cutter','utility']))
    team_df['line'] = team_df['line'].astype(pd.CategoricalDtype(['offense','defense','hybrid']))

if (team_df is None or len(team_df) == 0) and (load_euphoria_roster == True):
    team_df = make_euphoria_roster()
      

edited_df = st.data_editor(team_df,num_rows='dynamic')

submit_team = st.button("submit team")  
if submit_team:
    st.session_state.team_df = edited_df





