from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINews Node with API Keys for Tavily and Groq
        """
        self.tavily=TavilyClient()
        self.llm=llm
        self.state={}
    
    def fetch_news(self,state: dict)->dict:
        """
        Fetch AI news based on the specified frequency.
        Args:
            state(dict): The state dictionary containing 'frequency'
        Returns:
            dict : Updated  state   with 'news_data' key containing fetched news
        """
        frequency=state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map={'daily':'d' , 'weekly':'w', 'monthly':'m','year':'y'}
        days_map={'daily':1,'weekly':7 , 'monthly':30, 'year':366}

        response=self.tavily.search(
            query="Give the news of India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],

        )
        state['news_data']=response.get('results',[])
        self.state['news_data']=state['news_data']
        # st.success("Fetch News Called Succesfully")
        return state
    def summarize_news(self,state:dict)->dict:
        """
        Summarize  the fetched news using an LLM 
        Args :
            state (dict) : The state dictionary  containing 'news_data'
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.

        """
        news_items=self.state['news_data']
        prompt_template=ChatPromptTemplate.from_messages([
            (
                "system","""
                        Summarize news articles into markdown format . For each item include:
                        - Date in **YYYY-MM-DD** format in IST timezone 
                        - Concise sentences summary from latest news 
                        - Sort news by date wise (latest first)
                        - Source URL as link 
                        Use format :
                        ### [Date]
                        - [Summary](URL) 
                    """
            ),("user","Articles:\n{articles}")
        ])
        articles_str="\n\n".join(
            [
                f"Content:{item.get('content','')}\nURL:{item.get('url','')}\nDate: {item.get('published_date','')}"
                for item in news_items
            ]
        ) 
        response=self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary']=response.content
        self.state['summary']=state['summary']
        return self.state
    
    def save_result(self,state):
        frequency=self.state['frequency']
        summary=self.state['summary']
        filename=f"./News/{frequency}_summary.md"
        with open(filename,'w') as f:
            f.write(f"# {frequency.capitalize()} News Summary\n\n")
            f.write(summary)
        self.state['filename']=filename
        return self.state
    