# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI

# Import schema simplifier utilities
from tool_schema_simplifier import simplify_tools_for_openai

# Load environment variables from .env file
load_dotenv() 

async def main():
    """Main async function to run the email app"""
    server_params = StdioServerParameters(
        command="npx",
        # Make sure to update to the full absolute path to your math_server.py file
        args=["-y", "@softeria/ms-365-mcp-server", "--org-mode"],
    )


    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Simplify schemas to avoid OpenAI tool schema validation failures
            tools = simplify_tools_for_openai(tools)

            llm = AzureChatOpenAI(
                azure_endpoint=os.environ.get("AZURE_AI_ENDPOINT"),
                api_key=os.environ.get("AZURE_AI_API_KEY"),
                api_version= os.environ.get("AZURE_AI_API_VERSION"),
                deployment_name= os.environ.get("AZURE_AI_DEPLOYMENT_NAME", "gpt-5-mini"),
                # default_headers={
                #     "reasoning": "{'effort': 'minimal'}"
                # } 
            )

            # Create and run the agent
            # llm_with_tools = llm.bind_tools(tools, strict=False)
            msft_agent = create_react_agent(llm, tools)
            agent_response = await msft_agent.ainvoke({"messages":"provide the user with the link to login using the login tool"})
            print(agent_response)

if __name__ == "__main__":
    asyncio.run(main())