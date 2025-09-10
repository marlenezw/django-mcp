# ChatGPT Clone with MCP Server Integration

🎉 **SUCCESS! Your advanced ChatGPT clone is now ready with MCP integration!**

A simple Django web application that mimics ChatGPT's interface with a beautiful light purple theme. This app uses LangChain, OpenAI/Azure OpenAI, and MCP (Model Context Protocol) servers to provide intelligent AI responses with enhanced capabilities.

## Features

- 🎨 Beautiful ChatGPT-like interface with light purple theme
- 🤖 AI-powered responses using OpenAI's GPT-3.5-turbo or Azure OpenAI
- 🔌 **MCP Server Integration**: Enhanced with Microsoft 365 MCP server capabilities
- 🛠️ **React Agent**: Uses LangGraph React agent for advanced tool usage
- 💬 Real-time chat functionality
- 📱 Responsive design for mobile and desktop
- 💾 Message history saved to database
- ⚡ Fast and lightweight with intelligent fallback

## What's New: MCP Integration

This app now integrates with MCP (Model Context Protocol) servers, specifically the Microsoft 365 MCP server. This means the AI can:

- Access Microsoft 365 services and tools
- Provide more contextual and action-oriented responses
- Use specialized tools for various tasks
- Fall back gracefully to standard AI responses if MCP fails

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Node.js (for MCP server)
- OpenAI API key OR Azure OpenAI credentials

### 2. Installation

1. **Clone or download this project**
   ```bash
   cd django_mcp
   ```

2. **Activate the virtual environment** (already created)
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (already installed)
   ```bash
   pip install django langchain-openai langchain-mcp-adapters langgraph mcp python-dotenv
   ```

4. **Configure API Keys**
   - Open the `.env` file in the root directory
   - Configure either OpenAI OR Azure OpenAI credentials:

   **Option A: OpenAI (recommended for simplicity)**
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

   **Option B: Azure OpenAI (enterprise)**
   ```
   AZURE_AI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_AI_API_KEY=your-azure-api-key-here
   AZURE_AI_API_VERSION=2024-02-15-preview
   AZURE_AI_DEPLOYMENT_NAME=gpt-4
   ```

5. **Run database migrations** (already done)
   ```bash
   python manage.py migrate
   ```

6. **Start the development server** (already running)
   ```bash
   python manage.py runserver
   ```

### 3. Usage

1. Open your web browser and go to: `http://127.0.0.1:8000/`
2. You'll see a beautiful ChatGPT-like interface
3. Type your message in the input field and press "Send"
4. The AI will respond using:
   - **First**: MCP React agent with Microsoft 365 tools
   - **Fallback**: Direct OpenAI/Azure OpenAI if MCP fails
   - **Demo**: Simple message if no API keys are configured

## Getting Your OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

## Project Structure

```
django_mcp/
├── chatgpt_app/           # Django project settings
├── chat/                  # Chat application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   └── templates/        # HTML templates
├── static/               # Static files
├── venv/                 # Virtual environment
├── .env                  # Environment variables
├── manage.py             # Django management script
└── README.md             # This file
```

## Features Explained

### Frontend
- **Modern UI**: Clean, ChatGPT-inspired interface
- **Light Purple Theme**: Beautiful gradient backgrounds and purple accents
- **Responsive Design**: Works perfectly on both desktop and mobile
- **Smooth Animations**: Hover effects and loading states
- **Real-time Updates**: Messages appear instantly

### Backend
- **Django Framework**: Robust and secure web framework
- **LangChain Integration**: Easy integration with OpenAI
- **Database Storage**: All conversations are saved
- **Error Handling**: Graceful error messages for users
- **Security**: CSRF protection and input validation

## Customization

### Changing the Theme
You can easily customize the purple theme by modifying the CSS variables in `chat/templates/chat/index.html`:

```css
/* Main purple color */
background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);

/* Light purple background */
background: linear-gradient(135deg, #f5f3ff 0%, #e9d5ff 100%);
```

### Using Different AI Models
You can change the AI model in `chat/views.py`:

```python
llm = ChatOpenAI(
    openai_api_key=api_key,
    model="gpt-4",  # Change to gpt-4 or other models
    temperature=0.7
)
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure you activated the virtual environment: `source venv/bin/activate`

2. **"Invalid API key" errors**
   - Check that your OpenAI API key is correctly set in the `.env` file
   - Ensure you have credits available in your OpenAI account

3. **Server won't start**
   - Make sure no other application is using port 8000
   - Try running on a different port: `python manage.py runserver 8001`

4. **Database errors**
   - Run migrations again: `python manage.py migrate`

## Development

To continue developing this app:

1. **Add new features** in the `chat` app
2. **Modify the UI** by editing the HTML template
3. **Add more AI models** by updating the views
4. **Add user authentication** for personalized conversations

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure a proper database (PostgreSQL recommended)
3. Set up a web server (nginx + gunicorn)
4. Use environment variables for all secrets
5. Enable HTTPS

## License

This project is for educational purposes. Please respect OpenAI's usage policies when using their API.

---

🎉 **Your ChatGPT clone is ready!** Visit `http://127.0.0.1:8000/` to start chatting!
