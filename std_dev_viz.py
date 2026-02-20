"""
Standard Deviation Visualization — Teaching Edition v2
=======================================================
Five self-contained Manim scenes designed for classroom use.

What changed from v1:
  • Every scene that compares datasets shows a DATA TABLE with computed means,
    proving explicitly that the means are identical across groups.
  • Every graph carries manual numerical axis graduations (no LaTeX required).
  • Deviation arrows in Scene 2 are labelled with their ± distance.
  • Scene 3 builds a full computation table row-by-row (xᵢ | xᵢ−x̄ | (xᵢ−x̄)²)
    before deriving the formula.
  • Every scene ends with a breadcrumb sentence previewing the next one.

Scenes:
  DatasetIntroScene     – data tables + means proven equal + bar charts w/ y-axis
  DispersionScene       – comparison table + labelled number line + deviation arrows
  StdDevFormulaScene    – row-by-row computation table + formula derivation
  StabilityCompareScene – stats table + dual line graphs with numbered axes
  RealWorldScene        – asset stats table + time-series with numbered axes
"""

from manim import *
import numpy as np

# ── palette ───────────────────────────────────────────────────────────────────
C_LOW  = GREEN
C_MID  = YELLOW
C_HIGH = RED
C_MEAN = WHITE
C_BG   = "#1a1a2e"

# ── shared datasets  (all have mean = 10.0, sum = 100) ───────────────────────
STABLE   = [9, 10, 10, 11, 10,  9, 10, 11, 10, 10]   # σ ≈ 0.6
MODERATE = [6,  8, 12,  7, 14,  7,  9, 13,  9, 15]   # σ ≈ 3.0
CHAOTIC  = [1, 18,  3, 17,  2, 19,  4, 16,  5, 15]   # σ ≈ 7.0


# ═════════════════════════════════════════════════════════════════════════════
# Shared helper functions (no LaTeX anywhere)
# ═════════════════════════════════════════════════════════════════════════════

def _trow(vals, widths, row_h, accent=YELLOW, is_header=False):
    """One table row: list of (background rect + text) pairs as a VGroup."""
    g  = VGroup()
    x0 = -sum(widths) / 2
    for val, w in zip(vals, widths):
        bg = Rectangle(
            width=w, height=row_h,
            fill_color=accent, fill_opacity=0.15 if is_header else 0.0,
            stroke_color=GRAY, stroke_width=0.65,
        ).move_to([x0 + w / 2, -row_h / 2, 0])
        txt = Text(
            str(val),
            font_size=17 if is_header else 15,
            color=accent if is_header else WHITE,
        ).move_to(bg)
        g.add(bg, txt)
        x0 += w
    return g


def _table(headers, rows, col_widths, row_h=0.40, accent=YELLOW):
    """
    Stack table rows into a VGroup.
    Returns a VGroup where children are the individual row VGroups,
    so callers can animate them one at a time.
    """
    all_rows = VGroup()

    header = _trow(headers, col_widths, row_h, accent=accent, is_header=True)
    all_rows.add(header)

    for row in rows:
        r = _trow(row, col_widths, row_h, accent=accent, is_header=False)
        r.next_to(all_rows, DOWN, buff=0)
        all_rows.add(r)

    return all_rows


def _y_nums(ax, tick_vals, fs=14, color=GRAY):
    """Text tick-labels placed on the y-axis of an Axes object."""
    g = VGroup()
    for v in tick_vals:
        lbl = Text(str(v), font_size=fs, color=color)
        lbl.next_to(ax.c2p(ax.x_range[0], v), LEFT, buff=0.12)
        g.add(lbl)
    return g


def _x_nums(ax, tick_vals, labels=None, fs=14, color=GRAY):
    """Text tick-labels placed on the x-axis of an Axes object."""
    g = VGroup()
    for i, v in enumerate(tick_vals):
        lbl = Text(labels[i] if labels else str(v), font_size=fs, color=color)
        lbl.next_to(ax.c2p(v, ax.y_range[0]), DOWN, buff=0.10)
        g.add(lbl)
    return g


