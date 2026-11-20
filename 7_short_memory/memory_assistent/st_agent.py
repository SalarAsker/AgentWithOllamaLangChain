# st_agent.py
# Streamlit Customer Service with different thread_ids

import streamlit as st
from agent_for_st import create_customer_service_agent


# create and cache the agent
if "agent" not in st.session_state:
    st.session_state.agent = create_customer_service_agent()

agent = st.session_state.agent


st.set_page_config(
    page_title="Customer Service Assistant",
    page_icon="🤖",
    layout="centered"
)



st.title("Customer Service Assistant")
st.info( "Enter your order number to check its status.")


# -----------------------------------------
# 1. Initialize Streamlit session state
# -----------------------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "active_thread" not in st.session_state:
    st.session_state.active_thread = None

# -----------------------------------------
# 2. Sidebar: Select conversation thread
# -----------------------------------------
with st.sidebar:

    st.write(
        "Enter your order reference number "
        "to start or continue a conversation."
    )

    reference_number = st.text_input(
        "Order Reference Number",
        placeholder="00112233"
    )

    if st.button("Open Conversation", type="primary"):

        reference_number = reference_number.strip()

        if not reference_number:
            st.warning("Please enter an order reference number.")

        elif not reference_number.isdigit():
            st.warning("The reference number must contain only digits.")

        else:

            # Reference number becomes the thread_id
            st.session_state.active_thread = reference_number

            # Create visible chat history for new threads
            if reference_number not in st.session_state.conversations:
                st.session_state.conversations[reference_number] = []

            st.rerun()

# -----------------------------------------
# 3. Require an order reference number
# -----------------------------------------
if st.session_state.active_thread is None:

    st.warning(
        "Please enter your order reference number "
        "in the sidebar to begin."
    )

    st.stop() # stop the further execution of the application


# Otherwise if there is an reference number saved
# as active thread we will read it and get the conversation
# history of that id
thread_id = st.session_state.active_thread
st.subheader(f"Order Reference: {thread_id}")

# # 5. Display conversation history
chat_history = st.session_state.conversations[thread_id]
# Insert the chat history to the message flow
for message in chat_history:
    with st.chat_message(message["role"]): # role is: user or assistent
        st.markdown(message["content"])


# -----------------------------------------
# 6. Receive customer question
# -----------------------------------------
question = st.chat_input(
    "Ask about your order..."
)

if question:

  # Append chat history with new prompt question 
    chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Use the reference number as thread_id
    config = {
        "configurable": {
            # "thread_id": thread_id
            "thread_id": st.session_state.active_thread

        },
        "recursion_limit": 20
    }
    
    # Invoke the memory-enabled agent
    with st.chat_message("assistant"):

        try:
            with st.spinner("Checking your request..."):

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    },
                    config=config
                )

                answer = result["messages"][-1].content

                if not isinstance(answer, str):
                    answer = str(answer)

            st.markdown(answer)
          
           # Append chat history with answer to the prompt
            chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception as error:

            st.error(
                f"Unable to process your request: {error}"
            )
