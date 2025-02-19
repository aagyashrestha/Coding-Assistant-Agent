from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Import the OS module to interact with environment variables

from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Import OpenAI language model and embeddings
from langchain_astradb import AstraDBVectorStore  # Import AstraDB vector store for storing embeddings
from langchain.agents import create_tool_calling_agent  # Import function to create AI agents
from langchain.agents import AgentExecutor  # Import executor for running the agent
from langchain.tools.retriever import create_retriever_tool  # Import tool for retrieving information
from langchain import hub  # Import hub to get pre-defined prompts
from github import fetch_github_issues  # Import function to fetch GitHub issues
from note import note_tool  # Import a note-taking tool

load_dotenv()  # Load environment variables from the .env file

# Function to connect to AstraDB vector store
def connect_to_vstore():
    embeddings = OpenAIEmbeddings()  # Initialize OpenAI embeddings
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")  # Get AstraDB API endpoint from environment variables
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")  # Get AstraDB application token
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")  # Get AstraDB keyspace

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace  # Use the provided keyspace if available
    else:
        ASTRA_DB_KEYSPACE = None  # Otherwise, set keyspace to None

    # Create a connection to AstraDB vector store
    vstore = AstraDBVectorStore(
        embedding=embeddings,  # Use OpenAI embeddings
        collection_name="github",  # Name of the collection to store GitHub issues
        api_endpoint=ASTRA_DB_API_ENDPOINT,  # API endpoint for AstraDB
        token=ASTRA_DB_APPLICATION_TOKEN,  # Authentication token for AstraDB
        namespace=ASTRA_DB_KEYSPACE,  # Keyspace (namespace) for the database
    )
    return vstore  # Return the connected vector store

vstore = connect_to_vstore()  # Connect to the vector store

# Ask the user if they want to update the issues stored in the database
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    owner = "techwithtim"  # Define GitHub repository owner
    repo = "Flask-Web-App-Tutorial"  # Define GitHub repository name
    issues = fetch_github_issues(owner, repo)  # Fetch issues from GitHub

    try:
        vstore.delete_collection()  # Delete existing collection if it exists
    except:
        pass  # Ignore errors if the collection does not exist

    vstore = connect_to_vstore()  # Reconnect to the vector store
    vstore.add_documents(issues)  # Add fetched GitHub issues to the vector store

    # Uncomment the lines below to perform a similarity search on stored issues
    # results = vstore.similarity_search("flash messages", k=3)
    # for res in results:
    #     print(f"* {res.page_content} {res.metadata}")

retriever = vstore.as_retriever(search_kwargs={"k": 3})  # Create a retriever to search stored issues
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",  # Define tool name
    "Search for information about github issues. For any questions about github issues, you must use this tool!",  # Define tool description
)

prompt = hub.pull("hwchase17/openai-functions-agent")  # Load predefined prompt from LangChain hub
llm = ChatOpenAI()  # Initialize OpenAI language model

tools = [retriever_tool, note_tool]  # Define list of tools to be used by the agent
agent = create_tool_calling_agent(llm, tools, prompt)  # Create an AI agent with the tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # Create an agent executor to run the agent

# Run an interactive loop to ask questions about GitHub issues
while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})  # Get the agent's response
    print(result["output"])  # Print the response from the agent