def _mean_line(ax, mean_val, color=C_MEAN):
    """Horizontal dashed mean reference line + label on an Axes object."""
    line = DashedLine(
        ax.c2p(ax.x_range[0], mean_val),
        ax.c2p(ax.x_range[1], mean_val),
        color=color, stroke_width=1.5, dash_length=0.12,
    )
    lbl = Text(f"x̄={mean_val:.0f}", font_size=14, color=color)
    lbl.next_to(ax.c2p(ax.x_range[1], mean_val), RIGHT, buff=0.06)
    return VGroup(line, lbl)


def _breadcrumb(text):
    """Dim grey 'next scene' hint at the bottom of the frame."""
    return Text(text, font_size=18, color=GRAY, slant=ITALIC).to_edge(DOWN)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 1 – Dataset Introduction
# ═════════════════════════════════════════════════════════════════════════════
class DatasetIntroScene(Scene):
    """
    Step 1 – Show raw data tables for three datasets and compute the mean
             for each, proving they are all equal (10.0).
    Step 2 – Animate bar charts with numbered y-axis for visual comparison.
    """

    CONFIGS = [
        ("Stable",   STABLE,   C_LOW),
        ("Moderate", MODERATE, C_MID),
        ("Chaotic",  CHAOTIC,  C_HIGH),
    ]

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Dataset Spread", font_size=40, color=WHITE).to_edge(UP)
        sub   = Text("Three datasets — same mean, very different spread",
                     font_size=21, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: data tables with mean row ─────────────────────────────────
        step1 = Text("Step 1 — Raw data & means", font_size=21, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.2)
        self.play(FadeIn(step1))

        col_groups = VGroup()
        for name, data, colour in self.CONFIGS:
            mean_v = np.mean(data)
            tbl = _table(
                headers=["i", "xᵢ"],
                rows=[[str(i + 1), str(v)] for i, v in enumerate(data)]
                     + [["x̄", f"{mean_v:.1f}"]],
                col_widths=[0.50, 0.60],
                row_h=0.31,
                accent=colour,
            )
            # tint the mean (last) row distinctly
            mean_row = tbl[-1]
            for child in mean_row:
                if isinstance(child, Rectangle):
                    child.set_fill(color=colour, opacity=0.30)
                elif isinstance(child, Text):
                    child.set_color(colour)

            cap = Text(name, font_size=20, color=colour).next_to(tbl, UP, buff=0.12)
            col_groups.add(VGroup(cap, tbl))

        col_groups.arrange(RIGHT, buff=0.55).next_to(step1, DOWN, buff=0.25)

        for col in col_groups:
            self.play(FadeIn(col, shift=UP * 0.15), run_time=0.65)
            self.wait(0.15)

        # callout: means are all equal
        mean_rows = VGroup(*[grp[1][-1] for grp in col_groups])
        box = SurroundingRectangle(mean_rows, color=YELLOW, buff=0.06, corner_radius=0.05)
        note = Text("All x̄ = 10.0  ←  identical means, yet the data looks completely different",
                    font_size=18, color=YELLOW).to_edge(DOWN)
        self.play(Create(box), Write(note))
        self.wait(1.8)

        # ── STEP 2: bar charts with numbered y-axis ────────────────────────────
        step2 = Text("Step 2 — Visual comparison (y-axis: value)", font_size=21, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.2)
        self.play(
            FadeOut(step1), FadeOut(col_groups), FadeOut(box), FadeOut(note),
            FadeIn(step2),
        )

        charts = VGroup()
        for name, data, colour in self.CONFIGS:
            charts.add(self._bar_chart(name, data, colour))
        charts.arrange(RIGHT, buff=0.5).next_to(step2, DOWN, buff=0.25)

        for chart in charts:
            self.play(FadeIn(chart, shift=UP * 0.15), run_time=0.65)
            self.wait(0.15)

        crumb = _breadcrumb("Next: measure exactly how far each value sits from the mean  →")
        self.play(Write(crumb))
        self.wait(2.2)

    # ── helper: bar chart with manual y-axis numbers ──────────────────────────
    def _bar_chart(self, name, data, colour, chart_h=3.2, y_max=20):
        n    = len(data)
        bw   = 0.18
        gap  = 0.23
        scl  = chart_h / y_max
        mean = np.mean(data)

        bars = VGroup()
        for i, v in enumerate(data):
            h = v * scl
            rect = Rectangle(
                width=bw, height=h,
                fill_color=colour, fill_opacity=0.85,
                stroke_color=colour, stroke_width=0.7,
            ).move_to([(i - n / 2 + 0.5) * gap, h / 2 - chart_h / 2, 0])
            bars.add(rect)

        # y-axis spine + tick lines + labels
        x_left = -(n / 2) * gap - 0.18
        spine  = Line([x_left, -chart_h / 2, 0], [x_left, chart_h / 2, 0],
                      color=GRAY, stroke_width=1.0)
        x_bot  = Line([x_left, -chart_h / 2, 0],
                      [ (n / 2) * gap + 0.1, -chart_h / 2, 0],
                      color=GRAY, stroke_width=1.0)
        tick_grp = VGroup()
        for yv in [0, 5, 10, 15, 20]:
            ypos = yv * scl - chart_h / 2
            tick = Line([x_left - 0.10, ypos, 0], [x_left, ypos, 0],
                        color=GRAY, stroke_width=0.8)
            lbl  = Text(str(yv), font_size=12, color=GRAY)
            lbl.next_to(tick, LEFT, buff=0.06)
            tick_grp.add(tick, lbl)

        # mean dashed line
        mean_y = mean * scl - chart_h / 2
        ml     = DashedLine(
            [x_left, mean_y, 0], [(n / 2) * gap + 0.1, mean_y, 0],
            color=C_MEAN, stroke_width=1.5,
        )
        ml_lbl = Text(f"x̄={mean:.0f}", font_size=12, color=C_MEAN)
        ml_lbl.next_to(ml, RIGHT, buff=0.04)

        caption = Text(f"{name}\nσ={np.std(data):.1f}", font_size=16, color=colour)
        caption.next_to(VGroup(bars, spine), DOWN, buff=0.12)

        return VGroup(spine, x_bot, tick_grp, bars, ml, ml_lbl, caption)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 2 – Dispersion from the Mean
# ═════════════════════════════════════════════════════════════════════════════
class DispersionScene(Scene):
    """
    Step 1 – Comparison table: both datasets, their sums and means
             — identical at 10.0, proving the only difference is spread.
    Step 2 – Number line with tick labels; dots animate from mean to actual
             positions; deviation arrows carry ± distance labels.
    """

    LOW_DATA  = STABLE                              # mean=10, σ≈0.6
    HIGH_DATA = CHAOTIC                             # mean=10, σ≈7.0

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Dispersion from the Mean", font_size=38, color=WHITE).to_edge(UP)
        self.play(Write(title))

        ld, hd = self.LOW_DATA, self.HIGH_DATA

        # ── STEP 1: comparison table ───────────────────────────────────────────
        step1 = Text("Step 1 — Confirm equal means", font_size=21, color=YELLOW)
        step1.next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(step1))

        vals_low  = "  ".join(str(v) for v in ld[:5]) + "\n" + "  ".join(str(v) for v in ld[5:])
        vals_high = "  ".join(str(v) for v in hd[:5]) + "\n" + "  ".join(str(v) for v in hd[5:])

        tbl = _table(
            headers=["Dataset", "Values  (first 5 / last 5)", "Σ", "n", "x̄"],
            rows=[
                ["Low σ",  "9  10  10  11  10  /  9  10  11  10  10",
                 str(sum(ld)), str(len(ld)), f"{np.mean(ld):.1f}"],
                ["High σ", "1  18   3  17   2  /  19   4  16   5  15",
                 str(sum(hd)), str(len(hd)), f"{np.mean(hd):.1f}"],
            ],
            col_widths=[1.0, 4.2, 0.65, 0.5, 0.75],
            row_h=0.48,
            accent=YELLOW,
        )
        tbl.next_to(step1, DOWN, buff=0.28)
        self.play(FadeIn(tbl))

        box  = SurroundingRectangle(tbl, color=YELLOW, buff=0.08)
        note = Text("Both x̄ = 10.0  ✓   The ONLY difference is how spread out the values are",
                    font_size=18, color=YELLOW).to_edge(DOWN)
        self.play(Create(box), Write(note))
        self.wait(1.6)

        # ── STEP 2: number line + animated dots + labelled deviation arrows ────
        step2 = Text("Step 2 — Watch the deviations", font_size=21, color=YELLOW)
        step2.next_to(title, DOWN, buff=0.22)
        self.play(FadeOut(step1), FadeOut(tbl), FadeOut(box), FadeOut(note), FadeIn(step2))

        for lbl_txt, data, colour, y0 in [
            ("Low σ",  ld, C_LOW,   1.1),
            ("High σ", hd, C_HIGH, -1.4),
        ]:
            mean_v  = np.mean(data)
            scale_x = 10.2 / 20          # map value range [0,20] → ~[-5.1, 5.1]
            x_off   = -5.1

            # axis line
            nl  = Line([-5.3, y0, 0], [5.3, y0, 0], color=GRAY, stroke_width=1.4)
            row_lbl = Text(lbl_txt, font_size=23, color=colour)
            row_lbl.next_to(nl, LEFT, buff=0.08)

            # numeric tick marks: 0, 5, 10, 15, 20
            tick_grp = VGroup()
            for tv in [0, 5, 10, 15, 20]:
                tx   = tv * scale_x + x_off
                tick = Line([tx, y0 - 0.13, 0], [tx, y0 + 0.13, 0],
                            color=GRAY, stroke_width=1.0)
                tlbl = Text(str(tv), font_size=13, color=GRAY)
                tlbl.next_to([tx, y0 - 0.13, 0], DOWN, buff=0.06)
                tick_grp.add(tick, tlbl)

            # mean marker
            mx     = mean_v * scale_x + x_off
            ml     = DashedLine([mx, y0 - 0.42, 0], [mx, y0 + 0.42, 0],
                                color=C_MEAN, stroke_width=2)
            ml_lbl = Text("x̄=10", font_size=14, color=C_MEAN)
            ml_lbl.next_to([mx, y0 + 0.42, 0], UP, buff=0.04)

            self.play(Create(nl), FadeIn(row_lbl), Create(tick_grp),
                      Create(ml), Write(ml_lbl), run_time=0.55)

            # dots: start at mean, fly to actual positions
            dots = VGroup(*[Dot([mx, y0, 0], color=colour, radius=0.11) for _ in data])
            self.play(FadeIn(dots), run_time=0.25)

            target_xs = [v * scale_x + x_off for v in data]
            self.play(*[d.animate.move_to([tx, y0, 0])
                        for d, tx in zip(dots, target_xs)], run_time=1.3)

            # deviation arrows with ± labels
            arr_grp = VGroup()
            for dot, v, tx in zip(dots, data, target_xs):
                dev = v - mean_v
                if abs(dev) < 0.05:
                    continue
                arr = Arrow(
                    [mx, y0, 0], [tx, y0, 0],
                    buff=0, stroke_width=1.4, color=colour,
                    tip_length=0.10, max_stroke_width_to_length_ratio=999,
                )
                d_lbl = Text(f"{dev:+.0f}", font_size=11, color=colour)
                d_lbl.next_to(arr.get_center(),
                              UP * 0.4 if y0 > 0 else DOWN * 0.4, buff=0.02)
                arr_grp.add(arr, d_lbl)
            self.play(Create(arr_grp), run_time=0.75)

        msg   = Text("Wider spread  →  Higher σ  →  More instability",
                     font_size=22, color=YELLOW)
        crumb = _breadcrumb("Next: one formula that captures all those deviations  →")
        msg.next_to(crumb, UP, buff=0.18)
        self.play(Write(msg), FadeIn(crumb))
        self.wait(2.5)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 3 – Standard Deviation Formula
