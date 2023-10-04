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
        actions = ["pick up disc","pass","bad look-off","turn","throwaway","⭐","score!"]
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
        new_row = [selected_action] + [False]*(idx) + [True] + [False]*(len(line)-idx-1) + [counter]
        point_data = pd.concat([point_data,pd.DataFrame(data=[new_row], columns=col_names + ['action_counter'])],ignore_index=True)
        if selected_action == 'score!':
            #get gender and line type of the point before it changes
            temp_gender = get_gender_of_point(first_point_gender,us_score + them_score)
            temp_line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)
            st.session_state.temp_gender = temp_gender
            st.session_state.temp_line_type = temp_line_type
            us_score = us_score + 1
            st.session_state.us_score = us_score
            #recalculate next point gender 
            point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
            #recalculate the next point line type
            line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)
            #save the results
            st.session_state.line_type = line_type
            st.session_state.point_gender = point_gender
            st.session_state.point_data = point_data
            st.dataframe(point_data[col_names], hide_index=True)

            #rerun immediately so score and gender update
            st.rerun()


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
        point_data = point_data[0:len(point_data)-1]
        st.session_state.point_data = point_data
        st.rerun()


    #save data
    st.session_state.point_data = point_data
    st.session_state.line = line

    if st.button('Opponent scored'):
        #get gender and line type of the point before it changes
        temp_gender = get_gender_of_point(first_point_gender,us_score + them_score)
        temp_line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)
        st.session_state.temp_gender = temp_gender
        st.session_state.temp_line_type = temp_line_type
        them_score = them_score + 1
        st.markdown(them_score)
        st.session_state.them_score = them_score
        #recalculate next point gender 
        point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
        #recalculate the next point line type
        line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)

        #save the results
        st.session_state.line_type = line_type
        st.session_state.point_gender = point_gender
        #rerun immediately so score and gender update
        st.rerun()

    if st.button('Undo opponent score'):
        #so get the gender and line_type of the PREVIOUS score to use for when saving the point
        temp_gender = get_gender_of_point(first_point_gender,us_score + them_score)
        temp_line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)
        st.session_state.temp_gender = temp_gender
        st.session_state.temp_line_type = temp_line_type
        them_score = them_score - 1
        st.session_state.them_score = them_score
        #recalculate next point gender 
        point_gender = get_gender_of_point(first_point_gender,us_score+them_score)
        #recalculate the next point line type
        line_type = get_line_type_of_point(first_point_line_type,us_score,them_score,half_score)

        #save the results
        st.session_state.line_type = line_type
        st.session_state.point_gender = point_gender
        #rerun immediately so score and gender update
        st.rerun()

    #when ready, save the point (point will be saved as a dataframe concantenated with all points df)
    #add extra columns for the opponent name, offensive vs defensive point, gender, us score, them score
    #when the score is recorded, the line type and point gender are updated


    with st.form('submit point'):
        if point_data is not None:

            #if the last row contains a score, lower our score inputted (bc otherwise it will increase BEFORE saving)
            #else assume the other team scored and lower their score
            #'score' tracks the score of the game DURING the point
            if 'score' in point_data.action:
                us_score = us_score - 1
            else:
                them_score = them_score - 1
            point_data['us_score'] = us_score
            point_data['them_score'] = them_score
            point_data['score'] = us_score + them_score

            st.markdown(them_score)
            point_data['opponent'] = ''
            point_data['line_type'] = temp_line_type
            point_data['point_gender'] = temp_gender

            # Melt the DataFrame to combine selected columns into a new column
            melted_df = pd.melt(point_data, id_vars=['action','line_type','point_gender','us_score','them_score','score','action_counter'], value_vars=list(line),
                        var_name='name', value_name='action_bool')
            
            all_points = pd.concat([all_points,melted_df])
            if st.form_submit_button(label='Submit point into system'):
                st.session_state.all_points = all_points
                #clear the current point by removing from session state
                del st.session_state.point_data
                point_data = None
                st.success('Point submitted!')
                st.rerun()
    


    st.sidebar.markdown('--------------------------------------')
    st.sidebar.title('Save progress')
    # download_checkpoint(all_points)
    # upload_from_checkpoint()

        #try melting/pivoting to have names become a column called name, then groupby name and other attributes