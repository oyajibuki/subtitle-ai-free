import streamlit as st
import sys
import os

st.title("Streamlit Environment Check")
st.write(f"Python Executable: `{sys.executable}`")
st.write(f"Python Version: `{sys.version}`")
st.write("System Path:")
st.code("\n".join(sys.path))

try:
    import supabase
    st.success(f"Supabase found at: `{supabase.__file__}`")
except ImportError as e:
    st.error(f"Supabase Import Error: {e}")
