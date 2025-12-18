# LangGraph AI Assistant

A local AI assistant built with **LangGraph**, **LangChain**, **Ollama**, and **Streamlit**.  
It takes a user query, performs step-by-step reasoning using a local LLM (via Ollama), and presents both the reasoning steps and a clear final answer.

## Features

- Multi-step reasoning workflow using LangGraph (Input → Reasoning → Final Output nodes)
- Runs completely locally with Ollama (no API keys or cloud dependency)
- Clean, dark-themed Streamlit UI
- Real-time processing with "Cancel" support during long generations
- Displays intermediate reasoning and final structured answer separately
- Input validation with user-friendly error message
- Responsive button that changes to "Cancel" while processing

## Tech Stack

- **LangGraph** – for building the stateful reasoning graph
- **LangChain + langchain_ollama** – integration with local Ollama models
- **Ollama** – runs the LLM locally (default: phi3)
- **Streamlit** – simple and beautiful frontend
- **Python dotenv** – for environment configuration

## Prerequisites

1. Python 3.10 or higher
2. Ollama installed and running[](https://ollama.com)
3. Pull a model (recommended: `phi3` or any other compatible model)

```bash
ollama pull phi3
Project Structure
text.
├── app.py              # Streamlit frontend + threading logic
├── graph.py            # LangGraph definition
├── input_node.py       # Validates and passes input
├── reasoning_node.py   # Generates step-by-step reasoning
├── output_node.py      # Formats final answer based on reasoning
├── .env                # Environment variables (optional)
└── requirements.txt    # Python dependencies
Installation & Setup

Clone the repository

Bashgit clone https://github.com/yourusername/langgraph-ai-assistant.git
cd langgraph-ai-assistant

Create a virtual environment (recommended)

Bashpython -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

Install dependencies

Bashpip install -r requirements.txt

(Optional) Create a .env file to set your preferred model

envMODEL_NAME=phi3
# You can change to any model pulled in Ollama, e.g., llama3, mistral, etc.
Run the App
Make sure Ollama is running:
Bashollama serve
Then start the Streamlit app:
Bashstreamlit run app.py
The app will open in your browser (usually at http://localhost:8501).
Usage

Type or paste your problem/question into the text area.
Click Solve.
Wait while the model processes (button changes to Cancel if you need to stop).
View the Reasoning Steps and Final Answer once complete.
The input clears automatically — ready for your next query!

Example Queries

"Explain how photosynthesis works step by step."
"What is the capital of Japan and some interesting facts?"
"Solve: 2x + 5 = 15"
"Write a short poem about the ocean."

Customization

Change the default model by editing the MODEL_NAME in .env or directly in the node files.
Adjust temperature or other LLM parameters in reasoning_node.py and output_node.py.

Troubleshooting

If you get connection errors → make sure Ollama is running (ollama serve).
Model not found → pull it first with ollama pull <model_name>.
Slow response → try a smaller/faster model like phi3:mini or gemma2:2b.

Credits
Made by Priyal Lunagariya
