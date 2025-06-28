import streamlit as st
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Pokémon eBay Sales (API)", layout="wide")
st.title("🔴 Live Pokémon Card Sales on eBay (via API)")

# STEP 2: Replace this with your actual eBay App ID from developer.ebay.com
EBAY_APP_ID = "AchitEnk-PokemonS-SBX-48e98c9a6-091b2ac8"

def get_ebay_sales():
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    headers = {
        "X-EBAY-SOA-OPERATION-NAME": "findCompletedItems",
        "X-EBAY-SOA-SECURITY-APPNAME": EBAY_APP_ID,
        "X-EBAY-SOA-REQUEST-DATA-FORMAT": "XML"
    }
    params = {
        "keywords": "pokemon card",
        "itemFilter.name": "SoldItemsOnly",
        "itemFilter.value": "true",
        "paginationInput.entriesPerPage": "15",
        "outputSelector": "PictureURLLarge"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        st.error(f"API request failed: {response.status_code}")
        return []

    root = ET.fromstring(response.content)
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title")
        price = item.find("sellingStatus/currentPrice").text
        url = item.findtext("viewItemURL")
        img = item.findtext("pictureURLLarge")
        items.append({
            "title": title,
            "price": price,
            "url": url,
            "img": img or ""
        })
    return items

if st.button("Load Latest Sales"):
    sales = get_ebay_sales()
    if not sales:
        st.warning("No sales found or API limit reached.")
    else:
        for sale in sales:
            st.image(sale["img"], width=150)
            st.markdown(f"**[{sale['title']}]({sale['url']})**")
            st.markdown(f"💵 ${sale['price']}")
            st.markdown("---")
else:
    st.info("Click 'Load Latest Sales' to fetch recent Pokémon card sales from eBay.")

