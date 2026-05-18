import streamlit as st
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Live News Dashboard",
    page_icon="📰",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("📰 Live News Dashboard")

st.write("Latest real-time news updates")

# ---------------- API KEY ---------------- #

API_KEY = "API_KEY"

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("🔎 News Filters")

category = st.sidebar.selectbox(
    "Select Category",
    [
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

country_dict = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca"
}

country_name = st.sidebar.selectbox(
    "Select Country",
    list(country_dict.keys())
)

country = country_dict[country_name]

search_query = st.sidebar.text_input(
    "Search News"
)

# ---------------- API URL ---------------- #

# ---------------- API URL ---------------- #

if search_query:

    url = (
        f"https://newsdata.io/api/1/news?"
        f"apikey={API_KEY}&"
        f"q={search_query}&"
        f"language=en"
    )

else:

    url = (
        f"https://newsdata.io/api/1/news?"
        f"apikey={API_KEY}&"
        f"country={country}&"
        f"category={category}&"
        f"language=en"
    )
# ---------------- FETCH NEWS ---------------- #

try:

    response = requests.get(url)

    news_data = response.json()

    # ---------------- ERROR CHECK ---------------- #

    if news_data.get("status") == "error":

        st.error(
            news_data.get(
                "results",
                "Failed to fetch news"
            )
        )

    else:

        articles = news_data.get("results", [])

        # ---------------- LOAD MORE ---------------- #

        next_page = news_data.get("nextPage")

        if next_page:

            if st.button("Load More News"):

                more_url = (
                    f"https://newsdata.io/api/1/news?"
                    f"apikey={API_KEY}&"
                    f"country={country}&"
                    f"category={category}&"
                    f"language=en&"
                    f"page={next_page}"
                )

                more_response = requests.get(more_url)

                more_data = more_response.json()

                more_articles = more_data.get("results", [])

                articles.extend(more_articles)
                
        st.success(
            f"Total Articles Found: {len(articles)}"
        )

        # ---------------- DISPLAY NEWS ---------------- #

        for article in articles:

            st.markdown("---")

            # Title
            st.markdown(
                f"""
                <h2 style="
                    font-size:38px;
                    font-weight:bold;
                ">
                {article.get("title", "No Title")}
                </h2>
                """,
                unsafe_allow_html=True
            )

            # Image
            if article.get("image_url"):

                st.image(
                article["image_url"],
                width=500
            )

            # Description
            st.markdown(
                f"""
                <div style="
                    font-size:20px;
                    line-height:1.8;
                    font-weight:500;
                ">
                {article.get("description", "No Description Available")}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Source
            st.write(
                "📰 Source:",
                article.get(
                    "source_id",
                    "Unknown"
                )
            )

            # Published Date
            st.write(
                "📅 Published At:",
                article.get(
                    "pubDate",
                    "N/A"
                )
            )

            # Read More
            st.markdown(
                f"[🔗 Read Full Article]({article.get('link', '#')})"
            )

except Exception as e:

    st.error(f"Error: {e}")
