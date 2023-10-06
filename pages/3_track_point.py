import streamlit as st
from functions import *
import numpy as np

st.set_page_config(
    page_title="Track Point",
    page_icon="📋"
)

# Load session states
opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type = load_session_states(st.session_state)

#set score on sidebar

# Only start tracking points if you have set a team and line
if team_df is None:
    st.warning('Create team', icon="⚠️")

else:
    if (line is None) or (len([item for item in line if item != 'other team']) != 7):
        st.warning('Line not 7 players')

    # Define column names for the DataFrame
    col_names = ['action'] + list(line)

    # Get the selected action type from the radio button

    st.title('Track point')
    st.markdown('Currently on: ' + current_O_D)
    #if currently offense, offer offensive actions, else offer defensive actions
    if current_O_D == 'O':
        actions = ["pick up disc","pass","bad look-off","turn","throwaway","⭐","assist","score!"]
    else: 
        actions = ["pull","generate turn","shutdown D","handblock/footblock","space coverage","⭐","opponent throwaway","opponent score"]

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
        if (selected_action == 'turn') or (selected_action == 'throwaway') or (selected_action == "score!"):
            st.session_state.current_O_D = 'D'
            st.session_state.point_data = point_data
            st.dataframe(point_data[col_names], hide_index=True)
            st.rerun()
        if (selected_action == "generate turn") or (selected_action == "handblock/footblock") or (selected_action == "opponent throwaway") or (selected_action == "opponent score"):
            st.session_state.current_O_D = 'O'
            st.session_state.point_data = point_data
            st.dataframe(point_data[col_names], hide_index=True)
            st.rerun()
    


    # Display DataFrame
    st.markdown("point " + str(them_score+us_score) + ":")
    if (point_data is not None):
        st.dataframe(point_data[col_names], hide_index=True)

    if st.button('Undo last action'):
    
        if point_data is None:
            st.warning('Cannot undo a point that has already been submitted', icon="⚠️")
            # st.dataframe(all_points)
            
            # last_score = all_points.score.max()
            # point_data = all_points[all_points.score == last_score]
            # point_gender = point_data.point_gender.mode()
            # line_type = point_data.line_type.mode()
            # test = point_data.pivot(index=['name'],columns=['action'], values=['action_bool'])
            # st.dataframe(test)





        else:
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

    # opponent_scored_bool = st.checkbox('Opponent scored',value=False)

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
                st.success('Point submitted!')
                #save session states and update score
                if (point_data is not None) and (point_data[len(point_data)-1:len(point_data)].action.values == 'opponent score'): #opponent_scored_bool == True:
                    them_score = them_score + 1
                    st.session_state.them_score = them_score 
                    
                elif (point_data is not None) and (point_data[len(point_data)-1:len(point_data)].action.values == 'score!'):
                    us_score = us_score + 1
                    st.session_state.us_score = us_score 
                del st.session_state.point_data
                point_data = None

                #recalculate next point gender 
                point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
                #recalculate the next point line type
                get_line_type_of_point(all_points,first_point_line_type,us_score,them_score,half_score) 
                #save the results
                st.session_state.line_type = line_type
                st.session_state.point_gender = point_gender
                st.session_state.current_O_D = line_type
                st.success('Point submitted!')

                st.rerun()

    st.markdown('-------')
    st.markdown('If error, force a change below:')
    force_gender_change = st.checkbox('Force gender match change?')
    force_line_type_change = st.checkbox('Force offsense/defense change?')
    force_us_score_change = st.checkbox('Force score change for our team?')
    force_them_score_change = st.checkbox('Force score change for them?')
    


    with st.form('Force change:'):
        
        if force_gender_change:
            gender_change = st.radio("Gender match change: ",['F','M'])
        if force_line_type_change:
            line_type_change = st.radio("Offense/Defense change: ",['O','D'])
        if force_us_score_change:
            us_score_change = st.number_input('Our score:',min_value=0, step=1,value=us_score)
        if force_them_score_change:
            them_score_change = st.number_input('Opponent score:',min_value=0, step=1,value=them_score)

        if st.form_submit_button(label='Submit force change'):
            if force_gender_change:
                point_gender = gender_change
                st.session_state.point_gender = point_gender

            if force_line_type_change:
                line_type = line_type_change
                st.session_state.line_type = line_type
                st.session_state.current_O_D = line_type

            if force_us_score_change:
                us_score = us_score_change
                st.session_state.us_score = us_score

            if force_them_score_change:
                them_score = them_score_change
                st.session_state.them_score = them_score

            st.rerun()


        
    

    #score, gender, offense/defense (us_score,them_score,point_gender,line_type)
    set_point_info(us_score,them_score,point_gender,line_type)

