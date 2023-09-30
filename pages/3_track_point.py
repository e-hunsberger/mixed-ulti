import streamlit as st
from functions import *
# st.set_page_config(
#     page_title="Track Point",
#     page_icon="📋")


# opponent_name, team_df, first_point_gender, line, point_data = load_session_states(st.session_state)

# #only start tracking the points if you have set a team and line
# if team_df is None:
#     st.warning('Create team',icon="⚠️")
# elif (line is None) or (len(line)) != 7:
#     st.warning('Line not 7 players')
# else:
#     #load data for the point
#     # data_point = {'name': line,'pass':False,}
#     col_names = ['action'] + list(line)
#     action_type = st.radio("",["pick up disc","pull","pass","throwaway","D","something special"],horizontal=True)
#     data_row = [[action_type] + [False]*(len(col_names)-1)]
#     #load previous point data and append new data 
#     #only add new row if a checkbox has been filled in the last row
#     if (point_data is not None) and (point_data.iloc[len(point_data)-1,:][line].sum() > 0):
#         st.markdown('here')
#         st.markdown(point_data.iloc[len(point_data)-1,:][line].sum())
#         data = pd.concat([point_data,pd.DataFrame(data=data_row,columns=col_names)],axis=0,ignore_index=True)
#     else:
#         data = data_row.copy()
#     #load previous data from point
#     data_tracker = pd.DataFrame(data,columns=col_names,
#                                 )

#     point_data = st.data_editor(data_tracker,hide_index=True,num_rows='dynamic')
#     st.dataframe(point_data)
#     st.session_state.point_data = point_data

#     st.session_state.line = line

import streamlit as st
import pandas as pd
from functions import *  # Assuming functions.py contains your helper functions

st.set_page_config(
    page_title="Track Point",
    page_icon="📋"
)

# Load session states
opponent_name, team_df, first_point_gender, line, point_data = load_session_states(st.session_state)

# Only start tracking points if you have set a team and line
if team_df is None:
    st.warning('Create team', icon="⚠️")
elif (line is None) or (len(line)) != 7:
    st.warning('Line not 7 players')
else:
    # Define column names for the DataFrame
    col_names = ['action'] + list(line)

    # Get the selected action type from the radio button
    action_type = st.radio("Select Action", ["pick up disc", "pull", "pass", "throwaway", "D", "something special"], horizontal=True)

    player = st.radio('player: ',[''] + list(line),horizontal=True,index=0)
    # Check if any checkbox is selected, add a new row if true
    if player != '':
        # Initialize a new row with False values
        new_row = [False] * len(col_names)
        new_row[0] = action_type  # Set the action type

        if (point_data is None) or (len(point_data) == 0):
            point_data = pd.DataFrame(data = [new_row],columns=col_names)
        else:
            point_data = point_data.append(pd.Series(new_row, index=col_names), ignore_index=True)
        #replace False with true for the player selected
        point_data.iloc[len(point_data)-1,:][player] = True
        st.dataframe(point_data)

    # Display the point data table and save it in the session state
    st.dataframe(point_data, hide_index=True)
    st.session_state.point_data = point_data
    st.session_state.line = line
