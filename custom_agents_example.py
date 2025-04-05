import os
from dotenv import load_dotenv
from langchain_analyzer import LangChainAnalyzer, MultiAgentAnalyzer
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

def create_custom_multi_agent():
    """Create a custom multi-agent system with specialized roles"""
    
    # Create a shared memory for all agents
    shared_memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )
    
    # Define custom agent roles and their specialized prompts
    custom_agents = {
        "ui_ux_expert": LangChainAnalyzer(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            memory=shared_memory,
            agent_role="UI/UX expert"
        ),
        "backend_architect": LangChainAnalyzer(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            memory=shared_memory,
            agent_role="backend architect"
        ),
        "security_specialist": LangChainAnalyzer(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            memory=shared_memory,
            agent_role="security specialist"
        ),
        "data_scientist": LangChainAnalyzer(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            memory=shared_memory,
            agent_role="data scientist"
        )
    }
    
    return custom_agents, shared_memory

def main():
    # Create custom agents with shared memory
    custom_agents, shared_memory = create_custom_multi_agent()
    
    # Example project description
    project_description = """
    I'm developing a machine learning platform that will help businesses analyze customer data.
    The platform will use Python for the backend, React for the frontend, and will integrate
    with various ML libraries. It needs to handle large datasets and provide real-time insights.
    """
    
    print("=== Project Description ===")
    print(project_description)
    print("\n=== Getting questions from specialized agents ===")
    
    # Get questions from each specialized agent
    for agent_name, agent in custom_agents.items():
        print(f"\n--- {agent_name.replace('_', ' ').title()} ---")
        result = agent.analyze_response(project_description)
        print(f"Analysis: {result['analysis']}")
        print(f"Question: {result['follow_up_questions']}")
    
    # Example user response
    user_response = """
    The platform will focus on customer segmentation and predictive analytics. We'll use TensorFlow
    for the ML models and store data in a PostgreSQL database. We need to ensure GDPR compliance
    and implement proper data anonymization. The UI should be intuitive with interactive dashboards.
    """
    
    print("\n=== User Response ===")
    print(user_response)
    print("\n=== Getting follow-up questions from specialized agents ===")
    
    # Get follow-up questions from each specialized agent
    for agent_name, agent in custom_agents.items():
        print(f"\n--- {agent_name.replace('_', ' ').title()} ---")
        result = agent.analyze_response(user_response)
        print(f"Analysis: {result['analysis']}")
        print(f"Question: {result['follow_up_questions']}")
    
    # Get a final summary from each agent
    print("\n=== Final Summaries from Each Agent ===")
    for agent_name, agent in custom_agents.items():
        print(f"\n--- {agent_name.replace('_', ' ').title()} Summary ---")
        result = agent.analyze_response(user_response, is_final_summary=True)
        print(result['analysis'])
    
    # Example of creating a new agent that inherits the shared memory
    print("\n=== Adding a New Agent Mid-Conversation ===")
    new_agent = LangChainAnalyzer(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        memory=shared_memory,  # Use the same shared memory
        agent_role="project manager"
    )
    
    print("\n--- Project Manager ---")
    result = new_agent.analyze_response(user_response)
    print(f"Analysis: {result['analysis']}")
    print(f"Question: {result['follow_up_questions']}")

if __name__ == "__main__":
    main() 