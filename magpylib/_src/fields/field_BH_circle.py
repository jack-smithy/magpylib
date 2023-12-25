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


# CORE
def current_circle_field(
    *,
    field: str,
    observers: np.ndarray,
    diameter: np.ndarray,
    current: np.ndarray,
) -> np.ndarray:
    """Magnetic field of a circular (line) current loops.

    The loop lies in the z=0 plane with the coordinate origin at its center.

    SI units are used for all inputs and outputs.

    Parameters
    ----------
    field: str, default=`'B'`
        If `field='B'` return B-field in units of T, if `field='H'` return H-field
        in units of A/m.

    observers: ndarray, shape (n,3)
        Observer positions (x,y,z) in Cartesian coordinates in units of m.

    diameter: ndarray, shape (n,)
        Diameter of loop in units of m.

    current: ndarray, shape (n,)
        Electrical current in units of A.

    Returns
    -------
    B-field or H-field: ndarray, shape (n,3)
        B- or H-field of source in Cartesian coordinates in units of T or A/m.

    Examples
    --------
    Compute the field of three different circular loops at three different positions.

    >>> import numpy as np
    >>> import magpylib as magpy
    >>> H = magpy.core.current_circle_field(
    ...     field='H',
    ...     observers=np.array([(0,0,0), (1,1,1), (2,2,2)]),
    ...     diameter=np.array([1,2,3]),
    ...     current=np.array([1,1,2])
    ... )
    >>> print(H)
    [[0.         0.         1.        ]
     [0.0496243  0.0496243  0.02124542]
     [0.02833835 0.02833835 0.00654999]]

    Notes
    -----
    Advanced unit use: The input unit of magnetization and polarization
    gives the output unit of H and B. All results are independent of the
    length input units. One must be careful, however, to use consistently
    the same length unit throughout a script.

    Implementation based on "Numerically stable and computationally efficient expression for
    the magnetic field of a current loop.", M.Ortner et al, Submitted to MDPI Magnetism, 2022
    """

    check_field_input(field)
    if field in "MJ":
        return np.zeros_like(observers)

    r, phi, z = cart_to_cyl_coordinates(observers)
    r0 = np.abs(diameter / 2)
    n = len(r0)

    # allocate result
    Br_tot, Bz_tot = np.zeros((2, n))

    # Special cases:
    # case1: loop radius is 0 -> return (0,0,0)
    mask1 = r0 == 0
    # case2: at singularity -> return (0,0,0)
    mask2 = np.logical_and(abs(r - r0) < 1e-15 * r0, z == 0)
    # case3: r=0
    mask3 = r == 0
    if np.any(mask3):
        mask4 = mask3 * ~mask1  # only relevant if not also case1
        Bz_tot[mask4] = (
            0.6283185307179587
            * r0[mask4] ** 2
            / (z[mask4] ** 2 + r0[mask4] ** 2) ** (3 / 2)
        )

    # general case
    mask5 = ~np.logical_or(np.logical_or(mask1, mask2), mask3)
    if np.any(mask5):
        r0 = r0[mask5]
        r = r[mask5]
        z = z[mask5]
        n5 = len(r0)

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
        pf = k / np.sqrt(r) / q2 / 20 / r0

        # cel* part
        cc = k2 * k2
        ss = 2 * cc * q / p
        Br_tot[mask5] = pf * z / r * cel_iter(q, p, np.ones(n5), cc, ss, p, q)

        # cel** part
        cc = k2 * (k2 - (q2 + 1) / r)
        ss = 2 * k2 * q * (k2 / p - p / r)
        Bz_tot[mask5] = -pf * cel_iter(q, p, np.ones(n5), cc, ss, p, q)

    # transform field to cartesian CS
    Bx_tot, By_tot = cyl_field_to_cart(phi, Br_tot)
    B_cart = (
        np.concatenate(((Bx_tot,), (By_tot,), (Bz_tot,)), axis=0) * current * 1e-6
    ).T  # ugly but fast

    # B or H field
    if field == "B":
        return B_cart

    return B_cart / MU0


def current_loop_field(*args, **kwargs):
    """current_loop_field is deprecated, see current_circle_field"""

    warnings.warn(
        (
            "current_loop_field is deprecated and will be removed in a future version, "
            "use current_circle_field instead."
        ),
        MagpylibDeprecationWarning,
        stacklevel=2,
    )
    return current_circle_field(*args, **kwargs)
