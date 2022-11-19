import streamlit as st

from app.multipage import MultiPage
from app.pages import main_page, map_page

app = MultiPage()

st.title("STARTER")

app.add_page('Main Page', main_page.run())
# app.add_page('Map Page', map_page.run())


if __name__ == '__main__':
    app.run()