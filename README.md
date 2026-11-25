# 🩺 Diabetes Risk Assessment Assistant

An AI-powered assistant that combines Machine Learning, Retrieval-Augmented Generation (RAG), Graph Databases, and Agentic AI to provide educational diabetes risk assessments and relevant health information.

The project uses **LangGraph** to orchestrate an intelligent agent capable of selecting and interacting with three specialized tools: a Machine Learning classification model, a ChromaDB-based knowledge retrieval system, and a Neo4j graph database.

> **Disclaimer:** This project is intended for educational and informational purposes only. It does not provide medical diagnoses, treatment recommendations, or replace professional medical advice.

---

## 📌 Project Overview

The Diabetes Risk Assessment Assistant aims to provide users with an interactive way to explore diabetes-related risk factors and educational information.

Instead of relying on a single AI model, the system integrates three specialized tools:

1. **Machine Learning:** Estimates diabetes-related risk based on user-provided medical measurements.
2. **ChromaDB (RAG):** Retrieves relevant information from a collection of diabetes-related educational documents.
3. **Neo4j:** Explores relationships between diabetes, symptoms, risk factors, medical conditions, and screening tests.

An LLM-powered agent coordinates these tools through LangGraph and generates a response based on the available results.

---

## 🎯 Project Objectives

- Develop an ML classification model for diabetes-related risk assessment.
- Build a knowledge retrieval system using ChromaDB.
- Represent diabetes-related medical concepts and their relationships using Neo4j.
- Integrate the three tools into an agentic workflow using LangGraph.
- Enable the agent to dynamically select the appropriate tools depending on the user's query.
- Generate clear, informative responses grounded in retrieved information and actual tool outputs.

---

## 🏗️ System Architecture

The system follows an agent-based architecture:

```text
                User
                  |
                  v
             LangGraph Agent
                  |
                  v
              LLM Node
                  |
          Tool Selection
                  |
       +----------+----------+
       |          |          |
       v          v          v
   ML Tool    ChromaDB     Neo4j
       |        Tool        Tool
       |          |          |
       v          v          v
   Risk       Retrieved   Graph
 Prediction   Documents   Results
       |          |          |
       +----------+----------+
                  |
                  v
             LLM Node
                  |
                  v
            Final Response
                  |
                  v
                 User
```

The agent can decide whether to call one tool, multiple tools, ask the user for missing information, or generate a final response.

The workflow has a maximum of five iterations to prevent unnecessary tool execution.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangGraph | Agent workflow orchestration |
| LangChain | LLM and tool integration |
| OpenAI | Large Language Model |
| Scikit-learn | Machine Learning |
| Pandas & NumPy | Data preprocessing and analysis |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| Neo4j | Graph database |
| Streamlit | User interface |
| Joblib | Saving and loading ML models |
| PyPDF | PDF document processing |

---

## 🔧 Core Components

### 1. Machine Learning Tool

The ML component is responsible for estimating diabetes-related risk based on relevant input measurements.

Main tasks:
- Dataset collection and exploration.
- Data preprocessing and feature engineering.
- Model training and evaluation.
- Model selection and optimization.
- Saving the trained model.
- Exposing a prediction function for the agent.

**Output:** A structured prediction result that the agent can interpret.

### 2. ChromaDB — Knowledge Retrieval Tool

The retrieval component provides educational information from a collection of diabetes-related documents.

Main tasks:
- Collect reliable educational documents.
- Extract and clean document content.
- Split documents into smaller chunks.
- Generate text embeddings.
- Store embeddings and metadata in ChromaDB.
- Retrieve relevant information using semantic similarity.

**Knowledge areas include:**
- Diabetes overview.
- Risk factors.
- Symptoms.
- Prevention.
- Screening tests.
- General educational information.

**Output:** Relevant document chunks and their associated metadata.

### 3. Neo4j — Graph Database Tool

The graph component represents diabetes-related concepts and their relationships.

Potential entities include:
- Diabetes.
- Symptoms.
- Risk factors.
- Medical conditions.
- Screening tests.
- Preventive measures.

Example relationships:

```text
Diabetes --HAS_SYMPTOM--> Increased Thirst

Obesity --INCREASES_RISK_OF--> Type 2 Diabetes

HbA1c Test --USED_FOR_SCREENING--> Diabetes
```

Main tasks:
- Define graph entities and relationships.
- Create nodes and edges.
- Populate the database.
- Write Cypher queries.
- Expose graph query functions to the agent.

**Output:** Relevant entities and relationships retrieved from Neo4j.

---

## 🤖 Agent Workflow

The LangGraph agent coordinates the three tools.

The workflow follows these steps:

1. Receive a user query.
2. Analyze the query using the LLM.
3. Determine which tool or tools are needed.
4. Execute the selected tool.
5. Receive and interpret the tool results.
6. Decide whether another tool call is necessary.
7. Generate the final response.

The agent supports dynamic tool selection and has a maximum of five iterations.

Every iteration should be logged, including:
- Iteration number.
- Selected action or tool.
- Tool input.
- Tool output.

---

## 📁 Project Structure

```text
diabetes-agent/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── eda.ipynb
│   └── model_training.ipynb
│
├── src/
│   └── diabetes_agent/
│       ├── tools/
│       │   ├── ml_tool.py
│       │   ├── vector_tool.py
│       │   └── graph_tool.py
│       │
│       ├── agent/
│       │   ├── agent.py
│       │   └── state.py
│       │
│       ├── config/
│       │   └── settings.py
│       │
│       ├── app.py
│       └── logger.py
│
├── models/
├── chroma_db/
├── neo4j/
├── logs/
├── docs/
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.11
- Git
- Neo4j Desktop or a Neo4j server
- An OpenAI API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd diabetes-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Configure the required values:

```env
OPENAI_API_KEY=your_api_key
LLM_MODEL=gpt-4o-mini

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=diabetes_knowledge

MODEL_PATH=./models/diabetes_model.joblib

MAX_ITERATIONS=5
```

Never commit your actual `.env` file or API keys to GitHub.

### 5. Run the Application

Once the components and application entry point are implemented, start the application using:

```bash
streamlit run src/diabetes_agent/app.py
```

---

## 🧪 Testing

Each component should be tested independently before integration.

```bash
pytest tests/
```

Testing will cover:

- ML model predictions.
- ChromaDB document retrieval.
- Neo4j graph queries.
- LangGraph tool selection.
- Agent iteration limits.
- Error handling.
- End-to-end agent responses.

---

## 📊 Expected Outcomes

The completed system is expected to:

- Estimate diabetes-related risk using a trained ML classifier.
- Retrieve relevant educational information from a vector database.
- Explore relationships between medical concepts through a graph database.
- Dynamically coordinate all three tools using LangGraph.
- Provide understandable responses grounded in actual tool outputs.

---

## 👥 Team

Developed as a university project by a team of six AI students.

**Course:** Introduction to Data Science

**Project:** Diabetes Risk Assessment Assistant

---

## ⚠️ Disclaimer

This system is an academic prototype designed for educational and research purposes. Its predictions should not be interpreted as medical diagnoses. Users should consult qualified healthcare professionals for medical evaluation and decisions.
