import streamlit as st
from functions import *
import plotly.express as px 

st.set_page_config(
    page_title="Game Stats",
    page_icon="📈")

opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)

st.title('Game stats')

if len(all_points) == 0:
    st.warning('No points to track',icon="⚠️")
else:

    test = ['all actions'] + list(all_points.action.unique())
    plot_action = st.radio('Count actions by: ',test,horizontal=True)

    df_grouped = all_points.groupby(['action','name'],observed=False).agg({'action_bool':'sum'}).reset_index()
    #join the team_df for information such as gender
    df_grouped_with_attributes = pd.merge(df_grouped,team_df,on='name',how='outer')
    if plot_action == 'all actions':
        fig = px.bar(df_grouped_with_attributes,x='name',y='action_bool',color='action')
    else:
        df_filtered = df_grouped_with_attributes[df_grouped_with_attributes.action == plot_action]
        fig = px.bar(df_filtered,x='name',y='action_bool',color='gender match')
    fig.update_layout(yaxis_title='Count',xaxis_title='Player',title='Actions by person')
    st.plotly_chart(fig,use_container_width=True)


    #gender plot
    actions_gender_df = pd.merge(all_points,team_df,on='name',how='outer').groupby(['gender match','action']).agg({'action_bool':'sum'}).reset_index()
    fig = px.bar(actions_gender_df,x='action',y='action_bool',color='gender match')
    fig.update_layout(yaxis_title='Count',xaxis_title='Action',title='Actions by gender match')
    st.plotly_chart(fig,use_container_width=True)

set_point_info(us_score,them_score,point_gender,line_type)