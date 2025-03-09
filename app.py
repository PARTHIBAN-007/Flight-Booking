import sys
import datetime
import streamlit as st
import os
from langchain.tools import Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from dotenv import load_dotenv

st.set_page_config(page_title="✈️ FlightFinder Pro", layout="wide")

st.markdown("<h1 style='color: #0066cc;'>✈️ FlightFinder Pro</h1>", unsafe_allow_html=True)
st.subheader("Powered by DuckDuckGo and LangChain")

with st.sidebar:
    st.header("Search Configuration")
    st.markdown("DuckDuckGo is being used for searches, no API key required.")

load_dotenv()

st.header("Search for Flights")
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin City (IATA Code)", "SFO")
    departure_date = st.date_input("Departure Date", datetime.date.today() + datetime.timedelta(days=30))

with col2:
    destination = st.text_input("Destination City (IATA Code)", "JFK")
    return_date = st.date_input("Return Date (Optional)", datetime.date.today() + datetime.timedelta(days=37))

search_button = st.button("Search Flights")

# Kayak Search Tool
def kayak_search(departure: str, destination: str, date: str, return_date: str = None) -> str:
    """
    """
    url = f"https://www.kayak.com/flights/{departure}-{destination}/{date}"
    if return_date:
        url += f"/{return_date}"
    url += "?currency=USD"
    return url

kayak_tool = Tool(
    name="Kayak Search",
    func=kayak_search,
    description="Generates a Kayak search URL for flights."
)

ddg_search = DuckDuckGoSearchAPIWrapper()
ddg_tool = Tool(
    name="DuckDuckGo Search",
    func=ddg_search.run,
    description="Searches for flight information using DuckDuckGo."
)

if search_button:
    with st.spinner("Searching for flights... This may take a few minutes."):
        request = f"flights from {origin} to {destination} on {departure_date.strftime('%Y-%m-%d')}"
        if return_date:
            request += f" returning on {return_date.strftime('%Y-%m-%d')}"
        
        try:
            results = ddg_tool.run(request)
            kayak_url = kayak_tool.run(origin, destination, departure_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d') if return_date else None)
            
            st.success("Search completed!")
            st.markdown("## Flight Results")
            st.markdown(f"🔗 **[Search Flights on Kayak]({kayak_url})**")
            
            if isinstance(results, list):
                for idx, res in enumerate(results[:5], 1):
                    st.markdown(f"**{idx}. [{res['title']}]({res['href']})**\n\n{res['body']}")
            else:
                st.markdown(f"🔎 {results}")
        except Exception as e:
            st.error(f"An error occurred during the search: {str(e)}")

st.markdown("---")
st.markdown("""
### About FlightFinder Pro
This application uses AI tools to search for flights and find the best deals for you.
Simply enter your origin, destination, and travel date to get started.
""")