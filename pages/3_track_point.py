import streamlit as st
from functions import *

st.set_page_config(
    page_title="Track Point",
    page_icon="📋"
)

# Load session states
opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)

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

    st.title('Track point')
    #if currently offense, offer offensive actions, else offer defensive actions
    if current_O_D == 'O':
        actions = ["pick up disc","pass","bad look-off","turn","throwaway","⭐","assist","score!"]
    else: 
        actions = ["pull","generate turn","shutdown D","handblock/footblock","space coverage","⭐"]

    selected_action = st.radio('Select Action:', actions,horizontal=True)
    selected_player = st.radio('Select Player:', list(line))
    idx = list(line).index(selected_player)

    if st.button('Add'):
        # Add new row to DataFrame
        if point_data is None:
            counter = 0
        else:
            counter = len(point_data)
        new_row = [selected_action] + [False]*(idx) + [True] + [False]*(len(line)-idx-1) + [counter] + [current_O_D]
        point_data = pd.concat([point_data,pd.DataFrame(data=[new_row], columns=col_names + ['action_counter'] + ['current_O_D'])],ignore_index=True)


        #if action was 'throwaway' or 'turn' switch from offensive actions to defensive actions
        if (selected_action == 'turn') or (selected_action == 'throwaway'):
            st.session_state.current_O_D = 'D'
            st.session_state.point_data = point_data
            st.dataframe(point_data[col_names], hide_index=True)
            st.rerun()
        if (selected_action == "generate turn") or (selected_action == "handblock/footblock"):
            st.session_state.current_O_D = 'O'
            st.session_state.point_data = point_data
            st.dataframe(point_data[col_names], hide_index=True)
            st.rerun()
    


    # Display DataFrame
    st.markdown("point " + str(them_score+us_score) + ":")
    if (point_data is not None):
        st.dataframe(point_data[col_names], hide_index=True)

    if st.button('Undo last action'):
        prev_action = point_data[len(point_data)-1:len(point_data)].action.values
        point_data = point_data[0:len(point_data)-1]
        #set current O or D to the O or D of the previous point so the action options are current
        #if the previous action was an offensive action, set current_O_D to O, else set to D
        if prev_action in ["pick up disc","pass","bad look-off","turn","throwaway","⭐","assist","score!"]:
            current_O_D = 'O'
        else:
            current_O_D = 'D'
        st.session_state.current_O_D = current_O_D
        st.session_state.point_data = point_data
        st.rerun()


    #save data
    st.session_state.point_data = point_data
    st.session_state.line = line

    opponent_scored_bool = st.checkbox('Opponent scored',value=False)

    with st.form('submit point'):
        if point_data is not None:
            point_data['us_score'] = us_score
            point_data['them_score'] = them_score
            point_data['score'] = us_score + them_score
            point_data['opponent'] = opponent_name
            point_data['line_type'] = line_type
            point_data['point_gender'] = point_gender

            # Melt the DataFrame to combine selected columns into a new column
            melted_df = pd.melt(point_data, id_vars=['action','line_type','point_gender','us_score','them_score','score','action_counter','current_O_D'], value_vars=list(line),
                        var_name='name', value_name='action_bool')
            
            all_points = pd.concat([all_points,melted_df])
            if st.form_submit_button(label='Submit point into system'):
                st.session_state.all_points = all_points
                #clear the current point by removing from session state
                del st.session_state.point_data
                point_data = None
                st.success('Point submitted!')
                #save session states and update score
                if opponent_scored_bool == True:
                    them_score = them_score + 1
                    st.session_state.them_score = them_score 
                else:
                    us_score = us_score + 1
                    st.session_state.us_score = us_score 
                #recalculate next point gender 
                point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
                #recalculate the next point line type
                line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)
                #save the results
                st.session_state.line_type = line_type
                st.session_state.point_gender = point_gender

                st.rerun()
    


