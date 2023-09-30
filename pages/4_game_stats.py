import streamlit as st


st.set_page_config(
    page_title="Game Stats",
    page_icon="📈")

#if an oponent name has been added start collecting stats
if 'opponent_name' in st.session_state:
    opponent_name = st.session_state['opponent_name'] 
    st.markdown('Stats for game versus ' + opponent_name + ':')

if 'team_df' in st.session_state:
    team_df = st.session_state.team_df

    st.markdown("Gender matchup breakdown:")
    st.dataframe(team_df.groupby('gender match').agg({'name':'nunique'}).rename(columns={'name':'gender match count'}))

