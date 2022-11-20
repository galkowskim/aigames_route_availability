import streamlit as st

from app.multipage import MultiPage
from app.pages import main_page

app = MultiPage()

st.title("Route availability classification")

app.add_page('Main Page', main_page.run())

if __name__ == '__main__':
    app.run()