import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

agno_agent = Agent(
    name="Agno Agent",
    model=OpenRouter(
                id="meituan/longcat-flash-chat",
                api_key=os.getenv('OPENROUTER_API_KEY')
            ),
    
    # Add a database to the Agent
    db=SqliteDb(db_file="agno.db"),
    
    # Add the Agno MCP server to the Agent
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    
    # Add the previous session history to the context
    add_history_to_context=True,
    markdown=True,
)


# Create the AgentOS
agent_os = AgentOS(agents=[agno_agent])

# Get the FastAPI app for the AgentOS
app = agent_os.get_app()