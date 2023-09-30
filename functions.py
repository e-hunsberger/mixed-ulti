import streamlit as st
import pandas as pd
#load session states
#line is a list, point data is an array of dataframes
def load_session_states(ss):
    #if an oponent name has been added start collecting stats
    if 'opponent_name' in ss:
        opponent_name = ss['opponent_name'] 

    else: 
        opponent_name = None

    if 'team_df' in ss:
        team_df = ss.team_df
    else: 
        team_df = None

    if 'first_point_gender' in ss:
        first_point_gender = ss.first_point_gender

    else:
        first_point_gender = None

    if 'line' in ss:
        line = ss.line
    else:
        line = None

    if 'point_data' in ss:
        point_data = ss.point_data
    else:
        point_data = None

    
    
    return opponent_name, team_df, first_point_gender, line, point_data

#create default euphoria roster
def make_euphoria_roster():

    euphoria_roster = pd.DataFrame(
        [
            {"name": "Aishah", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},
            {"name": "Christine", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},
            {"name": "Esther", "number": 00, "gender match":'female',"position":'handler',"line":'defense'},
            {"name": "Evelyn", "number": 00, "gender match":'female',"position":'cutter',"line":'offense'},
            {"name": "Gigi", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},
            {"name": "Hazel", "number": 00, "gender match":'female',"position":'hybrid',"line":'defense'},
            {"name": "Jo", "number": 00, "gender match":'female',"position":'cutter',"line":'defense'},
            {"name": "Christine", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},
            {"name": "Merchu", "number": 00, "gender match":'female',"position":'cutter',"line":'defense'},
            {"name": "Meg", "number": 00, "gender match":'female',"position":'cutter',"line":'offense'},
            {"name": "Petra", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},
            {"name": "Spyke", "number": 00, "gender match":'female',"position":'handler',"line":'offense'},

            {"name": "Anthony", "number": 00, "gender match":'male',"position":'hybrid',"line":'defense'},
            {"name": "Ben Chong", "number": 00, "gender match":'male',"position":'cutter',"line":'defense'},
            {"name": "Binh", "number": 00, "gender match":'male',"position":'cutter',"line":'defense'},
            {"name": "Dan", "number": 00, "gender match":'male',"position":'cutter',"line":'offense'},
            {"name": "Elliot", "number": 00, "gender match":'male',"position":'handler',"line":'offense'},
            {"name": "Ethan", "number": 00, "gender match":'male',"position":'cutter',"line":'defense'},
            {"name": "Greg", "number": 00, "gender match":'male',"position":'handler',"line":'offense'},
            {"name": "Jackson", "number": 00, "gender match":'male',"position":'cutter',"line":'defense'},
            {"name": "Kesh", "number": 00, "gender match":'male',"position":'handler',"line":'offense'},
            {"name": "Luke", "number": 00, "gender match":'male',"position":'handler',"line":'defense'},
            {"name": "Mitch", "number": 00, "gender match":'male',"position":'hybrid',"line":'defense'},


        ]
    )



    return euphoria_roster 

#save session states
def save_session_states(first_point_gender,first_point_line,score_us,score_them):

    if first_point_gender not in st.session_state:
        st.session_state.first_point_gender = first_point_gender
    
    if first_point_line not in st.session_state:
        st.session_state.first_point_line = first_point_line






def get_gender_of_point(first_point_gender,score):
    #if the first point is F
    if first_point_gender == 'F':
        #create dict of gender for each total score
        score_gender_dict = {
            0:'F',1:'M',2:'F',3:'F',4:'M'
        }
    
    else:
        score_gender_dict = {0:'M',1:'F'

        }

    point_gender = score_gender_dict[score] 

    return point_gender


def set_point_info(us_score,them_score,point_gender,line_type):
    st.sidebar.subheader("score: " + str(us_score+them_score))
    st.sidebar.markdown("(us: " + str(us_score) + ", them: " + str(them_score) + ")")
    st.sidebar.subheader("gender match: " + point_gender )
    st.sidebar.subheader("line: " + line_type)


def save_line(line,team_df):
    st.dataframe(team_df[team_df.name.isin(line)].name.unique())
    st.session_state.line = team_df[team_df.name.isin(line)].name.unique()