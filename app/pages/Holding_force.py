import streamlit as st
import magpylib as magpy
from magpylib_force import getFT

st.set_page_config(page_title="Holding Force", page_icon="🧲")


with st.sidebar:
    st.header("Holding Force")
    st.image("./docs/_static/images/magpylib_logo.png", width=150)

    with st.expander("Advanced"):
        pol = st.number_input(label="Polarisation (z-direction)", value=1.33)

st.markdown("""
            # Holding force calculator
            
            This example makes use of the [magpylib-force package](https://github.com/magpylib/magpylib-force).

            With Magpylib-force it is possible to compute the holding force of a magnet attached magnetically to a soft-ferromagnetic plate. See the implementation [here](https://github.com/magpylib/magpylib-force/blob/main/magpylib_force/force.py)
            """)

col1, col2, col3 = st.columns([3, 6, 2])

with col2:
    st.image(
        "./docs/_static/images/examples_force_haftkraft.png",
        width=250,
        caption="Sketch of holding force F that must be overcome to detach the magnet from a soft-magnetic plate.",
    )

st.markdown(
    """
    For this we make use of the "magnetic mirror" effect, which is quite similar to the well-known electrostatic "mirror-charge" model. 
    
    The magnetic field of a magnetic dipole moment that lies in front of a highly permeable surface is similar to the field of two dipole moments: the original one and one that is mirrored across the surface such that each "magnetic charge" that makes up the dipole moment is mirrored in both position and charge."""
)


# Create sliders for x, y, and z

st.markdown("#### Input magnet dimensions (m)")
x = st.number_input("**x**", value=5e-3, min_value=1e-5, step=1e-5, format="%.5f")
y = st.number_input("**y**", value=2.5e-3, min_value=1e-5, step=1e-5, format="%.5f")
z = st.number_input("**z**", value=1e-3, min_value=1e-5, step=1e-5, format="%.5f")


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
    st.markdown(f"Holding Force: **{result} g**")
