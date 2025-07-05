from src.langraphagenticai.state.state import State 
class BasicChatbotNode:
    """
    Basic Chatbot Login Implementation
    """
    def __init__(self,model):
        self.llm=model
    
    def process(self,state:State)->dict:
        """
        Processes the input state and genrates a chatbot response.
        """
        return {"messages":self.llm.invoke(state["messages"])} 