import sys
import datetime
import streamlit as st
import os
from crewai import Crew, Process, Task, Agent
from duckduckgo_search import DDGS
from crewai.tools import tool
from dotenv import load_dotenv

st.set_page_config(page_title="✈️ FlightFinder Pro", layout="wide")

st.markdown("<h1 style='color: #0066cc;'>✈️ FlightFinder Pro</h1>", unsafe_allow_html=True)
st.subheader("Powered by DuckDuckGo and CrewAI")

# Sidebar for API key input
with st.sidebar:
    st.header("Search Configuration")
    st.markdown("DuckDuckGo is being used for searches, no API key required.")

# Load environment variables
load_dotenv()

# Flight search form
st.header("Search for Flights")
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin City (IATA Code)", "SFO")
    departure_date = st.date_input("Departure Date", datetime.date.today() + datetime.timedelta(days=30))

with col2:
    destination = st.text_input("Destination City (IATA Code)", "JFK")
    return_date = st.date_input("Return Date (Optional)", datetime.date.today() + datetime.timedelta(days=37))

search_button = st.button("Search Flights")

@tool("Kayak tool")
def kayak_search(departure: str, destination: str, date: str, return_date: str = None) -> str:
    """
    Generates a Kayak URL for flights between departure and destination on the specified date.
    """
    url = f"https://www.kayak.com/flights/{departure}-{destination}/{date}"
    if return_date:
        url += f"/{return_date}"
    url += "?currency=USD"
    return url

kayak = kayak_search

def search_flights_duckduckgo(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
    return results

if search_button:
    with st.spinner("Searching for flights... This may take a few minutes."):
        request = f"flights from {origin} to {destination} on {departure_date.strftime('%Y-%m-%d')}"
        if return_date:
            request += f" returning on {return_date.strftime('%Y-%m-%d')}"
        
        try:
            results = search_flights_duckduckgo(request)
            kayak_url = kayak_search(origin, destination, departure_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d') if return_date else None)
            
            st.success("Search completed!")
            st.markdown("## Flight Results")
            st.markdown(f"🔗 **[Search Flights on Kayak]({kayak_url})**")
            
            for idx, res in enumerate(results, 1):
                st.markdown(f"**{idx}. [{res['title']}]({res['href']})**\n\n{res['body']}")
        except Exception as e:
            st.error(f"An error occurred during the search: {str(e)}")

st.markdown("---")
st.markdown("""
### About FlightFinder Pro
This application uses AI agents to search for flights and find the best deals for you.
Simply enter your origin, destination, and travel date to get started.
""")