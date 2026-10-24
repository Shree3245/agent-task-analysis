"""Self-contained SVG charts; no browser library, JS, font, or network dependency."""

from html import escape
import math
import numpy as np


def frame(title, body):
    return (
        f'<svg role="img" aria-label="{escape(title)}" viewBox="0 0 680 270" '
        'xmlns="http://www.w3.org/2000/svg"><rect width="680" height="270" fill="#fff"/>'
        '<g font-family="system-ui,sans-serif" font-size="12" fill="#435265">'
        f'<text x="58" y="24" font-size="15" font-weight="600">{escape(title)}</text>'
        '<path d="M58 42V220H650" stroke="#c2cbd4" fill="none"/>' + body + "</g></svg>"
    )


def distribution(values, name):
    positive = [v for v in values if v > 0]
    if not positive:
        return frame(
            f"{name} · cost distribution", '<text x="80" y="120">No positive priced costs</text>'
        )
    lo, hi = math.log10(min(positive)), math.log10(max(positive))
    if hi - lo < 0.1:
        lo, hi = lo - 0.5, hi + 0.5
    bins = np.linspace(lo, hi, 25)
    heights, _ = np.histogram(np.log10(positive), bins=bins)
    peak = max(heights.max(), 1)
    body = ""
    for count in (0, peak / 2, peak):
        yy = 220 - 160 * count / peak
        body += f'<text x="48" y="{yy + 4:.1f}" text-anchor="end">{count:g}</text>'
    for i, count in enumerate(heights):
        h = 160 * count / peak
        body += f'<rect x="{60 + i * 24.5:.1f}" y="{220 - h:.1f}" width="22" height="{h:.1f}" fill="#087f8c"><title>{count} tasks</title></rect>'
    for t in np.linspace(lo, hi, 5):
        x = 60 + (t - lo) / (hi - lo) * 588
        body += f'<text x="{x:.1f}" y="240" text-anchor="middle">${10**t:.3g}</text>'
    body += f'<text x="58" y="260">Log-scale USD · {len(values)} tasks · {len(values) - len(positive)} zero-cost</text>'
    return frame(f"{name} · cost distribution", body)


def loss_curve(row, name):
    price = row["price"]
    low_mean, high_mean = [v * price for v in row["ci"]]
    mean = row["loss_ratio"] * price
    prices = np.linspace(price * 0.5, price * 2, 60)
    ymax = max(1.2, high_mean / prices[0] * 1.1)

    def x(p):
        return 58 + (p - prices[0]) / (prices[-1] - prices[0]) * 590

    def y(r):
        return 220 - r / ymax * 170

    upper = [(x(p), y(high_mean / p)) for p in prices]
    lower = [(x(p), y(low_mean / p)) for p in reversed(prices)]
    points = " ".join(f"{a:.1f},{b:.1f}" for a, b in upper + lower)
    body = f'<polygon points="{points}" fill="#bce1e4"/>'
    curve = " ".join(f"{x(p):.1f},{y(mean / p):.1f}" for p in prices)
    body += f'<polyline points="{curve}" stroke="#087f8c" stroke-width="3" fill="none"/>'
    for ratio in (0.6, 0.9, 1.0):
        body += f'<path d="M58 {y(ratio):.1f}H650" stroke="#c2cbd4" stroke-dasharray="4 4"/><text x="8" y="{y(ratio) + 4:.1f}">{ratio:.0%}</text>'
    for p in np.linspace(prices[0], prices[-1], 5):
        body += f'<text x="{x(p):.1f}" y="240" text-anchor="middle">${p:.3g}</text>'
    body += '<text x="58" y="260">Fixed price · shaded band = 90% bootstrap interval</text>'
    return frame(f"{name} · {row['scope']} loss ratio vs price (p99 cap)", body)
