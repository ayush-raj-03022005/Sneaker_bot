import streamlit as st
import requests
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set page config
st.set_page_config(
    page_title="🚀 Ultimate Sneaker Bot",
    page_icon="👟",
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hey sneakerhead! 🔥 Ask me about upcoming releases, raffles, or restocks!"
    }]

# Configure sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("OpenRouter API Key", type="password")
    st.markdown("[Get API Key](https://openrouter.ai/keys)")
    
    # Model selection
    model_name = st.selectbox(
        "Choose Model",
        ( "google/palm-2-chat-bison"),
        index=0
    )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7)
        max_retries = st.number_input("Max Retries", 1, 5, 2)
    
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Chat cleared! Ask me about sneakers!"
        }]

# Main interface
st.title("👟 AI Sneaker Release Tracker")
st.caption("Never miss a drop with real-time updates on limited editions and exclusive releases")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about sneakers..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("🔑 API key required! Check sidebar settings")
        st.stop()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        attempts = 0
        
        while attempts < max_retries:
            try:
                # API request with enhanced formatting controls
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sneaker-bot.streamlit.app",
                        "X-Title": "Ultimate Sneaker Bot"
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": f"""You are a professional sneaker release analyst. Follow these STRICT rules:
1. RESPOND ONLY IN PLAIN TEXT
2. NEVER USE JSON, MARKDOWN, OR CODE BLOCKS
3. Format lists with hyphens (-) only
4. Include dates in format: Month Day, Year (e.g., February 17, 2024)
5. Structure responses clearly with line breaks
6. If unsure about information, say "I need to verify that"
7. Maintain enthusiastic, helpful tone
8. Give info in structured format:
- Release Name: [Name] and then info
9. Current date: {time.strftime("%B %d, %Y")}

Failure to follow these rules will result in poor user experience!"""
                            },
                            *st.session_state.messages
                        ],
                        "temperature": temperature,
                        "response_format": {"type": "text"}
                    },
                    timeout=15
                )

                response.raise_for_status()
                data = response.json()
                raw_response = data['choices'][0]['message']['content']
                
                # Clean response pipeline
                processed_response = raw_response
                
                # Remove common formatting artifacts
                formatting_cleaners = [
                    ("```json", ""), ("```", ""), ("\\boxed{", ""),
                    ("**", ""), ("###", ""), ("####", ""), ("\\n", "\n"),
                    ('"', "'"), ("{", ""), ("}", "")
                ]
                
                for pattern, replacement in formatting_cleaners:
                    processed_response = processed_response.replace(pattern, replacement)
                
                # Attempt JSON parsing if any remains
                try:
                    json_response = json.loads(processed_response)
                    if 'response' in json_response:
                        processed_response = json_response['response']
                    elif 'answer' in json_response:
                        processed_response = json_response['answer']
                except:
                    pass
                
                # Final cleanup
                processed_response = processed_response.strip()
                
                # Stream response
                for chunk in processed_response.split():
                    full_response += chunk + " "
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.03)
                
                response_placeholder.markdown(full_response)
                break
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON Error: {str(e)}")
                attempts += 1
                if attempts == max_retries:
                    response_placeholder.error("⚠️ Failed to process response. Try rephrasing your question")
                    full_response = "Error: Please try a different question format"
                else:
                    time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                response_placeholder.error(f"🌐 Network Error: {str(e)}")
                full_response = "Error: Connection issue - try again later"
                break
                
            except Exception as e:
                logging.error(f"Unexpected Error: {str(e)}")
                response_placeholder.error(f"❌ Unexpected error: {str(e)}")
                full_response = "Error: Please check your input and try again"
                break

    st.session_state.messages.append({"role": "assistant", "content": full_response})