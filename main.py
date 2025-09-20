import streamlit as st
import time
from chatbot.bot import Bot

# Configure page
st.set_page_config(
    page_title="Pakistan Constitution Assistant",
    page_icon="📜",
    layout="wide"
)

# Initialize the chatbot
@st.cache_resource
def load_bot():
    return Bot()

def clear_chat():
    """Clear all chat-related session state"""
    st.session_state.messages = []
    st.session_state.current_topic = ""
    st.session_state.reference_docs = []

def format_chat_history_for_bot(messages):
    """Convert streamlit messages format to bot-compatible format"""
    history = []
    for message in messages:
        if message["role"] == "user":
            history.append(f"User: {message['content']}")
        elif message["role"] == "assistant":
            history.append(f"Assistant: {message['content']}")
    return "\n".join(history)

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    if "reference_docs" not in st.session_state:
        st.session_state.reference_docs = []

    # Load the bot
    try:
        bot = load_bot()
    except Exception as e:
        st.error(f"Error loading chatbot: {str(e)}")
        return

    # Sidebar
    with st.sidebar:
        st.title("📜 Pakistan Constitution Assistant")
        
        # Chat name display
        if st.session_state.current_topic:
            st.subheader("Current Chat")
            st.write(st.session_state.current_topic)
        else:
            pass
            # st.write("*No active chat*")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Reference documents section - removed from sidebar, now shown after messages

    # Main chat interface
    st.title("Constitution of Pakistan Assistant")
    st.markdown("Ask me anything about Pakistan's Constitution!")

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("What would you like to know about Pakistan's Constitution?")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            try:
                # Prepare chat history for the bot
                history = format_chat_history_for_bot(st.session_state.messages[:-1])  # Exclude current message
                
                # Get response from bot
                with st.spinner("Thinking..."):
                    response_stream, ref_data = bot.get_query_response(prompt, history if history else None)
                
                # Stream the response
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                # Final response without cursor
                response_placeholder.markdown(full_response)
                
                # Display references immediately after the response
                if ref_data:
                    st.markdown("---")
                    st.markdown("**📚 Reference Documents:**")
                    
                    with st.expander("View References", expanded=False):
                        for j, doc in enumerate(ref_data[:5]):  # Show top 5
                            st.write(f"**Reference {j+1}** (Score: {doc['score']:.3f})")
                            st.write(f"*Source:* {doc['metadata'].get('source', 'Unknown')}")
                            # st.write(f"*Page:* {doc['metadata'].get('page', 'N/A')}")
                            with st.expander(f"Content {j+1}"):
                                st.write(doc['page_content'][:300] + "..." if len(doc['page_content']) > 300 else doc['page_content'])
                            st.markdown("---")
                
                # Add assistant response to chat history with references
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response,
                    "reference_docs": ref_data
                })
                
                # Get topic for the conversation
                try:
                    topic = bot.get_topic(prompt, full_response)
                    
                    if topic and topic.strip():
                        st.session_state.current_topic = topic.strip()
                
                except Exception as e:
                    st.error(f"Error getting topic: {str(e)}")
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                st.error("Please check your configuration and try again.")

if __name__ == "__main__":
    main()