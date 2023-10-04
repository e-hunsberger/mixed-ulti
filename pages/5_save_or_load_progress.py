import streamlit as st
import pandas as pd
from functions import *

st.set_page_config(
    page_title="Save or load progress",
    page_icon="🤝")
st.title("Save or load progress")
opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)

download_checkpoint(all_points)
upload_from_checkpoint()