import os  # Import the OS module to interact with the operating system
import requests  # Import the requests module to send HTTP requests
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
from langchain_core.documents import Document  # Import Document from langchain_core to store structured data

# Load environment variables from a .env file
load_dotenv()

# Get the GitHub token from environment variables
github_token = os.getenv("GITHUB_TOKEN")

# Function to fetch data from a specific GitHub API endpoint
def fetch_github(owner, repo, endpoint):
    # Construct the API URL using the repository owner, repository name, and endpoint
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    
    # Define the authorization header using the GitHub token
    headers = {"Authorization": f"Bearer {github_token}"}
    
    # Send a GET request to the GitHub API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200 means success)
    if response.status_code == 200:
        data = response.json()  # Convert the response to JSON format
    else:
        print("Failed with status code:", response.status_code)  # Print an error message if the request fails
        return []  # Return an empty list if the request fails

    print(data)  # Print the fetched data (for debugging purposes)
    return data  # Return the fetched data

# Function to fetch issues from a GitHub repository
def fetch_github_issues(owner, repo):
    data = fetch_github(owner, repo, "issues")  # Call fetch_github to get the issues data
    return load_issues(data)  # Process and return structured issues

# Function to process GitHub issues and convert them into structured documents
def load_issues(issues):
    docs = []  # Initialize an empty list to store processed issues
    
    # Loop through each issue in the response data
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],  # Get the author's username
            "comments": entry["comments"],  # Get the number of comments on the issue
            "body": entry["body"],  # Get the issue description/body
            "labels": entry["labels"],  # Get the labels assigned to the issue
            "created_at": entry["created_at"],  # Get the issue creation date
        }
        
        data = entry["title"]  # Get the issue title
        
        # Append the issue description/body to the title if it exists
        if entry["body"]:
            data += entry["body"]
        
        # Create a Document object to store issue details
        doc = Document(page_content=data, metadata=metadata)
        
        # Add the processed issue document to the list
        docs.append(doc)

    return docs  # Return the list of structured issue documents
