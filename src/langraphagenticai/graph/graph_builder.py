from langgraph.graph import StateGraph,START,END
from src.langraphagenticai.nodes.chatbot_with_tool_node import  ChatBotWithToolNode
from src.langraphagenticai.state.state import State
from src.langraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode 
from langgraph.prebuilt import ToolNode,tools_condition
from src.langraphagenticai.tools.search_tool import  get_tools,create_tool_node
from src.langraphagenticai.nodes.ai_news_node import AINewsNode
import streamlit as st
class GraphBuilder:

    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)
    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This methold creates a chatbot graph that includes both a chatbot
        node and tool node. It defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes. 
        The Chatbot node is set as the entry point 
        """
        tools=get_tools()
        tool_node=create_tool_node(tools)

        llm=self.llm
        obj_chatbot_with_node=ChatBotWithToolNode(llm)
        # st.success("Chatbot with tool node success")
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
        # st.success("create chatbot success")
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        # self.graph_builder.add_edge("chatbot",END)




    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using Langraph 
        This methold initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into graph. The Chatbot node is set as both the entry 
        and exit point of the graph
        """

        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def ai_news_builder_graph(self):
        # st.success("Inside AI news builder graph")
        ai_news_node=AINewsNode(self.llm)
        # st.success("AI news node called successfully")
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_news",ai_news_node.save_result)
        # st.success("Added Node")
        self.graph_builder.set_entry_point("fetch_news")
        # st.success("Entry Point Called Sucess")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_news")
        self.graph_builder.add_edge("save_news",END)
        
    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case 
        """
        # st.success("Inside Function setup_graph")
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
            self.ai_news_builder_graph()
        return self.graph_builder.compile()
