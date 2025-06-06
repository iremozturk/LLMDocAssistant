from response_analyzer import ResponseAnalyzer
import json

def print_result(result, title):
    """Helper function to print results in a formatted way"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print("\nAnalysis:")
    print(result["analysis"])
    print("\nFollow-up Questions:")
    print(result["follow_up_questions"])
    print(f"\n{'='*50}\n")

def test_analyzer():
    # Initialize the analyzer
    analyzer = ResponseAnalyzer()
    
    # Test Case 1: Short, focused response
    print("\nTest Case 1: Short Response")
    short_response = """
    Our project is a machine learning system that helps companies predict customer churn.
    We use Python for the backend and TensorFlow for the models. The frontend is built
    with React and TypeScript.
    """
    result = analyzer.analyze_response(short_response)
    print_result(result, "Short Response Analysis")
    
    # Test Case 2: Long response that needs summarization
    print("\nTest Case 2: Long Response")
    long_response = """
    Our project is a comprehensive machine learning system designed to help companies predict and prevent customer churn.
    The system is built using a modern tech stack that includes Python for the backend services, TensorFlow for the machine learning models,
    and React with TypeScript for the frontend interface. We've implemented several key features including real-time data processing,
    automated model retraining, and a user-friendly dashboard for monitoring key metrics.
    
    The backend architecture consists of multiple microservices that handle different aspects of the system:
    - Data ingestion service that processes customer data in real-time
    - Model training service that retrains the churn prediction model weekly
    - API service that handles all client requests
    - Monitoring service that tracks system health and performance
    
    The frontend dashboard provides various views and features:
    - Customer segmentation analysis
    - Churn risk visualization
    - Historical trend analysis
    - Custom report generation
    
    We're currently working on improving the model accuracy and adding more features to the dashboard.
    The team is also considering implementing A/B testing capabilities and expanding the API endpoints.
    """
    result = analyzer.analyze_response(long_response)
    print_result(result, "Long Response Analysis")
    
    # Test Case 3: Follow-up response to previous analysis
    print("\nTest Case 3: Follow-up Response")
    follow_up_response = """
    The current model accuracy is around 85%. We're planning to add more features
    to the dashboard next month, including customer segmentation and trend analysis.
    The team is also working on improving the data preprocessing pipeline.
    """
    result = analyzer.analyze_response(follow_up_response)
    print_result(result, "Follow-up Response Analysis")
    
    # Test Case 4: Reset conversation and test new topic
    print("\nTest Case 4: New Topic After Reset")
    analyzer.reset_conversation()
    new_topic_response = """
    We're developing a new feature for automated code review. The system uses
    static analysis and machine learning to identify potential issues in code.
    It supports multiple programming languages and integrates with popular CI/CD platforms.
    """
    result = analyzer.analyze_response(new_topic_response)
    print_result(result, "New Topic Analysis")
    
    # Test Case 5: Save conversation history
    print("\nTest Case 5: Conversation History")
    history = analyzer.get_conversation_history()
    print("Number of messages in history:", len(history))
    print("\nLast message in history:")
    print(history[-1]["content"])

if __name__ == "__main__":
    test_analyzer() 