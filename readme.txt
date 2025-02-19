#AI Agent for GitHub Issue Tracker with LangChain Integration

#Overview
This project leverages an AI agent powered by Retrieval-Augmented Generation (RAG). It fetches GitHub issues from a specific repository, processes them into structured documents, and stores them in a vector database for efficient searching. Using the LangChain framework, the AI agent interacts with the stored issues through a query-based interface to generate contextually accurate responses. Additionally, it includes a note-taking tool to save notes locally.

#Features
-Fetch GitHub Issues: Retrieve issues from a specific GitHub repository using the GitHub API.
-Process Issues: Convert fetched GitHub issues into structured documents using LangChain's Document class.
-Store in AstraDB: Store the processed issues in a vector database (AstraDB) for fast retrieval.
-Search Issues: Perform similarity searches on stored issues using LangChain's retriever tool.
-Interactive AI Agent (RAG): The AI agent uses Retrieval-Augmented Generation (RAG) to fetch relevant information from the database and generate responses to user queries based on this information.
-Note-Taking Tool: Save notes locally in a text file using the built-in note tool.

#Setup
-Install Dependencies:
pip install requests dotenv langchain langchain_openai langchain_astradb github

-Environment Variables:
GITHUB_TOKEN: GitHub Personal Access Token to authenticate API requests.
ASTRA_DB_API_ENDPOINT: Endpoint for AstraDB API.
ASTRA_DB_APPLICATION_TOKEN: Token for authenticating AstraDB access.
ASTRA_DB_KEYSPACE: Keyspace for the AstraDB database.

#Run the Script:
The script will ask whether to update the GitHub issues in the database. If yes, it will fetch issues from the specified repository (techwithtim/Flask-Web-App-Tutorial) and store them in the vector store.
You can interact with the AI agent by asking questions related to the GitHub issues.

#Usage
-Updating Issues: The user can update the stored issues in the vector database by confirming when prompted.
-Querying Issues (RAG): After the issues are loaded into the database, users can ask questions about the issues. The AI agent will retrieve relevant information -from the database and generate contextually accurate responses based on this information.
-Saving Notes: Any notes entered through the note_tool function are saved to a notes.txt file.

#Example
Do you want to update the issues? (y/N): y
Ask a question about github issues (q to quit): What is the status of the issue titled 'error in flask'?

#Files
notes.txt: Stores any notes created via the note_tool.
GitHub Issues: Stored in AstraDB for fast querying and retrieval.


python3 -m venv github

source github/bin/activate

pip install python-dotenv requests langchain langchain-astradb langchain-openai langchainhub

RAG APPLICATION WHICH HAS ACCESS TO DATABASE CALLED VECTOR DATABASE FROM WHICH IT CAN QUERY
