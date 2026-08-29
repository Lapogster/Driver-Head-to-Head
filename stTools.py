import streamlit as st

def loadingText(text, loadText):
    loadText.text(text)

def setPage(newPage):
    st.session_state.pageHistory.append(st.session_state.page)
    st.session_state.page = newPage

def backButton():
    if st.session_state.pageHistory == []:
        st.session_state.pageHistory.append("home")

    if st.button(f"Return to {st.session_state.pageHistory[-1]}"):
        st.session_state.page = st.session_state.pageHistory[-1]
        st.session_state.pageHistory.pop()

        st.rerun()

def renderNamePFP(image, name):
    with st.container(horizontal=True):

        print(image)

        if image == False:
            image = "Assets\\missingIcon.png"

        st.image(image, width=25)
        st.text(name)