"""
Design goals:
- Simple function signatures for portfolio notebooks
- No seaborn dependency
- Helpful defaults (sorting, tick formatting) for common business charts
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from IPython.display import display, Markdown


def bar_vertical(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    sort_by: Optional[str] = None,
    ascending: bool = False,
    figsize: Tuple[int, int] = (10, 5),
    rotate_x: int = 0,
) -> None:
    """Vertical bar chart."""
    d = df.copy()
    if sort_by:
        d = d.sort_values(sort_by, ascending=ascending)

    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.bar(d[x].astype(str), d[y])

    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=rotate_x)
    plt.tight_layout()
    plt.show()


def bar_horizontal(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    sort_desc: bool = True,
    figsize: Tuple[int, int] = (10, 6),
) -> None:
    """Horizontal bar chart (largest at top by default)."""
    d = df.copy().sort_values(x, ascending=not sort_desc)

    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.barh(d[y].astype(str), d[x])
    ax.invert_yaxis()

    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    plt.show()


def line_plot_monthly(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str,
    xlabel: str = "Month",
    ylabel: str = "Value",
    month_interval: int = 3,
    figsize: Tuple[int, int] = (11, 5),
    marker: str = "o",
) -> None:
    """Line plot optimized for monthly time series."""
    import matplotlib.dates as mdates

    d = df.copy()
    d[date_col] = pd.to_datetime(d[date_col])
    d = d.sort_values(date_col)

    plt.figure(figsize=figsize)
    plt.plot(d[date_col], d[value_col], marker=marker)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=month_interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def grouped_bar_wide(
    df: pd.DataFrame,
    x: str,
    y_cols: Sequence[str],
    title: str,
    xlabel: Optional[str] = None,
    ylabel: str = "",
    legend_title: str = "",
    figsize: Tuple[int, int] = (11, 5),
    rotate_x: int = 0,
    y_col_labels: Optional[Sequence[str]] = None,
) -> None:
    """Grouped bars when data is wide (one row per x)."""
    import numpy as np

    d = df.copy()
    labels = d[x].astype(str).tolist()
    n = len(y_cols)

    legend_labels = list(y_col_labels) if y_col_labels is not None else list(y_cols)
    if len(legend_labels) != n:
        raise ValueError("y_col_labels must have the same length as y_cols")

    x_idx = np.arange(len(labels))
    width = 0.8 / max(n, 1)

    plt.figure(figsize=figsize)
    ax = plt.gca()

    for i, (col, lab) in enumerate(zip(y_cols, legend_labels)):
        ax.bar(x_idx + i * width, d[col].values, width=width, label=str(lab))

    ax.set_xticks(x_idx + width * (n - 1) / 2)
    ax.set_xticklabels(labels, rotation=rotate_x)

    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel)
    ax.legend(title=legend_title if legend_title else None)

    plt.tight_layout()
    plt.show()


def scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6),
    alpha: float = 0.7,
) -> None:
    """Simple scatter plot."""
    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.scatter(df[x], df[y], alpha=alpha)

    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    plt.show()


def insight_monthly_trend(
    df: pd.DataFrame,
    date_col: str = "MonthStart",
    value_col: str = "TotalSales",
) -> None:
    """Display a short insight paragraph for monthly trend charts."""
    d = df.copy()
    d[date_col] = pd.to_datetime(d[date_col])

    def _fmt_month(v) -> str:
        return pd.to_datetime(v).strftime("%Y-%m")

    peak = d.loc[d[value_col].idxmax()]
    low = d.loc[d[value_col].idxmin()]

    start_month = _fmt_month(d.iloc[0][date_col])
    end_month = _fmt_month(d.iloc[-1][date_col])

    start_val = float(d.iloc[0][value_col])
    end_val = float(d.iloc[-1][value_col])

    direction = "upward" if end_val >= start_val else "downward"

    display(
        Markdown(
            f"""**Insight:** The overall monthly sales trend is **{direction}** from **{start_month}** ({start_val:,.0f}) to **{end_month}** ({end_val:,.0f}).  
- **Highest month:** **{_fmt_month(peak[date_col])}** ({float(peak[value_col]):,.0f})  
- **Lowest month:** **{_fmt_month(low[date_col])}** ({float(low[value_col]):,.0f})"""
        )
    )