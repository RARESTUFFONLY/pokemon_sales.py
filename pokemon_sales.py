import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Live Pokémon eBay Sales", layout="wide")
st.title("🔴 Live Pokémon Card Sales on eBay")

st.markdown("Auto-refreshes every 30 seconds.")
st.markdown("---")

def get_sales():
    url = "https://www.ebay.com/sch/i.html?_nkw=pokemon+card&_sacat=0&LH_Sold=1&LH_Complete=1&_ipg=20"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = []
    for item in soup.select(".s-item"):
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        img = item.select_one(".s-item__image-img")
        link_tag = item.select_one("a")
        if title and price and link_tag:
            cards.append({
                "title": title.get_text(),
                "price": price.get_text(),
                "img": img["src"] if img else "",
                "url": link_tag["href"]
            })
    return cards

cards = get_sales()

for card in cards:
    st.image(card["img"], width=150)
    st.markdown(f"**[{card['title']}]({card['url']})**")
    st.markdown(f"💵 {card['price']}")
    st.markdown("---")
