import streamlit as st
import magpylib as magpy
from magpylib_force import getFT

st.set_page_config(page_title="Holding Force", page_icon="🧲")


with st.sidebar:
    st.header("Holding Force")
    st.image("./docs/_static/images/magpylib_logo.png", width=150)


st.markdown("""
            # Holding force calculator
            
            This example makes use of the [magpylib-force package](https://github.com/magpylib/magpylib-force).

            With Magpylib-force it is possible to compute the holding force of a magnet attached magnetically to a soft-ferromagnetic plate. See the implementation [here](https://github.com/magpylib/magpylib-force/blob/main/magpylib_force/force.py).
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
    
    The magnetic field of a magnetic dipole moment that lies in front of a highly permeable surface is similar to the field of two dipole moments: the original one and one that is mirrored across the surface such that each "magnetic charge" that makes up the dipole moment is mirrored in both position and charge.

    Select the dimensions of the magnet, and the polarization perpendicular to the surface.
    """
)


# Create sliders for x, y, and z

st.markdown("#### Input magnet parameters")
col4, col5, col6, col7 = st.columns([1, 1, 1, 1])
with col4:
    x = st.number_input(
        "**x** (m)", value=5e-3, min_value=1e-4, step=1e-5, format="%.4f"
    )

with col5:
    y = st.number_input(
        "**y** (m)", value=2.5e-3, min_value=1e-4, step=1e-5, format="%.4f"
    )

with col6:
    z = st.number_input(
        "**z** (m)", value=1e-3, min_value=1e-5, step=1e-4, format="%.4f"
    )

with col7:
    pol = st.number_input(label="**Polarization** (T)", value=1.33)


def calculate(x, y, z, pol):
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
    result = calculate(x, y, z, pol)
    st.markdown(f"Holding Force: **{result} g**")
