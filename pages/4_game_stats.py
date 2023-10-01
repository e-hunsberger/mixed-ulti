import streamlit as st
from functions import *

st.set_page_config(
    page_title="Game Stats",
    page_icon="📈")

opponent_name, team_df, first_point_gender, first_point_line_type, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points = load_session_states(st.session_state)

#if an oponent name has been added start collecting stats
if 'opponent_name' in st.session_state:
    opponent_name = st.session_state['opponent_name'] 
    st.markdown('Stats for game versus ' + opponent_name + ':')

if 'team_df' in st.session_state:
    team_df = st.session_state.team_df

    st.markdown("Gender matchup breakdown:")
    st.dataframe(team_df.groupby('gender match').agg({'name':'nunique'}).rename(columns={'name':'gender match count'}))

    st.dataframe(all_points)
    

