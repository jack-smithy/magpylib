"""
Implementations of analytical expressions for the magnetic field of
a circular current loop. Computation details in function docstrings.
"""
import warnings

import numpy as np

from magpylib._src.exceptions import MagpylibDeprecationWarning
from magpylib._src.fields.special_cel import cel_iter
from magpylib._src.input_checks import check_field_input
from magpylib._src.utility import cart_to_cyl_coordinates
from magpylib._src.utility import cyl_field_to_cart
from magpylib._src.utility import MU0


def current_circle_Bfield(
    *,
    r0: np.ndarray,
    r: np.ndarray,
    z: np.ndarray,
    i0: np.ndarray,
) -> np.ndarray:
    """
    B-field of a circular line-current loops.

    The loop lies in the z=0 plane with the coordinate origin at its center. The
    output is independent of the length units chosen for observers
    and radius. Implementation based on "Numerically stable and computationally
    efficient expression for the magnetic field of a current loop.", M.Ortner et al,
    Magnetism 2023, 3(1), 11-31

    Parameters
    ----------
    r0: ndarray, shape (n)
        Radii of loops.

    r: ndarray, shape (n)
        Radial positions of observers.

    z: ndarray, shape (n)
        Axial positions of observers.

    Returns
    -------
    B-Field: tuple, (Hr, Hz)
        B-field generated by Cylinders at observer positions in units of tesla.
    """
    n5 = len(r)

    # express through ratios (make dimensionless, avoid large/small input values, stupid)
    r = r / r0
    z = z / r0

    # field computation from paper
    z2 = z**2
    x0 = z2 + (r + 1) ** 2
    k2 = 4 * r / x0
    q2 = (z2 + (r - 1) ** 2) / x0

    k = np.sqrt(k2)
    q = np.sqrt(q2)
    p = 1 + q
    pf = k / np.sqrt(r) / q2 / 20 / r0 * 1e-6 * i0

    # cel* part
    cc = k2 * k2
    ss = 2 * cc * q / p
    Br = pf * z / r * cel_iter(q, p, np.ones(n5), cc, ss, p, q)

    # cel** part
    cc = k2 * (k2 - (q2 + 1) / r)
    ss = 2 * k2 * q * (k2 / p - p / r)
    Bz = -pf * cel_iter(q, p, np.ones(n5), cc, ss, p, q)

    return np.row_stack((Br, np.zeros(n5), Bz))
    # return Br, Bz


def BHJM_circle(
    *,
    field: str,
    observers: np.ndarray,
    diameter: np.ndarray,
    current: np.ndarray,
) -> np.ndarray:
    """
    Return BHMJ fields
    - treat special cases
    """

    # allocate result - USE SINGLE BHJM ARRAY INSTEAD OF TUPLE (SEE CYLINDER)
    # Br_tot, Bz_tot = np.zeros((2, n))
    BHJM = np.zeros_like(observers, dtype=float)

    check_field_input(field)
    if field in "MJ":
        return BHJM

    r, phi, z = cart_to_cyl_coordinates(observers)
    r0 = np.abs(diameter / 2)
    n = len(r0)

    # Special cases:
    # case1: loop radius is 0 -> return (0,0,0)
    mask1 = r0 == 0
    # case2: at singularity -> return (0,0,0)
    mask2 = np.logical_and(abs(r - r0) < 1e-15 * r0, z == 0)
    # case3: r=0
    mask3 = r == 0
    if np.any(mask3):
        mask4 = mask3 * ~mask1  # only relevant if not also case1
        BHJM[mask4, 2] = (
            0.6283185307179587e-6
            * r0[mask4] ** 2
            / (z[mask4] ** 2 + r0[mask4] ** 2) ** (3 / 2)
        ) * current[mask4]

    # general case
    mask5 = ~np.logical_or(np.logical_or(mask1, mask2), mask3)
    if np.any(mask5):
        BHJM[mask5] = current_circle_Bfield(
            r0=r0[mask5],
            r=r[mask5],
            z=z[mask5],
            i0=current[mask5],
        ).T
        # Br_gen, Bz_gen = current_circle_Bfield(r0=r0[mask5], r=r[mask5], z=z[mask5])
        # Br_tot[mask5] = Br_gen
        # Bz_tot[mask5] = Bz_gen

    # transform field to cartesian CS
    # Bx_tot, By_tot = cyl_field_to_cart(phi, Br_tot)
    BHJM[:, 0], BHJM[:, 1] = cyl_field_to_cart(phi, BHJM[:, 0])
    # B_cart = (
    #    np.concatenate(((Bx_tot,), (By_tot,), (Bz_tot,)), axis=0) * current
    # ).T  # ugly but fast

    # B or H field
    if field == "B":
        return BHJM

    return BHJM / MU0
