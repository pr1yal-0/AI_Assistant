# app.py
import streamlit as st
from dotenv import load_dotenv
import sys
import os
import threading
import queue
import time

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from graph import build_graph

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="LangGraph AI Assistant", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #000000; }
.main { padding-top: 3rem; max-width: 750px; margin: auto; }
h1 { text-align: center; color: #ffffff; font-weight: 600; }
.subtitle { text-align: center; color: #9ca3af; margin-bottom: 25px; }
textarea { background-color: #111827 !important; border-radius: 12px !important; padding: 14px !important; font-size: 16px !important; color: #ffffff !important; border: 1px solid #374151 !important; }
textarea::placeholder { color: #6b7280 !important; }
.output-box { background-color: #111827; border-radius: 12px; padding: 16px; border: 1px solid #374151; margin-top: 10px; line-height: 1.6; color: #e5e7eb; }
.footer { padding: 40px 0 20px; text-align: center; color: #9ca3af; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "processing" not in st.session_state:
    st.session_state.processing = False
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "cancel_flag" not in st.session_state:
    st.session_state.cancel_flag = threading.Event()
if "result_queue" not in st.session_state:
    st.session_state.result_queue = queue.Queue()
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ---------------- UI ----------------
st.title("LangGraph AI Assistant")
st.markdown("<div class='subtitle'>Built with LangGraph + Ollama in Local</div>", unsafe_allow_html=True)

# Text area
st.text_area(
    "Enter your problem",
    height=160,
    placeholder="Ask a question, explain a task, or enter a problem...",
    value=st.session_state.user_input,
    key="user_input_widget",
    disabled=st.session_state.processing
)

# Placeholders
status_placeholder = st.empty()
reasoning_placeholder = st.empty()
final_placeholder = st.empty()

# ---------------- SINGLE BUTTON ----------------
button_label = "Cancel" if st.session_state.processing else "Solve"
button_clicked = st.button(button_label, use_container_width=True)

# ---------------- BACKGROUND FUNCTION ----------------
def run_graph(input_text, cancel_event, result_queue):
    print(f"[LOG] Starting graph execution for: {input_text[:60]}...")
    try:
        graph = build_graph()
        result = graph.invoke({"input": input_text})
        if not cancel_event.is_set():
            print("[LOG] Graph execution completed successfully")
            result_queue.put(result)
        else:
            print("[LOG] Execution cancelled")
    except Exception as e:
        print(f"[ERROR] Graph execution failed: {e}")
        if not cancel_event.is_set():
            result_queue.put({"reasoning": f"Error: {e}", "final_output": ""})
    finally:
        cancel_event.clear()

# ---------------- BUTTON ACTION ----------------
if button_clicked:
    if st.session_state.processing:
        print("[LOG] Cancel button clicked")
        st.session_state.cancel_flag.set()
        status_placeholder.markdown("<div class='output-box'>Cancelling request... Please wait.</div>", unsafe_allow_html=True)
    else:
        current_input = st.session_state.user_input_widget.strip()
        if not current_input:
            st.error("⚠️ Field should not be empty. Please enter your problem.")
        else:
            print("[LOG] Solve button clicked")
            st.session_state.processing = True
            st.session_state.last_result = None
            st.session_state.cancel_flag.clear()
            st.session_state.result_queue = queue.Queue()

            status_placeholder.markdown("<div class='output-box'>Processing your request... Please wait.</div>", unsafe_allow_html=True)

            thread = threading.Thread(
                target=run_graph,
                args=(current_input, st.session_state.cancel_flag, st.session_state.result_queue),
                daemon=True
            )
            thread.start()

# ---------------- AUTO-CHECK WHILE PROCESSING ----------------
if st.session_state.processing:
    if not st.session_state.result_queue.empty():
        result = st.session_state.result_queue.get()
        st.session_state.processing = False
        st.session_state.last_result = result

        # Use container to reliably show subheader + content
        with reasoning_placeholder.container():
            st.subheader("🧠 Reasoning Steps")
            st.markdown(f"<div class='output-box'>{result.get('reasoning', 'No reasoning')}</div>", unsafe_allow_html=True)

        with final_placeholder.container():
            st.subheader("✅ Final Answer")
            st.markdown(f"<div class='output-box'>{result.get('final_output', 'No answer')}</div>", unsafe_allow_html=True)

        status_placeholder.empty()
        st.session_state.user_input = ""
        st.rerun()

    elif st.session_state.cancel_flag.is_set():
        status_placeholder.markdown("<div class='output-box'>Request cancelled successfully.</div>", unsafe_allow_html=True)
        st.session_state.processing = False
        st.session_state.user_input = ""
        time.sleep(0.5)
        st.rerun()

    else:
        status_placeholder.markdown("<div class='output-box'>Processing... This may take a few seconds.</div>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.rerun()

# ---------------- DISPLAY RESULT (persistent) ----------------
if st.session_state.last_result is not None:
    result = st.session_state.last_result

    with reasoning_placeholder.container():
        st.subheader("=> Reasoning Steps")
        st.markdown(f"<div class='output-box'>{result.get('reasoning', 'No reasoning')}</div>", unsafe_allow_html=True)

    with final_placeholder.container():
        st.subheader("=> Final Answer")
        st.markdown(f"<div class='output-box'>{result.get('final_output', 'No answer')}</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<div class='footer'>"
    "Made by <b>Priyal Lunagariya</b>"
    "</div>",
    unsafe_allow_html=True
)
