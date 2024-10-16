import streamlit as st
import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

st.set_page_config(page_title="Field Calculation", page_icon="🧲", layout="wide")

st.markdown("""# Streamplot Visualisation""")


st.sidebar.header("Field Line Visualisation")

with st.sidebar:
    st.image("./docs/_static/images/magpylib_logo.png", width=150)

# Create sliders for x, y, and z

st.markdown("""
In this example we show the B-field of a cuboid magnet using Matplotlib streamlines. 
            
Streamlines are not magnetic field lines in the sense that the field amplitude cannot be derived from their density. However, Matplotlib streamlines can show the field amplitude via color and line thickness. One must be careful that streamlines can only display two components of the field (x and z in this case). 
In the following example, the side lengths **(a,b,c)** of a cubiod, and polarisation of the magnet can be selected, and a streamplot of the B-field is shown at y=0. 
""")

magnet = None

inputs, plot, nums = st.columns([1, 1, 1])

with inputs:
    st.markdown("#### Input magnet dimensions")
    colx, coly, colz = st.columns([1, 1, 1])
    with colx:
        x_dim = st.number_input(
            "**a** (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    with coly:
        y_dim = st.number_input(
            "**b** (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    with colz:
        z_dim = st.number_input(
            "**c** (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    st.markdown("#### Input magnet polarization")
    col_polx, col_poly, col_polz = st.columns([1, 1, 1])
    with col_polx:
        x_pol = st.number_input(
            "**x** polarization (T)",
            value=300,
            min_value=0,
            max_value=500,
            step=1,
        )

    with col_poly:
        y_pol = st.number_input(
            "**y** polarization (T)",
            value=300,
            min_value=0,
            max_value=500,
            step=1,
        )

    with col_polz:
        z_pol = st.number_input(
            "**z** polarization (T)",
            value=300,
            min_value=0,
            max_value=500,
            step=1,
        )

    magnet = magpy.magnet.Cuboid(
        polarization=(x_pol, y_pol, z_pol),
        dimension=(x_dim, y_dim, z_dim),
    )


def calculate(magnet, dim):
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Create an observer grid in the xz-symmetry plane
    ts = np.linspace(-5, 5, 40)
    grid = np.array([[(x, 0, z) for x in ts] for z in ts])
    X, _, Z = np.moveaxis(grid, 2, 0)

    # Compute the B-field of a cube magnet on the grid
    B = magnet.getB(grid)
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
        cmap="spring_r",
    )

    # Add colorbar with logarithmic labels
    fig.colorbar(splt.lines, ax=ax, label="log10(|B|) (mT)")
    # Outline magnet boundary
    x_dim, _, z_dim = dim
    ax.plot(
        [x_dim / 2, x_dim / 2, -x_dim / 2, -x_dim / 2, x_dim / 2],
        [z_dim / 2, -z_dim / 2, -z_dim / 2, z_dim / 2, z_dim / 2],
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


with plot:
    if magnet is not None:
        calculate(magnet, dim=(x_dim, y_dim, z_dim))

with nums:
    st.markdown("#### Calculate field point")
    colx, coly, colz = st.columns([1, 1, 1])
    with colx:
        x_pos = st.number_input(
            "**x** position (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    with coly:
        y_pos = st.number_input(
            "**y** position (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    with colz:
        z_pos = st.number_input(
            "**z** position (m)",
            value=2.0,
            min_value=1e-2,
            max_value=4.5,
            step=1e-2,
        )

    if st.button("Calculate"):
        bx, by, bz = magnet.getB([x_pos, y_pos, z_pos])
        st.markdown(
            f"Magnetic field at ({x_pos}, {y_pos}, {z_pos}) = **({round(bx, 2)}T, {round(by, 2)}T, {round(bz, 2)}T)**"
        )
