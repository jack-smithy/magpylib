import streamlit as st
import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Field Calculation", page_icon="🧲")

st.markdown("""# Streamplot Visualisation""")


st.sidebar.header("Field Line Visualisation")

with st.sidebar:
    st.image("./docs/_static/images/magpylib_logo.png", width=150)
    with st.expander("Advanced"):
        pol = st.number_input(label="Polarisation (z-direction)", value=500)

# Create sliders for x, y, and z

st.markdown("""
In this example we show the B-field of a cuboid magnet using Matplotlib streamlines. 
            
Streamlines are not magnetic field lines in the sense that the field amplitude cannot be derived from their density. However, Matplotlib streamlines can show the field amplitude via color and line thickness. One must be careful that streamlines can only display two components of the field (x and z in this case). In the following example the third field component is always zero - but this is generally not the case.
""")

st.markdown("#### Input magnet dimensions (m)")
x = st.number_input("**x**", value=2.0, min_value=1e-2, max_value=4.5, step=1e-2)
z = st.number_input("**z**", value=2.0, min_value=1e-2, max_value=4.5, step=1e-2)


def calculate(x, z, pol):
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Create an observer grid in the xz-symmetry plane
    ts = np.linspace(-5, 5, 40)
    grid = np.array([[(x, 0, z) for x in ts] for z in ts])
    X, _, Z = np.moveaxis(grid, 2, 0)

    # Compute the B-field of a cube magnet on the grid
    cube = magpy.magnet.Cuboid(polarization=(pol, 0, pol), dimension=(x, 2, z))
    B = cube.getB(grid)
    Bx, _, Bz = np.moveaxis(B, 2, 0)
    log10_norm_B = np.log10(np.linalg.norm(B, axis=2))

    # Display the B-field with streamplot using log10-scaled
    # color function and linewidth
    splt = ax.streamplot(
        X,
        Z,
        Bx,
        Bz,
        density=1.5,
        color=log10_norm_B,
        linewidth=log10_norm_B,
        cmap="autumn",
    )

    # Add colorbar with logarithmic labels
    fig.colorbar(splt.lines, ax=ax, label="|B| (mT)")
    # Outline magnet boundary
    ax.plot(
        [x / 2, x / 2, -x / 2, -x / 2, x / 2],
        [z / 2, -z / 2, -z / 2, z / 2, z / 2],
        "k--",
        lw=2,
    )

    # Figure styling
    ax.set(
        xlabel="x-position (mm)",
        ylabel="z-position (mm)",
    )

    plt.tight_layout()
    st.pyplot(fig)


# Create a button to trigger the calculation
if st.button("Calculate"):
    result = calculate(x, z, pol)
