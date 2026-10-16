import re
import streamlit as st

from src.recommendation_engine import RecommendationEngine


st.set_page_config(
    page_title="Smart Product Recommendations",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Smart Product Recommendations")

query = st.text_input(
    "What are you looking for?",
    value="I need a laptop under 70000"
)

if st.button("Get Recommendations", type="primary"):
    price_match = re.search(
        r"(?:under|below|less than|within)\s*₹?\s*([\d,]+)",
        query.lower()
    )

    max_price = (
        float(price_match.group(1).replace(",", ""))
        if price_match else None
    )

    with st.spinner("Finding recommendations..."):
        engine = RecommendationEngine()
        result = engine.recommend(query, max_price=max_price)

    main_product = result["main_product"]
    recommendations = result["recommendations"]

    if main_product:
        st.subheader("Your Best Match")
        st.markdown(f"### {main_product['name']}")
        st.markdown(f"**Price: ₹{main_product['price']:,.0f}**")
        st.write(main_product["description"])

        st.divider()
        st.subheader("✨ You May Also Like")

        if recommendations:
            columns = st.columns(len(recommendations))

            for column, product in zip(columns, recommendations):
                with column:
                    st.markdown(f"**{product['name']}**")
                    st.write(f"₹{product['price']:,.0f}")
                    st.write(product["description"])
        else:
            st.info("No additional relevant products found.")
    else:
        st.warning("No matching products found in the catalog.")