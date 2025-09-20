# Pakistan Constitution Assistant

A Streamlit-based chatbot application that helps users understand Pakistan's Constitution through an interactive interface.

## Features

- **Chat Interface**: Interactive chat with the Constitution Assistant
- **Sidebar Information**:
  - Current chat topic display
  - Clear chat functionality
  - Reference documents from the knowledge base
- **Real-time Responses**: Streaming responses for better user experience
- **Chat History**: Maintains conversation context throughout the session

## Setup

### Local Development

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.streamlit/secrets.toml` file with your configuration:

   ```toml
   [pinecone]
   index = "your-pinecone-index-name"
   api_key = "your-pinecone-api-key"
   env = "your-pinecone-environment"

   [models]
   embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
   llm_model = "mixtral-8x7b-32768"

   [api_keys]
   hugging_face_token = "your-hugging-face-token"
   grok_api_key = "your-grok-api-key"

   [urls]
   base_url = "https://api.groq.com/openai/v1"
   ```

3. Run the application:

   ```bash
   streamlit run main.py
   ```

   Or use the batch file on Windows:

   ```bash
   run_app.bat
   ```

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and deploy your app
3. In the Streamlit Cloud dashboard, go to "Settings" → "Secrets"
4. Add the following secrets in the format:

   ```
   [pinecone]
   index = "your-pinecone-index-name"
   api_key = "your-pinecone-api-key"
   env = "your-pinecone-environment"

   [models]
   embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
   llm_model = "mixtral-8x7b-32768"

   [api_keys]
   hugging_face_token = "your-hugging-face-token"
   grok_api_key = "your-grok-api-key"

   [urls]
   base_url = "https://api.groq.com/openai/v1"
   ```

5. Replace the placeholder values with your actual API keys and configuration
6. Deploy the app

## Usage

1. **Ask Questions**: Type your constitutional questions in the chat input
2. **View References**: Check the sidebar for relevant constitutional documents
3. **Clear Chat**: Use the "Clear Chat" button to start a new conversation

## Components

- **main.py**: Streamlit interface and application logic
- **chatbot/bot.py**: Core chatbot functionality and LLM integration
- **chatbot/prompts.py**: System prompts and templates
- **secrets.toml**: Configuration for Streamlit Cloud deployment

## Features Provided by the Bot

1. **Response Generation**: Streaming responses from the LLM
2. **Reference Documents**: Relevant constitutional articles and provisions
3. **Topic Generation**: Automatic chat topic naming
