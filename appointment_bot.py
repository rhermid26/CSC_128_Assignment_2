# the Streamlit interface
from flow import handle, new_state
import streamlit as st


if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_state" not in st.session_state:
    st.session_state.current_state = new_state();

if "current_user_text" not in st.session_state:
    st.session_state.current_user_text = "";

st.title("IT Help Desk Bot")
st.caption("This bot will help out with appointments")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

reply, next_state = handle(st.session_state.current_user_text, st.session_state.current_state)
st.session_state.current_state = next_state;
user_text = st.chat_input(reply)

if user_text:
    st.session_state.current_user_text = user_text;
    # first-run guard, then redraw it, then handle new input.
    st.session_state.messages.append(
        {
            "role": "user", 
            "content": user_text
        }
    )

    with st.chat_message("user"):
        st.write(user_text)

    st.session_state.messages.append(
        {
            "role": "assistant", 
            "content": reply
        }
    )

    with st.chat_message("assistant"):
        st.write(reply)
