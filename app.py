import requests
import streamlit as st

API_URL = "https://stock-api-syp8.onrender.com"

CANDIDATE_PATHS = ["/predict/live", "/predict", "/live", "/predict_live"]

st.title("Stock Next-Close Predictor")

symbol = st.text_input("Stock symbol", "TSLA").strip().upper()


def call_api(path):
    return requests.get(
        API_URL + path,
        params={"symbol": symbol},
        timeout=90,
    )


if st.button("Predict next close"):
    r = None
    used_path = None
    try:
        with st.spinner("Fetching prediction..."):
            for path in CANDIDATE_PATHS:
                r = call_api(path)
                if r.status_code != 404:
                    used_path = path
                    break

        if used_path is None:
            st.error("No matching endpoint found.")
            st.write("Open " + API_URL + "/docs and find the prediction path.")
        elif r.status_code == 429:
            st.error("Rate limit reached. Try again later.")
        else:
            r.raise_for_status()
            data = r.json()
            st.caption("Endpoint used: " + used_path)

            if "predicted_next_close" in data:
                value = data["predicted_next_close"]
                st.metric("Predicted next close", round(value, 2))
            else:
                st.warning("Unexpected response format:")
                st.json(data)

    except requests.exceptions.Timeout:
        st.error("The API took too long to respond.")
    except requests.exceptions.HTTPError as e:
        st.error("API returned an error: " + str(e))
        try:
            st.json(r.json())
        except Exception:
            pass
    except requests.exceptions.RequestException as e:
        st.error("Could not reach the API: " + str(e))
    except ValueError:
        st.error("The API did not return valid JSON.")
