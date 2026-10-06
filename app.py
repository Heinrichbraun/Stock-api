import requests
import streamlit as st

API_URL = "https://stock-api-syp8.onrender.com"

# Paths to try, in order. The first one that doesn't return 404 is used.
CANDIDATE_PATHS = ["/predict/live", "/predict", "/live", "/predict_live"]

st.title("Stock Next-Close Predictor")

symbol = st.text_input("Stock symbol", "TSLA").strip().upper()


def call_api(path):
    return requests.get(
        f"{API_URL}{path}",
        params={"symbol": symbol},
        timeout=90,
    )


if st.button("Predict next close"):
    try:
        with st.spinner("Fetching prediction (the first request can take up to a minute)..."):
            r = None
            used_path = None
            for path in CANDIDATE_PATHS:
                r = call_api(path)
                if r.status_code != 404:
                    used_path = path
                    break

        if used_path is None:
            st.error(
                "None of the guessed endpoints exist. Open "
                f"{API_URL}/docs in your browser, find the prediction route, "
                "and put its path in CANDIDATE_PATHS."
            )
        elif r.status_code == 429:
            st.error("Rate limit reached. Please try again later.")
        else:
            r.raise_for_status()
            data = r.json()
            st.caption(f"Endpoint used: {used_path}")

            if "predicted_next_close" in data:
                st.metric("Predicted next close", f"${data['predicted_next_close']:.2f}")
            else:
                st.warning("The response has a different format than expected:")
                st.json(data)

    except requests.exceptions.Timeout:
        st.error("The API took too long to respond. Try again in
