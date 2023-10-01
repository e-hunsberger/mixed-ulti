import streamlit as st
from functions import *

st.set_page_config(
    page_title="Track Point",
    page_icon="📋"
)

# Load session states
opponent_name, team_df, first_point_gender, first_point_line_type, line, point_data, us_score, them_score, point_gender, line_type, current_O_D = load_session_states(st.session_state)

#set score on sidebar
#score, gender, offense/defense (us_score,them_score,point_gender,line_type)
set_point_info(us_score,them_score,point_gender,line_type)

# Only start tracking points if you have set a team and line
if team_df is None:
    st.warning('Create team', icon="⚠️")
elif (line is None) or (len(line)) != 7:
    st.warning('Line not 7 players')
else:
    # Define column names for the DataFrame
    col_names = ['action'] + list(line)

    # Get the selected action type from the radio button

    st.title('Track point stats')
    #if currently offense, offer offensive actions, else offer defensive actions
    if current_O_D == 'O':
        actions = ["pick up disc","pass","bad look-of","turn","throwaway","⭐","score!"]
    else: 
        actions = ["pull","generate turn","shutdown D","handblock/footblock","space coverage","⭐"]

    selected_action = st.radio('Select Action:', actions,horizontal=True)
    selected_player = st.radio('Select Player:', list(line))
    idx = list(line).index(selected_player)

    if st.button('Add'):
        # Add new row to DataFrame
        new_row = [selected_action] + [False]*(idx) + [True] + [False]*(len(line)-idx-1)
        point_data = pd.concat([point_data,pd.DataFrame(data=[new_row], columns=col_names)],ignore_index=True)
        if selected_action == 'score!':
            us_score = us_score + 1
            st.session_state.us_score = us_score
            #recalculate next point gender 
            point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
            st.session_state.point_gender = point_gender
            #rerun immediately so score and gender update
            st.rerun()


        #if action was 'throwaway' or 'turn' switch from offensive actions to defensive actions
        if (selected_action == 'turn') or (selected_action == 'throwaway'):
            current_O_D = 'D'
        if (selected_action == "generate turn") or (selected_action == "handblock/footblock"):
            corrent_O_D = 'O'
    


    # Display DataFrame
    st.markdown("point " + str(them_score+us_score) + ":")
    st.dataframe(point_data, hide_index=True)

    if st.button('Undo'):
        point_data = point_data[0:len(point_data)-1]
        st.session_state.point_data = point_data


    #save data
    st.session_state.point_data = point_data
    st.session_state.line = line

    if st.button('Opponent scored'):
        them_score = them_score + 1
        st.markdown(them_score)
        st.session_state.them_score = them_score
        #recalculate next point gender 
        point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
        st.session_state.point_gender = point_gender
        #rerun immediately so score and gender update
        st.rerun()

    if st.button('Undo opponent socre'):
        them_score = them_score - 1
        st.session_state.them_score = them_score
        #recalculate next point gender 
        point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
        st.session_state.point_gender = point_gender
        #rerun immediately so score and gender update
        st.rerun()