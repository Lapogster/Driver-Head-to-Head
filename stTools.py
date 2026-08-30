import streamlit as st

# Update empty text object to match loading info
def loadingText(text, loadText):
    loadText.text(text)

# Change page to new page, documenting previous history
def setPage(newPage):
    st.session_state.pageHistory.append(st.session_state.page)
    st.session_state.page = newPage

# Universal back button for use on any page, uses page history
def backButton():
    if st.session_state.pageHistory == []:
        st.session_state.pageHistory.append("home")

    if st.button(f"Return to {st.session_state.pageHistory[-1]}", type='primary'):
        st.session_state.page = st.session_state.pageHistory[-1]
        st.session_state.pageHistory.pop()

        st.rerun()

# Render a profile picture
def renderNamePFP(image, name):
    with st.container(horizontal=True):

        print(image)

        if image == False:
            image = "Assets\\missingIcon.png"

        st.image(image, width=25)
        st.text(name)

# Render text in the center of the container
def betterText(text):
    st.markdown(f"<p style='text-align: center;'>{text}</p>", unsafe_allow_html=True)