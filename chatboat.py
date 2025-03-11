import openai
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (Make sure .env file contains OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI Client
client = OpenAI()

# Initial system messages
initial_message = [
    {"role": "system", "content": "You are a trip planner in Dubai. You are an expert in Dubai tourism, location, events, hotels, etc. You are able to guide users to plan their vacation to Dubai. You should respond professionally. Your name is Sarang, short name SA. Response shouldn't exceed 100 words. always ask questions to user and help them to plan trip.finally give a day wise itinerary.deal with user professionally"},
    {"role": "assistant", "content": "Hello, I am SA, your expert trip planner. How can I help you?"}
]

# Function to fetch response from OpenAI
def get_response_from_llm(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content  # Extract the text content
    except openai.RateLimitError:
        st.error("⚠️ Rate limit exceeded. Please check your OpenAI quota.")
        return "Sorry, I can't respond right now. OpenAI quota exceeded."
    except openai.APIError as e:
        st.error(f"⚠️ API Error: {str(e)}")
        return "There was an issue with the API."
    except Exception as e:
        st.error(f"⚠️ Unexpected Error: {str(e)}")
        return "An unexpected error occurred."

# Initialize Streamlit app
st.title("Dubai Trip Assistant - Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = initial_message

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_message = st.chat_input("Enter your message:")
if user_message:
    new_message = {"role": "user", "content": user_message}
    st.session_state.messages.append(new_message)

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(user_message)

    # Get AI response
    response = get_response_from_llm(st.session_state.messages)
    
    if response:
        response_message= {"role": "assistant", "content": response}
        st.session_state.messages.append(response_message)

        # Display AI response in chat
        with st.chat_message("assistant"):
            st.markdown(response)
