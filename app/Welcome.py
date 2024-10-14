import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.markdown(
    """
    <style>
    .full-height {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }

    .top-gap {
        margin-top: 32px;
    }

    .sub-text {
        color: gray; 
        text-align: center;
        width: 100%;
    }

    .centered-content {
        display: flex;
        width: "100%";
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .small-header {
        font-size: 16px;
        color: #FF4B4B;
        margin-top: 128px;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 8])

with col1:
    st.image("./docs/_static/images/magpylib_logo.png", use_column_width=True)

with col3:
    st.markdown("# Magpylib Calculator")

with st.sidebar:
    st.header("Welcome")
    st.image("./docs/_static/images/magpylib_logo.png", width=150)
    st.success("Select a demo above.")

st.markdown('<div class="top-gap"></div>', unsafe_allow_html=True)

st.image("./docs/_static/images/index_flowchart.png", use_column_width=True)

st.markdown('<div class="top-gap"></div>', unsafe_allow_html=True)

st.markdown(
    """
    Magpylib is an open-source Python package for calculating static magnetic fields of magnets, currents, and other sources. 
    It uses analytical expressions, solutions to macroscopic magnetostatic problems, implemented in vectorized form which makes the computation extremely fast and leverages the open-source Python ecosystem for spectacular visualizations!

    This app provides an way of using **magpylib** functionality directly in your browser without having to write any python code.

    The documentation for Magpylib can be found [here](https://magpylib.readthedocs.io/en/latest/)
"""
)
