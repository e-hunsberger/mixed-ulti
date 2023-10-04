import streamlit as st
import pandas as pd
#load session states
#line is a list, point data is a dataframe
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
        first_point_gender = 'F'

    if 'first_point_line_type' in ss:
        first_point_line_type = ss.first_point_line_type
    else:
        first_point_line_type = None

    if 'line' in ss:
        line = ss.line
    else:
        line = None

    if 'point_data' in ss:
        point_data = ss.point_data
    else:
        point_data = None

    if 'us_score' in ss:
            us_score = ss.us_score
    else:
        us_score = 0 

    #int of opposition score
    if 'them_score' in ss:
            them_score = ss.them_score
    else:
        them_score = 0 

    #gender match of point (char 'F'/'M')
    if 'point_gender' in ss:
        point_gender = ss.point_gender
    elif first_point_gender is not None:
        point_gender = first_point_gender 
    #initialise with F but will switch later based on user selection
    else: 
        point_gender = 'F'
         

    #line type of point (char 'O'/'D')
    if 'line_type' in ss:
            line_type = ss.line_type
    elif first_point_line_type is not None:
        line_type = first_point_line_type
    #initialise with O, but will switch later based on user selection
    else:
        line_type = 'O' 

    #keep track of whether on O or D on the current point
    if 'current_O_D' in ss:
        current_O_D = ss.current_O_D
    elif line_type == 'O':
        current_O_D = 'O'
    elif line_type == 'D':
        current_O_D = 'D'
    else:
        current_O_D = None

    #dataframe of all points
    if 'all_points' in ss:
        all_points = ss.all_points
    else:
        all_points = pd.DataFrame()

    #score that half is taken at
    if 'half_score' in ss:
        half_score = ss.half_score
    else:
        half_score = 0

    if 'temp_gender' in ss:
        temp_gender = ss.temp_gender

    else:
        temp_gender = 'F'

    if 'temp_line_type' in ss:
        temp_line_type = ss.temp_line_type
    else:
        temp_line_type = 'O'

    return opponent_name, team_df, first_point_gender, first_point_line_type, half_score, line, point_data, us_score, them_score, point_gender, line_type, current_O_D, all_points, temp_gender, temp_line_type

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
def save_session_states(first_point_gender,first_point_line_type,score_us,score_them,half_score):

    st.session_state.first_point_gender = first_point_gender
    st.session_state.first_point_line_type = first_point_line_type
    st.session_state.score_us = score_us
    st.session_state.score_them = score_them
    st.session_state.half_score = half_score






def get_gender_of_point(first_point_gender,score):
    #if the first point is F
    if first_point_gender == 'F':
        #create dict of gender for each total score
        score_gender_dict = {-1:'placeholder',
            0:'F',1:'M',2:'F',3:'F',4:'M',5:'M',6:'F',7:'F',8:'M',9:'M',10:'F',11:'F',12:'M',13:'M',14:'F',15:'F',
            16:'M',17:'M',18:'F',19:'F',20:'M',21:'M',22:'F',23:'F',24:'M',25:'M',26:'F',27:'F',28:'M',29:'M',30:'F'
        }
    
    else:
        score_gender_dict = {-1:'placeholder',0:'M',1:'F'

        }

    point_gender = score_gender_dict[score] 

    return point_gender

#get whether the point is O or D
def get_line_type_of_point(first_point_line_type,us_score,them_score,half_score):
    score = us_score + them_score 
    #BEFORE HALF
    #if first point line type is F 
    if first_point_line_type == 'O':
        #then even points will be offense, unless someone is at half, then it will switch
        if score % 2 == 0:
            line_type = 'O'
        else:
            line_type = 'D'
    if first_point_line_type == 'D':
        #then even points will be offense, unless someone is at half, then it will switch
        if score % 2 == 0:
            line_type == 'D'
        else:
            line_type = 'O'

    #if it's past half, reverse the line type
    if (us_score > half_score) or (them_score > half_score):
        if line_type == 'O':
            line_type == 'D'
        if line_type == 'D':
            line_type == 'O'
    return line_type 








def set_point_info(us_score,them_score,point_gender,line_type):
    st.sidebar.title('Score Info:')
    st.sidebar.subheader("score: " + str(us_score+them_score))
    st.sidebar.markdown("(us: " + str(us_score) + ", them: " + str(them_score) + ")")
    st.sidebar.subheader("gender match: " + point_gender )
    st.sidebar.subheader("line: " + line_type)


def save_line(line,team_df):
    st.dataframe(team_df[team_df.name.isin(line)].name.unique())
    st.session_state.line = team_df[team_df.name.isin(line)].name.unique()

#download all the point data in case of page refresh
def download_checkpoint(all_points):
    st.markdown('Save progress by downloading a checkpoint:')
    st.download_button(label='Download checkpoint', data=all_points.to_csv(index=False), file_name='ulti_game_data.csv')

def upload_from_checkpoint():
    st.markdown('Upload data from a previous checkpoint:')
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        uploaded_file = pd.read_csv(uploaded_file)
        st.dataframe(uploaded_file)
        #set all points
        st.session_state.all_points = pd.DataFrame(uploaded_file)
        #set gender

        #set line type

        #check if anything else needs to be recalled from the old data
        uploaded_file = None
