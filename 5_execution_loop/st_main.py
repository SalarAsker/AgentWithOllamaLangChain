import streamlit as st
from agent import run
# from agent import tool_call_stats


st.title("Customer Service Assistant")

st.write(
    "Ask questions about orders, "
    "product stock, and deliveries."
)
st.divider()

question = st.text_area(
    "Enter your question:",
    placeholder=(
        "What product is included in order "
        "1052, and is it currently in stock?"
    ),
    height=120
)


if st.button("Ask Assistant", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner(
                "The agent is working..."
            ):

                answer = run(
                    user_question=question,
                    # max_tool_rounds=max_rounds
                )

            st.subheader("Assistant Response")

            st.write(answer[0])
            
            for tool in answer[1]:
                st.info(f"Tool called:\n\n {tool.name}")

        except Exception as error:

            st.error(
                "An error occurred while "
                "running the assistant."
            )

            st.caption(
                f"Error type: {type(error).__name__}"
            )

