import streamlit as st
import requests

st.set_page_config(
    page_title="Hallo, Fintool AI!",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Du fragst. Die Fintool AI antwortet."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Die Fintool AI denkt nach..."):
            # Check if running in production by checking Streamlit's environment
            is_prod = st.secrets.get("ENV", "dev") == "prod"

            api_url = (
                "https://default-756637458404.europe-west6.run.app/api/queries"
                if is_prod
                else "http://127.0.0.1:8000/api/queries"
            )

            api_key = st.secrets.get("API_KEY")

            res = requests.post(
                url=api_url,
                json={
                    "prompt": prompt,
                },
                headers={"x-api-key": api_key},
            )
            response_json = res.json()
            st.markdown(response_json["response"]["response"]["response"])
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_json["response"]["response"]["response"],
        }
    )
