import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image
import plotly.express as px
import hashlib
import os

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a user database if it doesn't exist
def create_user_database():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['Username', 'Password'])
        df.to_csv('users.csv', index=False)

# Function to register a new user
def register_user(username, password):
    df = pd.read_csv('users.csv')
    if username in df['Username'].values:
        return False  # User already exists
    new_user = pd.DataFrame({'Username': [username], 'Password': [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv('users.csv', index=False)
    return True  # User registered successfully

# Function to verify user credentials
def verify_user(username, password):
    df = pd.read_csv('users.csv')
    return any((df['Username'] == username) & (df['Password'] == hash_password(password)))

# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to right, #e0eafc, #cfdef3);
            font-family: 'Arial', sans-serif;
        }
        h1 {
            color: #333;
        }
        input {
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 300px;
            font-size: 16px;
        }
        button {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
            font-size: 16px;
        }
        .link {
            margin-top: 10px;
            color: #007BFF;
            text-decoration: none;
        }
        .link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function for the login page
def login_page():
    add_custom_css()
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_user(username, password):
            st.success("Login successful! Redirecting to the main page...")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "main"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

    if st.button("Register"):
        st.session_state.page = "register"
        st.experimental_rerun()

    st.markdown('<a class="link" href="#" onclick="st.session_state.page=\'register\'; st.experimental_rerun();">Need an account? Register here.</a>', unsafe_allow_html=True)

def register_page():
    add_custom_css()
    st.title("Register Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful! You can log in now.")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error("Username already exists. Choose a different one.")

    st.markdown('<a class="link" href="#" onclick="document.querySelector(\'.login\').scrollIntoView();">Already have an account? Log in here.</a>', unsafe_allow_html=True)

# Difficulty index calculation functions
def calculate_difficulty_index_simple(student_performance, feedback):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    difficulty_index = (performance_score + feedback_score) / 2
    return difficulty_index

def calculate_difficulty_index_weighted(student_performance, feedback, weight_performance=0.7, weight_feedback=0.3):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    difficulty_index = (weight_performance * performance_score) + (weight_feedback * feedback_score)
    return difficulty_index

def calculate_difficulty_index_harmonic(student_performance, feedback):
    performance_score = (sum(student_performance) / len(student_performance)) / 10
    feedback_score = sum(feedback) / len(feedback)
    if performance_score == 0 or feedback_score == 0:
        return 0
    difficulty_index = 2 * (performance_score * feedback_score) / (performance_score + feedback_score)
    return difficulty_index

# Map feedback categories to numerical values
feedback_mapping = {
    "More Difficult": 10,
    "Medium Difficult": 5,
    "Less Difficult": 2
}

# Function to visualize the data using Plotly
def visualize_data(course_data):
    fig = px.bar(course_data, x='Course', y='Difficulty Index', color='Difficulty Index',
                 title='Course Difficulty Index',
                 labels={'Difficulty Index': 'Difficulty Index'},
                 hover_data={'Difficulty Index': ':.2f'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)


def main_page():
    st.set_page_config(layout="wide")

    st.image("1485949524c5.webp", use_column_width=True)

    st.title("Engineering Course Difficulty Index Calculator")
    st.write(f"Welcome, {st.session_state.username}!")

    st.sidebar.image("images.jpeg", use_column_width=True)
    
    st.sidebar.markdown("## About Us")
    if st.sidebar.button("Meet the Team"):
        st.sidebar.image("images.png", caption="RenukaPrasad V G", use_column_width=True)
        st.sidebar.image("images (1).png", caption="Inchara Patel", use_column_width=True)
        st.sidebar.image("images (1).png", caption="Ranjitha ", use_column_width=True)
        st.sidebar.image("images.png", caption="Samrudh", use_column_width=True)

    # Algorithm selection
    st.sidebar.markdown("## Select Algorithm")
    algorithm = st.sidebar.selectbox(
        "Difficulty Index Calculation Algorithm",
        ("Simple Average", "Weighted Average", "Harmonic Mean")
    )

    # Select semester
    st.sidebar.markdown("## Select Semester")
    semester = st.sidebar.selectbox("Semester", range(1, 9))

    # Display courses for the selected semester
    st.sidebar.markdown("## Courses in Selected Semester")
    courses_by_semester = {
        1: ["Engineering Mathematics I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering"],
        2: ["Engineering Mathematics II", "Engineering Graphics", "Computer Programming", "Basic Electronics"],
        3: ["Engineering Mathematics III", "Data Structures", "Digital Logic Design", "Analog Electronics"],
        4: ["Computer Organization", "Software Engineering", "Operating Systems", "Microprocessors"],
        5: ["Database Management Systems", "Computer Networks", "Theory of Computation", "Design and Analysis of Algorithms"],
        6: ["Compiler Design", "Computer Graphics", "Artificial Intelligence", "Embedded Systems"],
        7: ["Machine Learning", "Big Data Analytics", "Cyber Security", "Cloud Computing"],
        8: ["Project Work", "Internship", "Elective I", "Elective II"]
    }
    courses = courses_by_semester[semester]
    # Display courses in a formatted way
    for course in courses:
        st.sidebar.write(f"- {course}")

    # Display available courses with resources and guides
    st.header("Available Courses with Resources and Guides")
    courses_info = {
        "Engineering Mathematics I": {
            "resources": ["Textbook: Advanced Engineering Mathematics", "Online Lecture: Khan Academy"],
            "guide": {"name": "Dr. A. Kumar", "photo": "images.jpeg"}
        },
        "Engineering Physics": {
            "resources": ["Textbook: University Physics", "Online Lecture: MIT OpenCourseWare"],
            "guide": {"name": "Dr. B. Sharma", "photo": "images.jpeg"}
        },
        "Engineering Chemistry": {
            "resources": ["Textbook: Engineering Chemistry", "Online Lecture: NPTEL"],
            "guide": {"name": "Dr. C. Patel", "photo": "images.jpeg"}
        },
        "Basic Electrical Engineering": {
            "resources": ["Textbook: Basic Electrical Engineering", "Online Lecture: Coursera"],
            "guide": {"name": "Dr. D. Rao", "photo": "images.jpeg"}
        },
        # Add more courses and their information here as needed
    }

    for course in courses:
        st.subheader(course)
        st.write("**Resources:**")
        for resource in courses_info.get(course, {}).get("resources", []):
            st.write(f"- {resource}")
        guide = courses_info.get(course, {}).get("guide", {})
        if guide:
            st.write("**Guide:**")
            st.image(guide["photo"], caption=guide["name"], width=100)

    # Upload CSV file
    st.sidebar.markdown("## Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if all(column in df.columns for column in ["Course", "Performance", "Feedback"]):
            course_data = []

            for course in courses:
                course_df = df[df['Course'] == course]
                performance_list = course_df['Performance'].tolist()
                feedback_list = course_df['Feedback'].map(feedback_mapping).tolist()
                
                if algorithm == "Simple Average":
                    difficulty_index = calculate_difficulty_index_simple(performance_list, feedback_list)
                elif algorithm == "Weighted Average":
                    difficulty_index = calculate_difficulty_index_weighted(performance_list, feedback_list)
                elif algorithm == "Harmonic Mean":
                    difficulty_index = calculate_difficulty_index_harmonic(performance_list, feedback_list)
                
                course_data.append({
                    "Course": course,
                    "Student Performance": performance_list,
                    "Feedback": feedback_list,
                    "Difficulty Index": difficulty_index
                })

            course_df = pd.DataFrame(course_data)
            course_df.sort_values(by='Difficulty Index', ascending=False, inplace=True)
            
            # Display the difficulty index table
            st.header("Course Difficulty Index")
            st.dataframe(course_df.style.format({'Difficulty Index': "{:.2f}"}))

            # Create a new table to display the difficulty index
            st.header("New Difficulty Index Table")
            st.table(course_df[['Course', 'Difficulty Index']].style.format({'Difficulty Index': "{:.2f}"}))

            # Visualization
            st.header("Course Difficulty Index Visualization")
            visualize_data(course_df)

            # Comparison Tool
            st.header("Compare Courses")
            course_selection = st.multiselect("Select courses to compare:", course_df['Course'])
            if course_selection:
                comparison_data = course_df[course_df['Course'].isin(course_selection)]
                st.dataframe(comparison_data.style.format({'Difficulty Index': "{:.2f}"}))
                visualize_data(comparison_data)

            # Additional Metrics
            st.header("Additional Metrics")
            avg_grade = course_df["Student Performance"].apply(lambda x: sum(x) / len(x)).mean()
            st.metric(label="Average Grade", value=avg_grade)

            # Interest-based Course Suggestion
            st.header("Personalized Course Suggestions")
            st.write("Please answer the following questions to help us suggest the best courses for you.")

            col1, col2 = st.columns(2)
            with col1:
                q1 = st.radio("Do you prefer theoretical or practical courses?", ("Theoretical", "Practical"))
                st.image("images.jpeg", caption="Theoretical vs Practical", use_column_width=True)
                q2 = st.radio("Do you enjoy programming?", ("Yes", "No"))
                st.image("images.jpeg", caption="Programming", use_column_width=True)
                q3 = st.radio("Do you like working with hardware?", ("Yes", "No"))
                st.image("images.jpeg", caption="Working with Hardware", use_column_width=True)
                q4 = st.radio("Do you prefer individual or group projects?", ("Individual", "Group"))
                st.image("images.jpeg", caption="Individual vs Group Projects", use_column_width=True)
                q5 = st.radio("Do you enjoy problem-solving?", ("Yes", "No"))
                st.image("images.jpeg", caption="Problem Solving", use_column_width=True)
            with col2:
                q6 = st.radio("Are you interested in AI and Machine Learning?", ("Yes", "No"))
                st.image("images.jpeg", caption="AI and Machine Learning", use_column_width=True)
                q7 = st.radio("Do you prefer working on theoretical frameworks?", ("Yes", "No"))
                st.image("images.jpeg", caption="Theoretical Frameworks", use_column_width=True)
                q8 = st.radio("Are you interested in developing software applications?", ("Yes", "No"))
                st.image("images.jpeg", caption="Software Development", use_column_width=True)
                q9 = st.radio("Do you prefer coursework with heavy lab work?", ("Yes", "No"))
                st.image("images.jpeg", caption="Lab Work", use_column_width=True)
                q10 = st.radio("Are you interested in data analysis and statistics?", ("Yes", "No"))
                st.image("images.jpeg", caption="Data Analysis and Statistics", use_column_width=True)

            if st.button("Get Course Suggestions"):
                suggestions = []
                if semester == 1:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics I")
                    else:
                        suggestions.append("Engineering Physics")
                    if q3 == "Yes":
                        suggestions.append("Basic Electrical Engineering")
                    if q5 == "Yes":
                        suggestions.append("Engineering Chemistry")
                elif semester == 2:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics II")
                    else:
                        suggestions.append("Engineering Graphics")
                    if q2 == "Yes":
                        suggestions.append("Computer Programming")
                    if q3 == "Yes":
                        suggestions.append("Basic Electronics")
                elif semester == 3:
                    if q1 == "Theoretical":
                        suggestions.append("Engineering Mathematics III")
                    else:
                        suggestions.append("Analog Electronics")
                    if q2 == "Yes":
                        suggestions.append("Data Structures")
                    if q5 == "Yes":
                        suggestions.append("Digital Logic Design")
                elif semester == 4:
                    if q1 == "Theoretical":
                        suggestions.append("Operating Systems")
                    else:
                        suggestions.append("Microprocessors")
                    if q2 == "Yes":
                        suggestions.append("Software Engineering")
                    if q5 == "Yes":
                        suggestions.append("Computer Organization")
                elif semester == 5:
                    if q1 == "Theoretical":
                        suggestions.append("Theory of Computation")
                    else:
                        suggestions.append("Database Management Systems")
                    if q2 == "Yes":
                        suggestions.append("Design and Analysis of Algorithms")
                    if q5 == "Yes":
                        suggestions.append("Computer Networks")
                elif semester == 6:
                    if q1 == "Theoretical":
                        suggestions.append("Artificial Intelligence")
                    else:
                        suggestions.append("Embedded Systems")
                    if q3 == "Yes":
                        suggestions.append("Computer Graphics")
                    if q5 == "Yes":
                        suggestions.append("Compiler Design")
                elif semester == 7:
                    if q1 == "Theoretical":
                        suggestions.append("Machine Learning")
                    else:
                        suggestions.append("Big Data Analytics")
                    if q3 == "Yes":
                        suggestions.append("Cyber Security")
                    if q5 == "Yes":
                        suggestions.append("Cloud Computing")
                elif semester == 8:
                    if q4 == "Group":
                        suggestions.append("Project Work")
                    else:
                        suggestions.append("Internship")
                    if q5 == "Yes":
                        suggestions.append("Elective I")
                    if q2 == "Yes":
                        suggestions.append("Elective II")
                
                st.write("Based on your interests, we suggest the following courses:")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
                
                # Convert suggestions to image
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.axis('off')
                table = ax.table(
                    cellText=[[suggestion] for suggestion in suggestions],
                    colLabels=["Suggested Courses"],
                    cellLoc='center',
                    loc='center'
                )
                table.auto_set_font_size(False)
                table.set_fontsize(14)
                table.auto_set_column_width([0])
                
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image = Image.open(buf)
                
                st.image(image, caption="Course Suggestions", use_column_width=True)

                # Download button
                buf.seek(0)
                st.download_button(
                    label="Download Course Suggestions as Image",
                    data=buf,
                    file_name='course_suggestions.png',
                    mime='image/png'
                )

        else:
            st.warning("The uploaded CSV file must contain 'Course', 'Performance', and 'Feedback' columns.")
    else:
        st.warning("Please upload a CSV file to proceed.")


def main():
    create_user_database()

    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        if st.session_state.page == "main":
            main_page()
        else:
            st.error("Invalid page.")
    else:
        if st.session_state.page == "login":
            login_page()
        else:
            register_page()

if __name__ == "__main__":
    main()