# ═════════════════════════════════════════════════════════════════════════════
class StdDevFormulaScene(Scene):
    """
    Left panel  – computation table built row-by-row: xᵢ | xᵢ−x̄ | (xᵢ−x̄)²
    Right panel – running summary: Σ squares, variance, σ, and the formula.
    """

    DATA = [2, 4, 4, 4, 5, 5, 7, 9]

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Building the Formula", font_size=38, color=WHITE).to_edge(UP)
        self.play(Write(title))

        data     = self.DATA
        mean_v   = float(np.mean(data))
        devs     = [v - mean_v for v in data]
        sq_devs  = [d ** 2 for d in devs]
        variance = float(np.mean(sq_devs))
        sigma    = float(np.sqrt(variance))

        # dataset + mean header
        header_line = Text(
            f"Dataset:  {data}   →   x̄ = {sum(data)} / {len(data)} = {mean_v:.0f}",
            font_size=22, color=YELLOW,
        ).next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(header_line))

        # ── LEFT: computation table ────────────────────────────────────────────
        col_w   = [0.75, 1.05, 1.30]
        row_h   = 0.37
        headers = ["xᵢ", "xᵢ − x̄", "(xᵢ − x̄)²"]

        # Header row (static)
        h_row = _trow(headers, col_w, row_h, accent=YELLOW, is_header=True)
        h_row.next_to(header_line, DOWN, buff=0.28)
        h_row.shift(LEFT * 2.6)
        self.play(FadeIn(h_row))

        # Data rows appear one at a time
        prev = h_row
        data_rows = []
        for v, d, sq in zip(data, devs, sq_devs):
            r = _trow(
                [str(v), f"{d:+.0f}", str(int(sq))],
                col_w, row_h, accent=YELLOW, is_header=False,
            )
            r.next_to(prev, DOWN, buff=0)
            self.play(FadeIn(r), run_time=0.28)
            data_rows.append(r)
            prev = r

        # Σ summary row
        sq_sum = int(sum(sq_devs))
        sum_row = _trow(
            ["Σ", "—", str(sq_sum)],
            col_w, row_h, accent=C_MID, is_header=True,
        )
        sum_row.next_to(prev, DOWN, buff=0)
        self.play(FadeIn(sum_row))
        self.wait(0.4)

        # ── RIGHT: running derivation ──────────────────────────────────────────
        right_x = RIGHT * 2.5
        steps = VGroup()

        s1 = Text(f"Σ(xᵢ − x̄)²  =  {sq_sum}", font_size=20, color=C_MID)
        s1.next_to(header_line, DOWN, buff=0.28)
        s1.align_to(right_x, LEFT)

        s2 = Text(f"Variance  =  {sq_sum} / {len(data)}  =  {variance:.2f}",
                  font_size=20, color=C_MID)
        s2.next_to(s1, DOWN, buff=0.28)
        s2.align_to(right_x, LEFT)

        formula = Text("σ  =  √( Σ(xᵢ − x̄)² / n )", font_size=26, color=WHITE)
        formula.next_to(s2, DOWN, buff=0.32)
        formula.align_to(right_x, LEFT)

        result = Text(f"σ  =  √{variance:.2f}  ≈  {sigma:.2f}", font_size=26, color=C_HIGH)
        result.next_to(formula, DOWN, buff=0.20)
        result.align_to(right_x, LEFT)

        res_box = SurroundingRectangle(result, color=C_HIGH, buff=0.12, corner_radius=0.06)

        for mob in [s1, s2, formula, result]:
            self.play(FadeIn(mob, shift=RIGHT * 0.2), run_time=0.55)
            self.wait(0.35)
        self.play(Create(res_box))

        interp = Text(
            f"σ = {sigma:.2f}  means every value is ~{sigma:.1f} units from the mean on average",
            font_size=18, color=GRAY_A,
        )
        crumb = _breadcrumb("Next: watch what σ = 0.6 vs σ = 5.7 look like on a graph  →")
        interp.next_to(crumb, UP, buff=0.18)
        self.play(FadeIn(interp), FadeIn(crumb))
        self.wait(2.5)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 4 – Stability Comparison
