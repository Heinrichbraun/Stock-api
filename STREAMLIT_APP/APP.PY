import requests
import streamlit as st

API_URL = "https://your-service.onrender.com"  # replace with your real Render URL (no brackets)

symbol = st.text_input("Stock symbol", "TSLA").strip().upper()

if st.button("Predict next close"):
    try:
        with st.spinner("Fetching prediction..."):
            r = requests.get(
                f"{API_URL}/predict/live",
                params={"symbol": symbol},
                timeout=60,  # Render free tier can take ~50s to wake up
            )
            r.raise_for_status()
            data = r.json()

        st.metric("Predicted next close", f"${data['predicted_next_close']:.2f}")

    except requests.exceptions.Timeout:
        st.error("The API took too long to respond. Try again in a moment.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API returned an error: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the API: {e}")
    except (KeyError, ValueError, TypeError):
        st.error("Unexpected response format from the API.")
