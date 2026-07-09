
import streamlit as st

# Task 1: The UI Shell
st.title("Echo Chamber 9000")
st.write("Enter your name and a message below, then hit Transmit to send it into the void.")

# Task 2: Multi-Data Collection
user_name = st.text_input("Name")
user_message = st.text_input("Message")

# Task 3: The Action Gate
if st.button("Transmit"):

    # Task 4: Conditional Routing (Edge Cases)
    if user_name == "":
        st.error("Please provide your name.")
    elif user_message == "":
        st.warning("Please type a message to transmit.")
    else:
        # Task 5: The Formatted Output
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")

        # Advanced Challenge: Token Cost Estimator
        char_count = len(user_message)
        token_count = char_count // 4
        st.info(f"System Check: Your message will consume approximately {token_count} tokens from our context window.")
