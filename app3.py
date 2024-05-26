import streamlit as st
import os
import git
from dotenv import load_dotenv
from openai import OpenAI
import GraphRetrieval
from GraphRetrieval import GraphRAG

load_dotenv()
os.environ["OPENAI_API_KEY"] =""
# os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

def merging_files(repo_link):
    project_name = repo_link.split('/')[-1]  # Getting the project name from the URL
    repo_link = repo_link + '.git'

    # Clone the repository
    target_directory = f'tmp/{project_name}'
    if not os.path.exists(target_directory):
        repo = git.Repo.clone_from(repo_link, target_directory, branch='main')
    else:
        print(f"The directory '{target_directory}' already exists. Skipping cloning.")
    
    # Open input.txt file for writing
    with open('input.txt', 'w', encoding='utf-8') as input_file:
        for blob in repo.tree().blobs:  # Traverse through the files in the repository
            # Read the content of each file
            file_content = blob.data_stream.read().decode('utf-8')
            # Write filename and its content into input.txt
            input_file.write("Start of next file \n")
            input_file.write(f"File: {blob.path}\n\n")
            input_file.write(file_content)
            input_file.write("\n\n")

    print('All files merged into input.txt')

def main():
    st.title("GitHub Repository File Merger and Query App")

    # Input for GitHub URL
    github_url = st.text_input("Enter GitHub Repository URL", "https://github.com/PsyCharan17/SampleRepo")

    if st.button("Merge Files"):
        merging_files(github_url)
        st.success("Files merged into input.txt")

    grag = GraphRAG()

    if os.path.exists("input.txt"):
        grag.create_graph_from_file("input.txt")

    query = st.text_input("Enter your query", "what happens if notes data is present in notesmaker.py file")

    if st.button("Query LLM"):
        if os.path.exists("input.txt"):
            result = grag.queryLLM(f"{query}")
            st.write(result)
        else:
            st.warning("Please merge the files first.")

if __name__ == "__main__":
    main()
