import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.hackernews import HackerNewsTools

load_dotenv()

agent = Agent(
    model=OpenRouter(
                id="meituan/longcat-flash-chat",
                api_key=os.getenv('OPENROUTER_API_KEY')
            ),
   #  tools=[HackerNewsTools()],
    markdown=True,
)
# agent.print_response("Summarize the top 5 stories on hackernews", stream=True)
agent.print_response("Share a 2 sentence horror story.")