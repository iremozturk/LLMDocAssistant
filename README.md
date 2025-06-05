# LLMDocAssistant

Multi-Agent LangChain Analyzer

This project implements a multi-agent system using LangChain that allows multiple specialized AI agents to analyze user input, generate follow-up questions, and create summaries. All agents share the same conversation memory, allowing them to build upon each other's insights.

## Features

- **Multiple Specialized Agents**: Create agents with different roles (project analyst, technical expert, business consultant, etc.)
- **Shared Memory**: All agents share the same conversation history, allowing them to build upon each other's insights
- **Flexible Analysis**: Each agent can analyze user input and generate follow-up questions based on their expertise
- **Comprehensive Summaries**: Generate summaries from the perspective of each agent
- **Customizable**: Easily create new agents with different roles and prompts

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install langchain langchain-openai python-dotenv
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Basic Multi-Agent System

The `MultiAgentAnalyzer` class provides a simple way to use multiple agents with shared memory:

```python
from langchain_analyzer import MultiAgentAnalyzer

# Initialize the multi-agent analyzer
multi_agent = MultiAgentAnalyzer(model_name="gpt-3.5-turbo", temperature=0.7)

# Analyze with a specific agent
result = multi_agent.analyze_with_agent("project_analyst", "Your project description here")
print(result["follow_up_questions"])

# Analyze with all agents at once
all_results = multi_agent.analyze_with_all_agents("Your project description here")
for agent_name, result in all_results.items():
    print(f"{agent_name}: {result['follow_up_questions']}")
```

### Custom Agents

You can create custom agents with different roles:

```python
from langchain_analyzer import LangChainAnalyzer
from langchain.memory import ConversationBufferMemory

# Create a shared memory
shared_memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

# Create custom agents with different roles
ui_expert = LangChainAnalyzer(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    memory=shared_memory,
    agent_role="UI/UX expert"
)

backend_expert = LangChainAnalyzer(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    memory=shared_memory,
    agent_role="backend architect"
)

# Use the agents
ui_result = ui_expert.analyze_response("Your project description here")
backend_result = backend_expert.analyze_response("Your project description here")
```

## Examples

The repository includes two example scripts:

1. `multi_agent_example.py`: Demonstrates how to use the `MultiAgentAnalyzer` class
2. `custom_agents_example.py`: Shows how to create custom agents with different roles

Run the examples with:

```
python multi_agent_example.py
python custom_agents_example.py
```

## Extending the System

You can extend the system by:

1. Creating new agent roles with specialized prompts
2. Implementing different memory types (e.g., `ConversationBufferWindowMemory` for a sliding window)
3. Adding new analysis methods to the `LangChainAnalyzer` class
4. Integrating with other LangChain components like agents, tools, and chains

## License

MIT
