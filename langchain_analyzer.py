import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

class LangChainAnalyzer:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.7, memory=None, agent_role="project analyst"):
        """Initialize the LangChain-based response analyzer
        
        Args:
            model_name: The OpenAI model to use
            temperature: The temperature for generation
            memory: Optional shared memory to use (if None, creates a new one)
            agent_role: The role of this agent (e.g., "project analyst", "technical expert")
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=self.api_key
        )
        
        # Initialize conversation memory (use shared memory if provided)
        self.memory = memory if memory else ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # Define the analysis prompt template
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an expert {agent_role} and interviewer. Your task is to analyze user responses 
            and generate focused follow-up questions. You should:
            1. Analyze the user's response thoroughly
            2. Identify key information and any gaps
            3. Generate exactly ONE focused follow-up question based on the most important missing information
            4. Do not include numbering or multiple questions
            
            Current conversation context:
            {{history}}
            """),
            ("human", "{input}")
        ])
        
        # Define the summary prompt template
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an expert {agent_role}. Your task is to create a comprehensive summary 
            that incorporates all the information provided in the conversation. The summary should:
            1. Include all key details from the initial description
            2. Incorporate all information from follow-up questions and answers
            3. Be well-structured and easy to understand
            4. Highlight the most important aspects of the project or topic
            
            Current conversation context:
            {{history}}
            """),
            ("human", "Please provide a comprehensive updated summary incorporating all the information above.")
        ])
        
        # Create the analysis chain
        self.analysis_chain = LLMChain(
            llm=self.llm,
            prompt=self.analysis_prompt,
            memory=self.memory,
            verbose=True
        )
        
        # Create the summary chain
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=self.summary_prompt,
            memory=self.memory,
            verbose=True
        )
    
    def analyze_response(self, user_input, is_final_summary=False):
        """Analyze the user's response and generate appropriate follow-up or summary"""
        if is_final_summary:
            # Generate a comprehensive summary
            response = self.summary_chain.invoke({"input": user_input})
            return {
                "analysis": response["text"],
                "follow_up_questions": ""
            }
        else:
            # Generate a follow-up question
            response = self.analysis_chain.invoke({"input": user_input})
            
            # Extract the question from the response
            content = response["text"]
            analysis = content.split("Follow-up question:")[0].strip()
            question = content.split("Follow-up question:")[1].strip() if "Follow-up question:" in content else ""
            
            return {
                "analysis": analysis,
                "follow_up_questions": question
            }
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.memory.clear()
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.memory.chat_memory.messages


class MultiAgentAnalyzer:
    """A class to manage multiple specialized agents with shared memory"""
    
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.7):
        """Initialize the multi-agent analyzer
        
        Args:
            model_name: The OpenAI model to use
            temperature: The temperature for generation
        """
        # Create a shared memory for all agents
        self.shared_memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # Initialize specialized agents with different roles
        self.agents = {
            "project_analyst": LangChainAnalyzer(
                model_name=model_name, 
                temperature=temperature, 
                memory=self.shared_memory,
                agent_role="project analyst"
            ),
            "technical_expert": LangChainAnalyzer(
                model_name=model_name, 
                temperature=temperature, 
                memory=self.shared_memory,
                agent_role="technical expert"
            ),
            "business_consultant": LangChainAnalyzer(
                model_name=model_name, 
                temperature=temperature, 
                memory=self.shared_memory,
                agent_role="business consultant"
            )
        }
    
    def analyze_with_agent(self, agent_name, user_input, is_final_summary=False):
        """Analyze user input with a specific agent
        
        Args:
            agent_name: The name of the agent to use
            user_input: The user's input text
            is_final_summary: Whether to generate a final summary
            
        Returns:
            The analysis results from the specified agent
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}")
        
        return self.agents[agent_name].analyze_response(user_input, is_final_summary)
    
    def analyze_with_all_agents(self, user_input, is_final_summary=False):
        """Analyze user input with all agents and combine results
        
        Args:
            user_input: The user's input text
            is_final_summary: Whether to generate a final summary
            
        Returns:
            A dictionary with results from each agent
        """
        results = {}
        for agent_name, agent in self.agents.items():
            results[agent_name] = agent.analyze_response(user_input, is_final_summary)
        return results
    
    def reset_conversation(self):
        """Reset the shared conversation history"""
        self.shared_memory.clear()
    
    def get_conversation_history(self):
        """Get the shared conversation history"""
        return self.shared_memory.chat_memory.messages 

# Create a multi-agent system
multi_agent = MultiAgentAnalyzer() 

# Get a question from the technical expert
tech_result = multi_agent.analyze_with_agent("technical_expert", "Your project description")
print(tech_result["follow_up_questions"])

# Get a question from the business consultant
business_result = multi_agent.analyze_with_agent("business_consultant", "Your project description")
print(business_result["follow_up_questions"])

# Get questions from all agents
all_results = multi_agent.analyze_with_all_agents("Your project description")
for agent_name, result in all_results.items():
    print(f"{agent_name}: {result['follow_up_questions']}")

from langchain_analyzer import LangChainAnalyzer
from langchain.memory import ConversationBufferMemory

# Create a shared memory
shared_memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Create custom agents
security_expert = LangChainAnalyzer(
    memory=shared_memory,
    agent_role="security specialist"
)

data_scientist = LangChainAnalyzer(
    memory=shared_memory,
    agent_role="data scientist"
)

# Add a new agent that can see the entire conversation history
new_agent = LangChainAnalyzer(
    memory=shared_memory,  # Use the same shared memory
    agent_role="project manager"
) 