# ═════════════════════════════════════════════════════════════════════════════
class StabilityCompareScene(Scene):
    """
    Step 1 – Stats table: mean, σ, and interpretation for both series.
    Step 2 – Side-by-side line graphs with numbered y-axis (0–22) and
             numbered x-axis (time steps), plus dashed mean reference lines.
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("σ and Data Instability", font_size=38, color=WHITE).to_edge(UP)
        self.play(Write(title))

        np.random.seed(7)
        n         = 20
        low_data  = np.round(10 + np.random.normal(0, 0.6, n)).astype(int)
        high_data = np.clip(np.round(10 + np.random.normal(0, 4.5, n)).astype(int), 0, 22)
        sig_low   = float(np.std(low_data))
        sig_high  = float(np.std(high_data))
        m_low     = float(np.mean(low_data))
        m_high    = float(np.mean(high_data))

        # ── STEP 1: stats table ────────────────────────────────────────────────
        step1 = Text("Step 1 — Compare the statistics", font_size=21, color=YELLOW)
        step1.next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(step1))

        tbl = _table(
            headers=["Series", "x̄  (mean)", "σ", "What it means"],
            rows=[
                ["Low σ",  f"{m_low:.1f}",  f"{sig_low:.2f}",  "Stable — next value is predictable"],
                ["High σ", f"{m_high:.1f}", f"{sig_high:.2f}", "Chaotic — next value could be anywhere"],
            ],
            col_widths=[0.95, 1.15, 0.90, 3.50],
            row_h=0.48,
            accent=YELLOW,
        )
        tbl.next_to(step1, DOWN, buff=0.28)
        self.play(FadeIn(tbl))
        self.wait(1.3)

        # ── STEP 2: dual line graphs ───────────────────────────────────────────
        step2 = Text("Step 2 — Visual comparison", font_size=21, color=YELLOW)
        step2.next_to(title, DOWN, buff=0.22)
        self.play(FadeOut(step1), FadeOut(tbl), FadeIn(step2))

        ax_kw = dict(
            x_range=[0, n - 1, 5],
            y_range=[0, 22, 2],
            x_length=4.5,
            y_length=3.5,
            axis_config={"color": GRAY, "stroke_width": 1.3,
                         "include_tip": False, "include_numbers": False},
        )
        ax_l = Axes(**ax_kw).shift(LEFT * 3.1 + DOWN * 0.45)
        ax_h = Axes(**ax_kw).shift(RIGHT * 3.1 + DOWN * 0.45)

        y_ticks = [0, 5, 10, 15, 20]
        x_ticks = [0, 5, 10, 15, 19]
        yl_l = _y_nums(ax_l, y_ticks)
        yl_h = _y_nums(ax_h, y_ticks)
        xl_l = _x_nums(ax_l, x_ticks)
        xl_h = _x_nums(ax_h, x_ticks)

        y_ax_lbl_l = Text("value", font_size=13, color=GRAY).next_to(ax_l.y_axis, LEFT, buff=0.45)
        y_ax_lbl_h = Text("value", font_size=13, color=GRAY).next_to(ax_h.y_axis, LEFT, buff=0.45)
        x_ax_lbl_l = Text("time",  font_size=13, color=GRAY).next_to(ax_l.x_axis, DOWN, buff=0.38)
        x_ax_lbl_h = Text("time",  font_size=13, color=GRAY).next_to(ax_h.x_axis, DOWN, buff=0.38)

        lbl_l = VGroup(
            Text(f"Low σ = {sig_low:.2f}", font_size=23, color=C_LOW),
            Text("Stable", font_size=17, color=C_LOW, slant=ITALIC),
        ).arrange(DOWN, buff=0.06).next_to(ax_l, UP, buff=0.08)

        lbl_h = VGroup(
            Text(f"High σ = {sig_high:.2f}", font_size=23, color=C_HIGH),
            Text("Unstable / Chaotic", font_size=17, color=C_HIGH, slant=ITALIC),
        ).arrange(DOWN, buff=0.06).next_to(ax_h, UP, buff=0.08)

        self.play(
            Create(ax_l), Create(ax_h),
            FadeIn(yl_l), FadeIn(yl_h),
            FadeIn(xl_l), FadeIn(xl_h),
            FadeIn(y_ax_lbl_l), FadeIn(y_ax_lbl_h),
            FadeIn(x_ax_lbl_l), FadeIn(x_ax_lbl_h),
            FadeIn(lbl_l), FadeIn(lbl_h),
        )

        # mean reference lines
        ml_l = DashedLine(ax_l.c2p(0, m_low),  ax_l.c2p(n - 1, m_low),
                          color=C_MEAN, stroke_width=1.3)
        ml_h = DashedLine(ax_h.c2p(0, m_high), ax_h.c2p(n - 1, m_high),
                          color=C_MEAN, stroke_width=1.3)
        ml_l_lbl = Text(f"x̄={m_low:.0f}", font_size=12, color=C_MEAN)
        ml_h_lbl = Text(f"x̄={m_high:.0f}", font_size=12, color=C_MEAN)
        ml_l_lbl.next_to(ax_l.c2p(n - 1, m_low),  RIGHT, buff=0.05)
        ml_h_lbl.next_to(ax_h.c2p(n - 1, m_high), RIGHT, buff=0.05)
        self.play(Create(ml_l), Create(ml_h), Write(ml_l_lbl), Write(ml_h_lbl))

        # data lines + dots
        pts_l  = [ax_l.c2p(i, v) for i, v in enumerate(low_data)]
        pts_h  = [ax_h.c2p(i, v) for i, v in enumerate(high_data)]
        line_l = VMobject(color=C_LOW,  stroke_width=2.5).set_points_as_corners(pts_l)
        line_h = VMobject(color=C_HIGH, stroke_width=2.5).set_points_as_corners(pts_h)
        self.play(Create(line_l), Create(line_h), run_time=2.5)

        dots_l = VGroup(*[Dot(p, color=C_LOW,  radius=0.07) for p in pts_l])
        dots_h = VGroup(*[Dot(p, color=C_HIGH, radius=0.07) for p in pts_h])
        self.play(FadeIn(dots_l), FadeIn(dots_h))

        msg   = Text("Higher σ  →  Wider swings  →  Less predictable",
                     font_size=21, color=YELLOW)
        crumb = _breadcrumb("Next: see this in a real-world scenario  →")
        msg.next_to(crumb, UP, buff=0.18)
        self.play(Write(msg), FadeIn(crumb))
        self.wait(2.5)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 5 – Real-World Impact
# ═════════════════════════════════════════════════════════════════════════════
class RealWorldScene(Scene):
    """
    Step 1 – Asset stats table: final value, daily σ, and risk label.
    Step 2 – 30-day price chart with numbered y-axis and x-axis (day numbers).
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Real-World Impact", font_size=38, color=WHITE)
        sub   = Text("Two assets — same average daily gain, different volatility",
                     font_size=20, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.1)
        VGroup(title, sub).to_edge(UP)
        self.play(Write(title), FadeIn(sub))

        np.random.seed(42)
        n         = 30
        xs        = np.arange(n)
        a_returns = np.cumsum(np.random.normal(0.3, 1.0, n)) + 100
        b_returns = np.cumsum(np.random.normal(0.3, 4.0, n)) + 100
        sig_a     = float(np.std(np.diff(a_returns)))
        sig_b     = float(np.std(np.diff(b_returns)))

        # ── STEP 1: stats table ────────────────────────────────────────────────
        step1 = Text("Step 1 — Asset statistics", font_size=21, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.22)
        self.play(FadeIn(step1))

        tbl = _table(
            headers=["Asset", "Daily gain avg", "Daily σ", "Risk verdict"],
            rows=[
                ["A (green)", "+0.3",  f"{sig_a:.2f}", "LOW  — steady, predictable"],
                ["B (red)",   "+0.3",  f"{sig_b:.2f}", "HIGH — volatile, dangerous"],
            ],
            col_widths=[1.25, 1.50, 1.10, 2.85],
            row_h=0.48,
            accent=YELLOW,
        )
        tbl.next_to(step1, DOWN, buff=0.28)
        self.play(FadeIn(tbl))

        note = Text(
            "Same average gain — σ alone separates 'stable growth' from 'high risk'",
            font_size=17, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(note))
        self.wait(1.4)

        # ── STEP 2: time-series with numbered axes ─────────────────────────────
        step2 = Text("Step 2 — 30-day price chart", font_size=21, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.22)
        self.play(FadeOut(step1), FadeOut(tbl), FadeOut(note), FadeIn(step2))

        y_min = float(min(a_returns.min(), b_returns.min())) - 5
        y_max = float(max(a_returns.max(), b_returns.max())) + 5

        ax = Axes(
            x_range=[0, n - 1, 5],
            y_range=[y_min, y_max, 10],
            x_length=9.0,
            y_length=4.0,
            axis_config={"color": GRAY, "stroke_width": 1.3,
                         "include_tip": False, "include_numbers": False},
        ).next_to(step2, DOWN, buff=0.25)

        # y-axis: round to nearest 10 for clean ticks
        y_lo = int(np.floor(y_min / 10) * 10)
        y_hi = int(np.ceil(y_max  / 10) * 10)
        y_tick_vals = list(range(y_lo, y_hi + 1, 10))
        yl = _y_nums(ax, y_tick_vals, fs=13)

        # x-axis: day numbers
        xl = _x_nums(ax, [0, 5, 10, 15, 20, 25, 29], fs=13)

        x_lbl = Text("Day",   font_size=16, color=GRAY).next_to(ax.x_axis, DOWN, buff=0.38)
        y_lbl = Text("Price", font_size=16, color=GRAY).next_to(ax.y_axis, LEFT, buff=0.45)

        self.play(Create(ax), FadeIn(yl), FadeIn(xl), Write(x_lbl), Write(y_lbl))

        pts_a  = [ax.c2p(i, v) for i, v in zip(xs, a_returns)]
        pts_b  = [ax.c2p(i, v) for i, v in zip(xs, b_returns)]
        line_a = VMobject(color=C_LOW,  stroke_width=2.5).set_points_as_corners(pts_a)
        line_b = VMobject(color=C_HIGH, stroke_width=2.5).set_points_as_corners(pts_b)
        self.play(Create(line_a), Create(line_b), run_time=3.0)

        leg_a = VGroup(
            Line(ORIGIN, RIGHT * 0.55, color=C_LOW,  stroke_width=3),
            Text(f"Asset A  σ={sig_a:.1f}  stable",   font_size=16, color=C_LOW),
        ).arrange(RIGHT, buff=0.1)
        leg_b = VGroup(
            Line(ORIGIN, RIGHT * 0.55, color=C_HIGH, stroke_width=3),
            Text(f"Asset B  σ={sig_b:.1f}  volatile", font_size=16, color=C_HIGH),
        ).arrange(RIGHT, buff=0.1)
        legend = VGroup(leg_b, leg_a).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        legend.to_corner(DR).shift(UP * 0.3 + LEFT * 0.1)
        self.play(FadeIn(legend))

        box_txt = Text(
            "Low σ  →  Predictable, lower risk\n"
            "High σ  →  Unpredictable, higher risk",
            font_size=19, color=WHITE,
        )
        box = SurroundingRectangle(box_txt, color=YELLOW, buff=0.16, corner_radius=0.08)
        VGroup(box, box_txt).to_edge(DOWN)
        self.play(FadeIn(VGroup(box, box_txt)))
        self.wait(3.0)
