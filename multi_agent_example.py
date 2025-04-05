import os
from dotenv import load_dotenv
from langchain_analyzer import MultiAgentAnalyzer

# Load environment variables
load_dotenv()

def main():
    # Initialize the multi-agent analyzer
    multi_agent = MultiAgentAnalyzer(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Example project description
    project_description = """
    I'm building a new mobile app for fitness tracking. The app will allow users to log their workouts,
    track their progress, and connect with friends. I'm planning to use React Native for the frontend
    and Firebase for the backend. I have a budget of $50,000 and want to launch in 6 months.
    """
    
    print("=== Project Description ===")
    print(project_description)
    print("\n=== Getting questions from different agents ===")
    
    # Get questions from each agent
    for agent_name in multi_agent.agents.keys():
        print(f"\n--- {agent_name.replace('_', ' ').title()} ---")
        result = multi_agent.analyze_with_agent(agent_name, project_description)
        print(f"Analysis: {result['analysis']}")
        print(f"Question: {result['follow_up_questions']}")
    
    # Example user response
    user_response = """
    The app will focus on strength training and cardio. I'm planning to include features like workout plans,
    progress tracking with charts, and social sharing. I have experience with React but not with React Native.
    I'm considering using a third-party API for workout data.
    """
    
    print("\n=== User Response ===")
    print(user_response)
    print("\n=== Getting follow-up questions from different agents ===")
    
    # Get follow-up questions from each agent
    for agent_name in multi_agent.agents.keys():
        print(f"\n--- {agent_name.replace('_', ' ').title()} ---")
        result = multi_agent.analyze_with_agent(agent_name, user_response)
        print(f"Analysis: {result['analysis']}")
        print(f"Question: {result['follow_up_questions']}")
    
    # Get a final summary from each agent
    print("\n=== Final Summaries from Each Agent ===")
    for agent_name in multi_agent.agents.keys():
        print(f"\n--- {agent_name.replace('_', ' ').title()} Summary ---")
        result = multi_agent.analyze_with_agent(agent_name, user_response, is_final_summary=True)
        print(result['analysis'])
    
    # Example of using all agents at once
    print("\n=== Using All Agents at Once ===")
    all_results = multi_agent.analyze_with_all_agents(user_response)
    for agent_name, result in all_results.items():
        print(f"\n--- {agent_name.replace('_', ' ').title()} ---")
        print(f"Question: {result['follow_up_questions']}")

if __name__ == "__main__":
    main() 