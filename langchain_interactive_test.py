from langchain_analyzer import LangChainAnalyzer
import os
from dotenv import load_dotenv

def print_analysis(result):
    """Helper function to print analysis in a formatted way"""
    print(f"\n{'='*50}")
    print("Analysis:")
    print(result["analysis"])
    print(f"{'='*50}\n")

def interactive_test():
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    # Initialize the analyzer
    analyzer = LangChainAnalyzer()
    initial_summary = ""
    collected_info = {}
    
    print("Welcome to the Enhanced LangChain Response Analyzer!")
    print("Enter your initial summary and I'll ask follow-up questions one by one.")
    print("Type 'quit' to exit or 'reset' to start a new conversation.\n")
    
    while True:
        # Get initial user input
        user_input = input("\nEnter your summary (or 'quit'/'reset'): ").strip()
        
        # Check for special commands
        if user_input.lower() == 'quit':
            print("\nThank you for testing! Goodbye!")
            break
        elif user_input.lower() == 'reset':
            analyzer.reset_conversation()
            initial_summary = ""
            collected_info = {}
            print("\nConversation reset. Starting fresh!")
            continue
        
        # Skip empty responses
        if not user_input:
            print("Please enter a response or use 'quit' to exit.")
            continue
        
        # Store initial summary
        initial_summary = user_input
        
        # Analyze the initial response
        result = analyzer.analyze_response(f"Initial summary: {user_input}")
        
        # Print the analysis
        print_analysis(result)
        
        # Ask three follow-up questions one by one
        for i in range(1, 4):
            # Get the follow-up question from the analysis
            question = result["follow_up_questions"].strip()
            
            print(f"\nFollow-up Question {i}:")
            print(question)
            
            # Get user's answer to the follow-up question
            answer = input("\nYour answer: ").strip()
            
            # Skip empty answers
            if not answer:
                print("Skipping empty answer...")
                continue
                
            # Store the Q&A
            collected_info[question] = answer
            
            # Generate next question based on all previous information
            context = f"""
Initial summary: {initial_summary}
Collected information:
{'\n'.join([f'Q: {q}\nA: {a}' for q, a in collected_info.items()])}
"""
            # Analyze and get next question
            result = analyzer.analyze_response(context)
            
            # After the last question, generate an updated summary
            if i == 3:
                print("\nGenerating final updated summary...")
                final_context = f"""
Initial summary: {initial_summary}
Collected information:
{'\n'.join([f'Q: {q}\nA: {a}' for q, a in collected_info.items()])}
"""
                final_result = analyzer.analyze_response(final_context, is_final_summary=True)
                print("\nUPDATED SUMMARY:")
                print("="*50)
                print(final_result["analysis"])
                print("="*50)
        
        # Show conversation history length
        history = analyzer.get_conversation_history()
        print(f"\nMessages in conversation: {len(history)}")

if __name__ == "__main__":
    interactive_test() 