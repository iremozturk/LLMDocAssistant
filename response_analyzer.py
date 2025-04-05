from typing import List, Dict, Optional
import os
import json
import requests
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

load_dotenv()

class ResponseAnalyzer:
    def __init__(self):
        # Initialize text splitter for handling long responses
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # API configuration
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Initialize conversation history
        self.conversation_history = []
        
        # System prompts
        self.analysis_prompt = """You are an AI assistant that analyzes user responses to extract useful information.
        Your task is to:
        1. Identify key information in the user's response
        2. Determine if any important information is missing
        3. Generate follow-up questions if needed
        
        Guidelines:
        - Be concise and focused
        - Prioritize the most important information
        - Generate at most 3 follow-up questions
        - Use bullet points for clarity
        - Focus on actionable information"""
        
        self.question_prompt = """Generate focused follow-up questions based on missing information.
        Guidelines:
        - Generate 1-3 specific questions
        - Focus on gathering actionable information
        - Avoid redundant questions
        - Keep questions clear and concise
        - Prioritize the most important missing information"""
    
    def _process_long_response(self, text: str) -> str:
        """Process long responses by splitting and summarizing if needed."""
        if len(text) > 2000:  # If text is too long
            # Split the text into chunks
            texts = self.text_splitter.split_text(text)
            
            # Convert chunks to documents
            docs = [Document(page_content=t) for t in texts]
            
            # Summarize the chunks
            summary = self._call_api([{"role": "user", "content": f"Please summarize this text: {text}"}])
            return summary
        return text
    
    def _call_api(self, messages: List[Dict[str, str]]) -> str:
        """Make API call to OpenAI."""
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error in API call: {str(e)}")
            return ""
    
    def analyze_response(self, user_response: str) -> Dict:
        """
        Analyze the user's response and extract useful information.
        Returns a dictionary containing the analysis results and any follow-up questions.
        """
        # Process long responses if needed
        processed_response = self._process_long_response(user_response)
        
        # Prepare messages for analysis
        messages = [
            {"role": "system", "content": self.analysis_prompt},
            {"role": "user", "content": processed_response}
        ]
        
        # Get analysis
        analysis_result = self._call_api(messages)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": processed_response})
        self.conversation_history.append({"role": "assistant", "content": analysis_result})
        
        # Prepare messages for follow-up questions
        question_messages = [
            {"role": "system", "content": self.question_prompt},
            {"role": "user", "content": "Based on the current context and missing information, generate relevant follow-up questions."}
        ]
        
        # Get follow-up questions
        questions = self._call_api(question_messages)
        
        return {
            "analysis": analysis_result,
            "follow_up_questions": questions,
            "chat_history": self.conversation_history
        }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List:
        """Get the current conversation history."""
        return self.conversation_history 