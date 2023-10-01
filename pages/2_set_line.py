import streamlit as st
from functions import *
import plotly.express as px
st.set_page_config(
    page_title="Set Line",
    page_icon="📋")

opponent_name, team_df, first_point_gender, first_point_line_type, line, point_data, us_score, them_score, point_gender, line_type, current_O_D = load_session_states(st.session_state)


if team_df is None:
    st.warning('Create team',icon="⚠️")
else:
    if opponent_name is None:
        opponent_name = st.text_input("Opponent name:")

    st.session_state.opponent_name = opponent_name

    #game start stats
    st.markdown('Game-start stats:')
    first_point_gender = st.radio('Gender of first point:',['F','M'],horizontal = True)
    first_point_line_type = st.radio('First point:',['O','D'], horizontal = True)
    score_us = 0
    score_them = 0


    #save game start stats as session state
    save_session_states(first_point_gender,first_point_line_type,score_us,score_them,line_type)

    #temp:

    score = 0

    point_gender = get_gender_of_point(first_point_gender,score)
    #if you navigated away and want the line back, click load previous line
    load_previous_line = st.checkbox("load previous line")
    if load_previous_line == True:
        #if there was no previous line, give a warning
        if ('line' not in st.session_state):
            st.warning("No previous line to select",icon="⚠️")
        else:
            line = list(st.session_state.line)
            st.session_state.line = line
    else:
        #call line from scratch
        line = st.multiselect(
                'Players for ' + line_type + ' point:',
                team_df['name'])

    #create a warning if too many of one gender or too many players are selected
    if (line is not None):
        #create a warning if wrong gender is selected
        n_female = (team_df[(team_df.name.isin(line)) & (team_df['gender match'] == 'female')].name.nunique())
        n_male = (team_df[(team_df.name.isin(line)) & (team_df['gender match'] == 'male')].name.nunique())
        if (n_female == 4) and (point_gender == 'M'):
            st.warning('Wrong gender. Too many female-matching players.',icon="⚠️")
        elif (n_female > 4):
            st.warning('Too many female-matching players.',icon="⚠️")

        elif (n_male == 4) and (point_gender == 'F'):
            st.warning('Wrong gender. Too many male-matching players.')
        elif (n_male > 4):
            st.warning('Too many male-matching players.',icon="⚠️")
        elif (len(line) > 7 ):
            st.warning('Too many players selected', icon="⚠️")
        else:
            line_summary = (team_df[team_df.name.isin(line)]
                        .groupby(['position','gender match'])
                        .agg({'name':'nunique'}).reset_index()
                        .rename(columns={'name':'number of players'}))
            fig = px.bar(line_summary,x='position',y='number of players',color='gender match')
            st.plotly_chart(fig)
        
        
        #submit_line = st.button("submit line",on_click=save_line(line,team_df))
 

        if st.button("submit line"):
            st.session_state.line = team_df[team_df.name.isin(line)].name.unique()
    

        #make plot of balance between O/D players, handlers/cutters and whether gender is correct