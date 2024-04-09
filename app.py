import os
import streamlit as st
from lyzr import ChatBot
from utils.llm_calling import llm_calling
import shutil
from PIL import Image

st.set_page_config(
    page_title="Lyzr Game Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Answer Scoring Agent")
st.markdown("### Welcome to the Lyzr Answer Scoring Agent!")
st.markdown("Upload Text book or use a sample Chemistry book")

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


data_directory = "data"
os.makedirs(data_directory, exist_ok=True)
remove_existing_files(data_directory)

uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded PDF file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    # Display the path of the stored file
    st.success(f"File successfully saved")


def get_all_files(data_directory):
    # List to store all file paths
    file_paths = []

    # Walk through the directory tree
    for root, dirs, files in os.walk(data_directory):
        for file in files:
            # Join the root path with the file name to get the absolute path
            file_path = os.path.join(root, file)
            # Append the file path to the list
            file_paths.append(file_path)

    return file_paths


def bookqabot(file_path):
    qa_bot = ChatBot.pdf_chat(
        input_files=[file_path],
    )

    response = qa_bot.chat(question)
    return response.response


def generate_grade(question, answer, ref_answer):
    res = llm_calling(user_prompt=f"For a 2 marks quetsion on {question} what should be the gradding criteria",
                      system_prompt="You are a grading criteria generator for questions",
                      llm_model="gpt-4-turbo-preview")
    prompt1 = f"""
                Give Grade for Answer for Question Based On Criterias and Reference answer.
                Question: {question}
                Answer: {answer}
                Criterias: {res}
                Reference Answer:{ref_answer}
                [!important] only give grades nothing apart from that


                Grades: 2/2
                """

    grade = llm_calling(user_prompt=prompt1, system_prompt="You are a giving grade to answers.",
                        llm_model="gpt-4-turbo-preview")
    return grade


paths = get_all_files(data_directory)
question = st.text_input("Enter your question: ")
answer = st.text_area("Enter Your Answer: ")
file_path = "lech201.pdf"

if paths:
    for path in paths:
        qa = bookqabot(path)
        if st.button("Grade"):
            grade = generate_grade(question, answer, qa)
            st.markdown(grade)
else:
    qa = bookqabot(file_path)
    if st.button("Grade"):
        grade = generate_grade(question, answer, qa)
        st.markdown(grade)
