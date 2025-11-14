import streamlit as st

st.set_page_config(
    page_title="langchain-study",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title(
    body="🦜 The LangChain Study Repo",
)
st.caption(body=("by Anurag Ravi Nimonkar (Nimo)"))

_add_vertical_space = lambda: st.write("")


def add_space(num_of_lines: int):
    for _ in range(num_of_lines):
        _add_vertical_space()


st.divider()

add_space(2)

buffer_column_1, introduction, buffer_column_2 = st.columns(
    spec=[1, 2, 1],
)

with introduction:

    if st.button(
        label="I want to explore",
        help="Click me to start configuring the environment and use the assistants",
        icon="☃️",
        type="secondary",
        use_container_width=True,
    ):
        st.switch_page(f"pages/_⚙️_setting_up_your_environment.py")

    if st.button(
        label="I want to learn more",
        help="Click me to learn more about why this repo even exists",
        icon="📚",
        type="secondary",
        use_container_width=True,
    ):
        with open("frontend/README.md", encoding="utf-8", mode="r") as f:
            learn_more_content = f.read()

        st.markdown(
            body=learn_more_content,
        )
