import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Live Pokémon eBay Sales", layout="wide")
st.title("🔴 Live Pokémon Card Sales on eBay")

st.markdown("Click the button below to load the latest sales.")

def get_sales():
    url = "https://www.ebay.com/sch/i.html?_nkw=pokemon+card&_sacat=0&LH_Sold=1&LH_Complete=1&_ipg=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    cards = []
    for item in soup.select("li.s-item"):
        title = item.select_one("h3.s-item__title")
        price = item.select_one(".s-item__price")
        img = item.select_one(".s-item__image-img")
        link_tag = item.select_one("a.s-item__link")
        if title and price and link_tag:
            cards.append({
                "title": title.get_text(),
                "price": price.get_text(),
                "img": img["src"] if img else "",
                "url": link_tag["href"]
            })
    return cards

if st.button("Load Latest Sales"):
    cards = get_sales()

    if not cards:
        st.warning("No sales found or failed to fetch data.")
    else:
        st.write(f"Found {len(cards)} sales:")
        for card in cards:
            st.image(card["img"], width=150)
            st.markdown(f"**[{card['title']}]({card['url']})**")
            st.markdown(f"💵 {card['price']}")
            st.markdown("---")
else:
    st.info("Click 'Load Latest Sales' to get the newest Pokémon card sales.")
