import streamlit as st
import magpylib as magpy
from magpylib_force import getFT

st.title("Holding force calculator")

with st.sidebar:
    st.image("docs/_static/images/magpylib_logo.png", width=150)

    with st.expander("Advanced"):
        pol = st.number_input(label="Polarisation (z-direction)", value=1.33)

# Create sliders for x, y, and z

st.write("Input magnet dimensions (m)")
x = st.number_input("x", value=5e-3, min_value=1e-5, step=1e-5, format="%.5f")
y = st.number_input("y", value=2.5e-3, min_value=1e-5, step=1e-5, format="%.5f")
z = st.number_input("z", value=1e-3, min_value=1e-5, step=1e-5, format="%.5f")


def calculate(x, y, z):
    # Target magnet
    m1 = magpy.magnet.Cuboid(
        dimension=(x, y, z),
        polarization=(0, 0, pol),
    )
    m1.meshing = (10, 5, 2)  # type: ignore

    # Mirror magnet
    m2 = m1.copy(position=(0, 0, 1e-3))

    F, _ = getFT(m2, m1)
    return round(F[2] * 100, 2)


# Create a button to trigger the calculation
if st.button("Calculate"):
    result = calculate(x, y, z)
    st.write(f"Holding Force: {result} g")
