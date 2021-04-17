import numpy as np
from matplotlib.patches import Ellipse


def show_vector(ax, start, end, label, color=None, **kwargs):
    lines = ax.plot(end[0], end[1], "o", label=label, color=color, **kwargs)
    if color is None:
        color = lines[0].get_color()
    ax.arrow(
        start[0],
        start[1],
        end[0] - start[0],
        end[1] - start[1],
        head_width=0.1,
        width=0.02,
        overhang=0.2,
        length_includes_head=True,
        color=color,
        **kwargs
    )


def show_normed_vects(ax, vects, norm=2):
    unit_vects = (
        vects.T / np.linalg.norm(vects, norm, axis=1)
    ).T  # a random unit vector

    for a1, b1 in zip(vects, unit_vects):
        ax.plot(
            [a1[0], b1[0]], [a1[1], b1[1]], linestyle="dotted", color="black", lw=0.5
        )

    ax.scatter(vects[:, 0], vects[:, 1], s=5)
    ax.scatter(unit_vects[:, 0], unit_vects[:, 1], s=5, color="green")
    ax.plot([0], [0], ".", color="red")

    ax.set_ylim((-3, 3))
    ax.set_xlim((-3, 3))
    ax.set_aspect(1.0)


def eigsorted(cov):
    vals, vects = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vects[:, order]


def draw_covariance_ellipse(ax, x, n_std):
    cov = np.cov(x.T)
    vals, vects = eigsorted(cov)
    angle = np.degrees(np.arctan2(*vects[:, 0][::-1]))
    width, height = 2 * n_std * np.sqrt(vals)
    ellipse = Ellipse(
        xy=(x[:, 0].mean(), x[:, 1].mean()),
        width=width,
        height=height,
        edgecolor="black",
        facecolor="none",
        angle=angle,
    )

    ax.add_artist(ellipse)
