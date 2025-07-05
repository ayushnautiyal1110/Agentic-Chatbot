import streamlit as st
from src.langraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langraphagenticai.LLMS.groqllm import GroqLLM
from src.langraphagenticai.graph.graph_builder import GraphBuilder
from src.langraphagenticai.ui.streamlitui.display_results import DisplayResultStreamlit

def load_langraph_agentic_ai_app():
    """
    Loads and runs the Langgraph Agentic AI application with Streamlit UI.
    This function initializes the UI handles user input ,configures the LLM Model
    sets up the graph based on the selected usecase ,and displays the output while 
    implementing exception handling for robustness.
    """
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()
    if not user_input:
        st.error("Error : Failed to load user input from the UI")
        return 
    user_message=st.chat_input("Enter your Message")
    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_inputs=user_input)
            model=obj_llm_config.get_llm_model()
            if not model:
                st.error("Error : LLM model cannot be iniatized")
                return
            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("Error No use case selected")
                return
            
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error : Graph Set up Failed {e}")
                return 
        except Exception as e:
            st.error(f"Graph Set up Failed - {e}")
            return 