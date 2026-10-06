import requests
import streamlit as st

# 1. Replace with your real Render URL (copy it from the Render dashboard).
#    No square brackets, no trailing slash.
API_URL = "https://stock-api-x7k2.onrender.com"

st.title("Stock Next-Close Predictor")

symbol = st.text_input("Stock symbol", "TSLA").strip().upper()

if st.button("Predict next close"):
    try:
        with st.spinner("Fetching prediction (the first request can take up to a minute)..."):
            r = requests.get(
                f"{API_URL}/predict/live",
                params={"symbol": symbol},
                timeout=90,
            )

        if r.status_code == 429:
            st.error("Rate limit reached. Please try again later.")
        else:
            r.raise_for_status()
            data = r.json()
            st.metric("Predicted next close", data["predicted_next_close"])

    except requests.exceptions.InvalidURL:
        st.error("API_URL is not a valid address. Check that you replaced the placeholder with your real Render URL.")
    except requests.exceptions.Timeout:
        st.error("The API took too long to respond. Try again in a moment.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API returned an error: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the API: {e}")
    except KeyError:
        st.error(f"Unexpected response from the API: {data}")
    except ValueError:
        st.error("The API did not return valid JSON.")
