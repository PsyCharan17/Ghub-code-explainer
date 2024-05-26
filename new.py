from openai import OpenAI
import os
import git
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

import GraphRetrieval
from GraphRetrieval import GraphRAG

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

grag = GraphRAG()
github_url = "https://github.com/PsyCharan17/SampleRepo"
merging_files(github_url)
grag.create_graph_from_file("input.txt")

query="what happens if notes data is present in notesmaker.py file"

print(grag.queryLLM(f"{query}"))
