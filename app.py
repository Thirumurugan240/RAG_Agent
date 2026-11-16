import os
import pandas as pd
import streamlit as st
from agent import crew

cart_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cart.xlsx")

st.set_page_config(page_title="ShopEasy Assistant", page_icon="🛍️", layout="wide")
st.title("🛍️ ShopEasy Shopping Assistant")
st.write("Ask about products or manage your cart. Example: *Which smart watch do you have?* or *Add 2 power banks to my cart*")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask about a product or your cart...")

if question:
    history = ""
    for msg in st.session_state.messages[-6:]:
        history = history + msg["role"] + ": " + msg["content"] + "\n"

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = crew.kickoff(inputs={"history": history, "question": question})
            answer = result.raw
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.sidebar.header("🛒 Your Cart")
if os.path.exists(cart_file):
    cart = pd.read_excel(cart_file)
    if cart.empty:
        st.sidebar.write("Your cart is empty.")
    else:
        st.sidebar.dataframe(cart, hide_index=True)
        st.sidebar.subheader("Total: Rs. " + str(cart["total"].sum()))
else:
    st.sidebar.write("Your cart is empty.")
