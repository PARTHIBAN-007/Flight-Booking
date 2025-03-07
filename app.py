import sys
import datetime
import streamlit as st
import os

from dotenv import load_dotenv

st.set_page_config(page_title="✈️ FlightFinder Pro", layout="wide")

st.markdown("<h1 style='color: #0066cc;'>✈️ FlightFinder Pro</h1>", unsafe_allow_html=True)
st.subheader("Flight Booking Assistant")
