import streamlit as st
import requests
import json
import time
import logging
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set page config with sneaker theme
st.set_page_config(
    page_title="🔥 Ultimate Sneaker Bot",
    page_icon="👟",
    layout="centered",
    initial_sidebar_state="expanded"
    
)

# Custom CSS for sneaker theme
def set_custom_theme():
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1600269452121-4f2416e55c28?q=80&w=2940&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .stChatMessage {{
            background-color: rgba(20, 20, 20, 0.9) !important;
            border-radius: 15px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }}
        .stChatMessage p {{
            font-size: 1.1rem !important;
            line-height: 1.6 !important;
        }}
        .stTextInput input {{
            background-color: rgba(30, 30, 30, 0.9) !important;
            color: white !important;
            border: 1px solid #444 !important;
        }}
        .stSelectbox select {{
            background-color: rgba(30, 30, 30, 0.9) !important;
            color: white !important;
        }}
        .stSlider .st-eb {{
            background-color: #ff4b4b !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(10, 10, 10, 0.95) !important;
            border-right: 1px solid #333 !important;
        }}
        .stButton button {{
            background-color: #ff4b4b !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
        }}
        .stButton button:hover {{
            background-color: #ff3333 !important;
        }}
        .css-1aumxhk {{
            color: #ff4b4b !important;
        }}
    </style>
    """, unsafe_allow_html=True)

set_custom_theme()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hey sneakerhead! 🔥 Ready to cop some heat? Ask me about:\n\n- 🔥 Upcoming releases\n- 🎟️ Raffles and drops\n- 🏪 Restock alerts\n- 📅 Release dates\n- 💰 Resell prices\n\nI'm your ultimate sneaker sidekick! 👟"
    }]

# Configure sidebar
with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu4byn3HNxpKbRIwDnVHdLt9buh2JE5p0mFg&s", width=200)
    st.title("⚙️ Bot Settings")
    
    with st.container():
        api_key = st.text_input("🔑 OpenRouter API Key", type="password")
        st.markdown("[Get API Key](https://openrouter.ai/keys)")
        
        # Model selection
        model_name = st.selectbox(
            "🤖 Choose Model",
            ("google/palm-2-chat-bison",),
            index=0
        )
        
        # Advanced settings
        with st.expander("🎛️ Advanced Settings"):
            temperature = st.slider("🎨 Response Creativity", 0.0, 1.0, 0.7)
            max_retries = st.number_input("🔄 Max Retries", 1, 5, 2)
        
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "🧹 Chat cleared! Ask me about the latest sneaker drops! 👟🔥"
            }]
    
    st.markdown("---")
    st.markdown("### 🔥 Popular Queries")
    if st.button("What's dropping this week?"):
        st.session_state.messages.append({"role": "user", "content": "What are the hottest sneaker releases this week?"})
    if st.button("Nike raffles near me"):
        st.session_state.messages.append({"role": "user", "content": "Where can I enter Nike raffles in my area?"})
    if st.button("Best resell value"):
        st.session_state.messages.append({"role": "user", "content": "Which upcoming sneakers have the best resell value?"})

# Main interface
colored_header(
    label="🔥 AI SNEAKER RELEASE TRACKER",
    description="Never miss a drop with real-time updates on limited editions and exclusive releases",
    color_name="red-70",
)

st.caption("👟 Powered by Ayush Raj | Shokendra Singh | Marouf Wani")

# Sneaker release ticker (fake data)
with stylable_container(
    key="ticker",
    css_styles="""
    {
        background-color: rgba(255, 75, 75, 0.2);
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 75, 75, 0.3);
        animation: scroll 20s linear infinite;
    }
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    """
):
    st.markdown("""
    <marquee behavior="scroll" direction="left" scrollamount="10">
    🚀 COMING SOON: Nike Dunk Low "Vintage Black" (May 15) | 🔥 Adidas Yeezy Boost 350 V2 "Onyx" Restock (May 18) | 🎟️ Jordan 1 Retro High OG "Shadow 2.0" Raffle Open | 💰 Travis Scott x Air Jordan 1 Low Resell: $1,200+
    </marquee>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Add emoji enhancement to assistant messages
        if message["role"] == "assistant":
            enhanced_content = message["content"]
            # Replace list indicators with emoji bullets
            enhanced_content = enhanced_content.replace("-", "•")
            st.markdown(enhanced_content)
        else:
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about sneakers..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("🔐 API key required! Please enter your OpenRouter key in the sidebar.")
        st.stop()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        attempts = 0
        
        # Thinking animation
        with st.spinner("🔍 Checking the latest sneaker news..."):
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
1. RESPOND IN PLAIN TEXT WITH EMOJIS
2. NEVER USE JSON, MARKDOWN, OR CODE BLOCKS
3. Format lists with bullet points (•)
4. Include dates in format: Month Day, Year (e.g., February 17, 2024)
5. Structure responses clearly with line breaks
6. If unsure about information, say "I need to verify that"
7. Maintain enthusiastic, helpful tone with relevant emojis
8. Give info in structured format:
• 🔥 Release Name: [Name] 
• 📅 Release Date: [Date]
• 🏪 Where to Buy: [Stores]
• 💰 Resell Estimate: [Price]
9. Current date: {time.strftime("%B %d, %Y")}

Example response:
🔥 Nike Air Jordan 1 Retro High OG "Bred Patent"
📅 Release Date: May 20, 2024
🏪 Where to Buy: SNKRS App, Foot Locker, Champs
💰 Resell Estimate: $400-$600 depending on size

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
                    
                    # Enhanced emoji processing
                    emoji_mapping = {
                        "release": "🔥",
                        "date": "📅",
                        "buy": "🏪",
                        "price": "💰",
                        "raffle": "🎟️",
                        "tip": "💡",
                        "warning": "⚠️",
                        "success": "✅"
                    }
                    
                    # Process response
                    processed_response = raw_response
                    for word, emoji in emoji_mapping.items():
                        processed_response = processed_response.replace(
                            f"{word.capitalize()}:", f"{emoji} {word.capitalize()}:"
                        )
                    
                    # Stream response with typing effect
                    for chunk in processed_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        response_placeholder.markdown(full_response + "▌")
                    
                    # Final display
                    response_placeholder.markdown(full_response)
                    break
                    
                except json.JSONDecodeError as e:
                    logging.error(f"JSON Error: {str(e)}")
                    attempts += 1
                    if attempts == max_retries:
                        response_placeholder.error("⚠️ Failed to process response. Try rephrasing your question")
                        full_response = "🔄 Error: Please try asking differently or check back later"
                    else:
                        time.sleep(0.5)
                    
                except requests.exceptions.RequestException as e:
                    response_placeholder.error(f"🌐 Network Error: {str(e)}")
                    full_response = "⚠️ Connection issue - try again later"
                    break
                    
                except Exception as e:
                    logging.error(f"Unexpected Error: {str(e)}")
                    response_placeholder.error(f"❌ Unexpected error: {str(e)}")
                    full_response = "😢 Oops! Something went wrong. Please try again."
                    break

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})