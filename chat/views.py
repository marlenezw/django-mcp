from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage, AIMessage
from .models import ChatMessage


def chat_view(request):
    """Main chat interface"""
    messages = ChatMessage.objects.all()[:10]  # Get last 10 messages
    return render(request, 'chat/index.html', {'messages': messages})


async def get_mcp_response(user_message: str, chat_history: list = None) -> str:
    """Get response from MCP server using React agent with chat history"""
    try:

        server_params = StdioServerParameters(
            command="npx",
            args=[
                    "mcp-remote",
                    "https://huggingface.co/mcp",
                    "--header",
                    "Authorization: Bearer {hf_token}"
                ],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                # Get tools
                tools = await load_mcp_tools(session)

                # Check if Azure OpenAI is configured
                azure_endpoint = settings.AZURE_AI_ENDPOINT
                azure_api_key = settings.AZURE_AI_API_KEY
                version = settings.AZURE_AI_API_VERSION
                model = settings.AZURE_AI_DEPLOYMENT_NAME
               
                # Use Azure OpenAI
                llm = AzureAIChatCompletionsModel(
                    endpoint=azure_endpoint,
                    model=model,
                    api_version=version,
                    credential=azure_api_key
                )

                # Prepare messages with chat history
                messages = []
                if chat_history:
                    for chat in chat_history:
                        messages.append(HumanMessage(content=chat.message))
                        messages.append(AIMessage(content=chat.response))
                
                # Add current user message
                messages.append(HumanMessage(content=user_message))

                # Create and run the agent
                msft_agent = create_react_agent(llm, tools)
                agent_response = await msft_agent.ainvoke({"messages": messages})
                
                # Extract the response content
                if 'messages' in agent_response and agent_response['messages']:
                    last_message = agent_response['messages'][-1]
                    if hasattr(last_message, 'content'):
                        return last_message.content
                    elif isinstance(last_message, dict) and 'content' in last_message:
                        return last_message['content']
                
                return str(agent_response)
                
    except Exception as e:
        return f"Error with MCP server: {str(e)}. Falling back to simple AI response."


async def get_simple_ai_response(user_message: str, chat_history: list = None) -> str:
    """Fallback to simple AI response without MCP but with chat history"""
    try:
        # Check if Azure OpenAI is configured
        azure_endpoint = settings.AZURE_AI_ENDPOINT
        azure_api_key = settings.AZURE_AI_API_KEY
        version = settings.AZURE_AI_API_VERSION
        model = settings.AZURE_AI_DEPLOYMENT_NAME
        
        # Use Azure OpenAI
        llm = AzureAIChatCompletionsModel(
                    endpoint=azure_endpoint,
                    model=model,
                    api_version=version,
                    credential=azure_api_key
                )
        
        # Prepare messages with chat history
        messages = []
        if chat_history:
            for chat in chat_history:
                messages.append(HumanMessage(content=chat.message))
                # Add assistant response using AIMessage
                messages.append(AIMessage(content=chat.response))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"Error generating AI response: {str(e)}"


@csrf_exempt
def send_message(request):
    """Handle message sending and AI response"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message.strip():
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Get recent chat history (last 10 messages for context)
            chat_history = list(ChatMessage.objects.all()[:10])
            chat_history.reverse()  # Reverse to get chronological order
            
            # Try to get MCP response first, fall back to simple AI if it fails
            try:
                ai_response = asyncio.run(get_mcp_response(user_message, chat_history))
                # If MCP response contains an error message, try fallback
                if ai_response.startswith("Error with MCP server:"):
                    ai_response = asyncio.run(get_simple_ai_response(user_message, chat_history))
            except Exception as e:
                # If MCP completely fails, use simple AI response
                ai_response = asyncio.run(get_simple_ai_response(user_message, chat_history))
            
            # Save to database
            chat_message = ChatMessage.objects.create(
                message=user_message,
                response=ai_response
            )
            
            return JsonResponse({
                'success': True,
                'response': ai_response,
                'timestamp': chat_message.created_at.strftime('%H:%M')
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
def clear_chat(request):
    """Clear all chat messages"""
    if request.method == 'POST':
        try:
            ChatMessage.objects.all().delete()
            return JsonResponse({'success': True, 'message': 'Chat cleared successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
