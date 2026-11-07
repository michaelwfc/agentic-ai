# Set up LangSmith Studio

Note: LangSmith Studio was formerly LangGraph Studio

LangSmith Studio is a custom IDE for viewing and testing agents.
Studio can be run locally and opened in your browser on Mac, Windows, and Linux.
See documentation here.
Graphs for LangSmith Studio are in the module-x/studio/ folders.

# Stadio Quickstart

## Create a LangGraph app

Set up a LangGraph app locally for testing and development

1. Create a LangGraph app key :
2. install the LangGraph CLI
  That older version of the CLI didn't depend on the heavy API package at all.
  ```bash
  pip uninstall langgraph-api langgraph-cli -y
  
  pip install "langgraph-cli[inmem]==0.1.71"
  ```
1. Create a LangGraph app
   Create a new app from the new-langgraph-project-python template.
   `langgraph new test_studio --template new-langgraph-project-python`


4. Install dependencies
  ```
  cd path/to/your/app
  pip install -e .
  ```

5. Create a .env file
You will find a .env.example in the root of your new LangGraph app. Create a .env file in the root of your new LangGraph app and copy the contents of the .env.example file into it, filling in the necessary API keys:
`LANGSMITH_API_KEY=lsv2_pt***`

6. Launch Agent Server
To start the local development server, run the following command in your terminal in the /studio directory each module:
```bash
export DATABASE_URI=sqlite:///./demo.db


langgraph dev
```
You should see the following output:

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
Open your browser and navigate to the Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

To use Studio, you will need to create a .env file with the relevant API keys
Run this from the command line to create these files for module 1 to 6, as an example: