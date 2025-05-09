import streamlit as st
import json
import os
from agents.supervisor import SupervisorAgent
from utils.config import load_config

# Set page configuration
st.set_page_config(
    page_title="Financial Assistant",
    page_icon="💰",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'supervisor_agent' not in st.session_state:
    config = load_config()
    st.session_state.supervisor_agent = SupervisorAgent(config)

# App title and description
st.title("Financial Assistant")
st.markdown("""
This application simulates a financial assistant powered by Amazon Bedrock's 
multi-agent collaboration framework. It can help you with:
- Creating investment portfolios based on industry and company count
- Providing financial data insights and FOMC report summaries
- Sending portfolio details via email
""")

# Sidebar for user information
with st.sidebar:
    st.header("User Information")
    user_email = st.text_input("Email Address (for portfolio delivery)", placeholder="your.email@example.com")
    st.divider()
    
    st.header("About")
    st.markdown("""
    This assistant uses a three-agent architecture:
    1. **Supervisor Agent** - Orchestrates requests and user interaction
    2. **Portfolio Assistant** - Creates portfolios and sends emails
    3. **Data Assistant** - Provides financial insights and report summaries
    """)

# Main interaction area
st.header("Chat with your Financial Assistant")

# Input form
with st.form(key="user_input_form"):
    user_input = st.text_area("Ask about portfolios, financial data, or FOMC reports:", 
                              placeholder="Example: Create a portfolio of 5 top technology companies")
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.form_submit_button("Send")

# Display chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.chat_message('user').write(message['content'])
    else:
        st.chat_message('assistant').write(message['content'])

# Process the user request
if submit_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })
    
    # Display user message
    st.chat_message('user').write(user_input)
    
    # Process the request through the supervisor agent
    with st.spinner('Processing your request...'):
        response = st.session_state.supervisor_agent.process_request(
            user_input, 
            user_email=user_email
        )
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response
    })
    
    # Display assistant response
    st.chat_message('assistant').write(response)
    
    # Clear the input area for the next question
    st.rerun()

# Quick action buttons
st.header("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Create Tech Portfolio"):
        prompt = "Create a portfolio of 3 top technology companies"
        if 'user_input_form' in locals():
            user_input = prompt
            submit_button = True

with col2:
    if st.button("Create Real Estate Portfolio"):
        prompt = "Create a portfolio of 3 top real estate companies"
        if 'user_input_form' in locals():
            user_input = prompt
            submit_button = True

with col3:
    if st.button("Latest FOMC Summary"):
        prompt = "What's in the latest FOMC report?"
        if 'user_input_form' in locals():
            user_input = prompt
            submit_button = True
