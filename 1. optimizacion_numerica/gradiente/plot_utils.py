from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from pathlib import Path


def evaluate_on_grid(f, X1, X2):
    try:
        Z = f(np.array([X1, X2]))
        Z = np.asarray(Z)
        if Z.ndim == 2:
            return Z
    except Exception:
        pass

    return np.vectorize(lambda a, b: f(np.array([a, b], dtype=float)))(X1, X2)


def plot_function_course_style(
    f,
    x1_range,
    x2_range,
    title="Function Plot",
    x1_point=None,
    x2_point=None,
    grid_size=300,
    elev=35,
    azim=45,
    cmap="inferno",
    contour_mode="log",
    special_case=None,
    point_label="Punto",
    point_color="cyan",
    output_path: str | Path | None = None,
    dpi: int = 200,
):
    x1 = np.linspace(x1_range[0], x1_range[1], grid_size)
    x2 = np.linspace(x2_range[0], x2_range[1], grid_size)
    X1, X2 = np.meshgrid(x1, x2)
    Z = evaluate_on_grid(f, X1, X2).astype(float)

    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(121, projection="3d")
    ax1.plot_surface(X1, X2, Z, cmap=cmap, edgecolor="none", alpha=0.92)
    ax1.set_title(f"3D Plot of {title}")
    ax1.set_xlabel("X1")
    ax1.set_ylabel("X2")
    ax1.set_zlabel("Z")
    ax1.view_init(elev=elev, azim=azim)

    case_name = (special_case or title or "").strip().lower().replace("-", "_").replace(" ", "_")
    if case_name == "rosenbrock":
        z_cap = np.percentile(Z, 98)
        if np.isfinite(z_cap) and z_cap > 0:
            ax1.set_zlim(0, z_cap)
        else:
            z_cap = float(np.max(Z)) if np.max(Z) > 0 else 1.0
    else:
        z_cap = float(np.max(Z)) if np.max(Z) > 0 else 1.0

    if x1_point is not None and x2_point is not None:
        z_point = float(f(np.array([x1_point, x2_point], dtype=float)))

        if case_name == "rosenbrock":
            z_mark = min(z_point + 0.12 * z_cap, z_cap)
            if z_mark <= z_point:
                z_mark = z_point + max(0.05 * z_cap, 1.0)

            ax1.plot(
                [x1_point, x1_point],
                [x2_point, x2_point],
                [z_point, z_mark],
                color=point_color,
                linewidth=2,
            )
            ax1.scatter(
                [x1_point],
                [x2_point],
                [z_mark],
                color=point_color,
                s=120,
                edgecolors="white",
                linewidths=1.5,
                depthshade=False,
                label=point_label,
            )
        else:
            ax1.scatter(
                [x1_point],
                [x2_point],
                [z_point],
                color=point_color,
                s=70,
                edgecolors="white",
                linewidths=1.0,
                depthshade=False,
                label=point_label,
            )
        ax1.legend()

    ax2 = fig.add_subplot(122)

    if contour_mode == "log":
        positive_values = Z[Z > 0]
        z_min = max(float(np.min(positive_values)) if positive_values.size else 1e-6, 1e-6)
        z_max = max(float(np.max(Z)), z_min * 10)
        levels = np.logspace(np.log10(z_min), np.log10(z_max), 30)
        heat = ax2.contourf(X1, X2, Z, levels=levels, cmap=cmap, norm=LogNorm(vmin=z_min, vmax=z_max))
        ax2.contour(X1, X2, Z, levels=levels, colors="white", linewidths=0.6, alpha=0.5)
    else:
        levels = 30
        heat = ax2.contourf(X1, X2, Z, levels=levels, cmap=cmap)
        ax2.contour(X1, X2, Z, levels=levels, colors="white", linewidths=0.4, alpha=0.5)

    if x1_point is not None and x2_point is not None:
        ax2.scatter(
            [x1_point],
            [x2_point],
            color=point_color,
            edgecolor="black",
            s=70,
            label=point_label,
            zorder=10,
        )
        ax2.legend()

    contour_title = "Heatmap + Contours" if contour_mode == "log" else "Contour Plot"
    ax2.set_title(f"{contour_title} of {title}")
    ax2.set_xlabel("X1")
    ax2.set_ylabel("X2")
    fig.colorbar(heat, ax=ax2)

    plt.tight_layout()
    if output_path is not None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destination, dpi=dpi, bbox_inches="tight")
    plt.show()
    plt.close(fig)


def _plot_histogram_triptych(
    runs_df,
    *,
    value_column: str,
    sample_sizes: list[int],
    title_prefix: str,
    xlabel: str,
    color: str,
    bins: int = 20,
    figsize: tuple[int, int] = (18, 4),
):
    fig, axes = plt.subplots(1, len(sample_sizes), figsize=figsize, sharey=True)
    if len(sample_sizes) == 1:
        axes = [axes]

    for ax, n_count in zip(axes, sample_sizes):
        subset = runs_df[runs_df["n_corridas_archivo"] == n_count].copy()
        ax.hist(subset[value_column].astype(float), bins=bins, color=color, edgecolor="white")
        ax.set_title(f"n = {n_count}")
        ax.set_xlabel(xlabel)
        ax.grid(axis="y", alpha=0.25)

    axes[0].set_ylabel("Frecuencia")
    fig.suptitle(title_prefix, fontsize=14)
    fig.tight_layout()
    fig.subplots_adjust(top=0.82)
    return fig


def plot_final_value_histogram(
    runs_df,
    *,
    function_label: str,
    dimension_label: str,
    sample_sizes: list[int] | None = None,
    bins: int = 20,
):
    return _plot_histogram_triptych(
        runs_df,
        value_column="valor_final",
        sample_sizes=sample_sizes or [100, 500, 1000],
        title_prefix=f"Figura A: histograma de solucion final en {function_label} {dimension_label}",
        xlabel="Valor final",
        color="#4c78a8",
        bins=bins,
        figsize=(18, 4.5),
    )


def plot_evaluations_histogram(
    runs_df,
    *,
    function_label: str,
    dimension_label: str,
    sample_sizes: list[int] | None = None,
    bins: int = 20,
):
    return _plot_histogram_triptych(
        runs_df,
        value_column="evaluaciones",
        sample_sizes=sample_sizes or [100, 500, 1000],
        title_prefix=f"Figura B: histograma de evaluaciones en {function_label} {dimension_label}",
        xlabel="Evaluaciones",
        color="#f58518",
        bins=bins,
        figsize=(18, 4.5),
    )


def plot_rosenbrock_final_value_histogram(
    runs_df,
    *,
    dimension_label: str,
    sample_sizes: list[int] | None = None,
    bins: int = 20,
):
    return plot_final_value_histogram(
        runs_df,
        function_label="Rosenbrock",
        dimension_label=dimension_label,
        sample_sizes=sample_sizes,
        bins=bins,
    )


def plot_rosenbrock_evaluations_histogram(
    runs_df,
    *,
    dimension_label: str,
    sample_sizes: list[int] | None = None,
    bins: int = 20,
):
    return plot_evaluations_histogram(
        runs_df,
        function_label="Rosenbrock",
        dimension_label=dimension_label,
        sample_sizes=sample_sizes,
        bins=bins,
    )
