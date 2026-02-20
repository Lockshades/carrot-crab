"""
Standard Deviation Visualization using Manim
A study of small videos showing how higher std dev = higher data instability.

Scenes:
  1. DatasetIntroScene     – show raw datasets with different spreads
  2. DispersionScene       – animate dots dispersing from the mean
  3. StdDevFormulaScene    – build the formula step by step
  4. StabilityCompareScene – side-by-side stability comparison (low vs high σ)
  5. RealWorldScene        – real-world analogy (stock prices / temperature)
"""

from manim import *
import numpy as np

# ── colour palette ──────────────────────────────────────────────────────────
C_LOW   = GREEN        # low std dev
C_MID   = YELLOW       # medium std dev
C_HIGH  = RED          # high std dev
C_MEAN  = WHITE
C_BG    = "#1a1a2e"

# common config applied per-scene via self.camera.background_color
FONT = "Monospace"


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 1 – Dataset Introduction
# ═══════════════════════════════════════════════════════════════════════════
class DatasetIntroScene(Scene):
    """Show three datasets: stable, moderate, chaotic."""

    DATASETS = {
        "Stable\n(σ ≈ 0.5)":   ([9, 10, 10, 11, 10, 9, 10, 11, 10, 10], C_LOW),
        "Moderate\n(σ ≈ 2.5)": ([5, 8,  12, 7,  14, 6, 9,  13, 10, 6],  C_MID),
        "Chaotic\n(σ ≈ 5.5)":  ([1, 18, 3,  17, 2,  19,4,  16, 5,  15],  C_HIGH),
    }

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Dataset Spread", font_size=42, color=WHITE)
        subtitle = Text("Same mean — very different behaviour", font_size=24,
                        color=GRAY, slant=ITALIC)
        VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(0.5)

        cols = VGroup()
        for label, (data, colour) in self.DATASETS.items():
            bars = self._make_bar_chart(data, colour)
            lbl  = Text(label, font_size=22, color=colour).next_to(bars, DOWN, buff=0.2)
            col  = VGroup(bars, lbl)
            cols.add(col)

        cols.arrange(RIGHT, buff=0.7).next_to(subtitle, DOWN, buff=0.5)

        for col in cols:
            self.play(FadeIn(col, shift=UP*0.3), run_time=0.8)
            self.wait(0.3)

        # highlight mean line on each bar chart
        mean_label = Text("── mean", font_size=18, color=C_MEAN).to_corner(DR)
        self.play(Write(mean_label))
        self.wait(2)

    # ── helpers ──────────────────────────────────────────────────────────────
    def _make_bar_chart(self, data, colour, width=2.6, height=2.4):
        bars   = VGroup()
        n      = len(data)
        bw     = width / n * 0.8
        gap    = width / n
        mx     = max(data) if data else 1
        mean   = sum(data) / len(data)
        scale  = height / mx

        for i, v in enumerate(data):
            rect = Rectangle(
                width=bw, height=v * scale,
                fill_color=colour, fill_opacity=0.85,
                stroke_color=colour, stroke_width=1,
            )
            rect.move_to([(i - n / 2 + 0.5) * gap, v * scale / 2 - height / 2, 0])
            bars.add(rect)

        # mean line
        mean_line = DashedLine(
            [-width / 2, mean * scale - height / 2, 0],
            [ width / 2, mean * scale - height / 2, 0],
            color=C_MEAN, stroke_width=2,
        )
        frame = Rectangle(width=width + 0.1, height=height + 0.1,
                          stroke_color=colour, stroke_width=1.5, fill_opacity=0)
        return VGroup(frame, bars, mean_line)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 2 – Dispersion Animation
# ═══════════════════════════════════════════════════════════════════════════
class DispersionScene(Scene):
    """Dots start at the mean then fly to their actual values."""

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Dispersion from the Mean", font_size=38, color=WHITE).to_edge(UP)
        self.play(Write(title))

        configs = [
            ("Low σ",  [10, 10, 11, 9, 10, 10, 9, 11, 10, 10], C_LOW),
            ("High σ", [1,  19, 3,  17, 5,  15, 2,  18, 4,  16], C_HIGH),
        ]

        row_y = [1.0, -1.5]
        axes_list = []

        for idx, (lbl_txt, data, colour) in enumerate(configs):
            y0 = row_y[idx]
            mean_val = np.mean(data)

            # axis line
            ax = Line([-5.5, y0, 0], [5.5, y0, 0], color=GRAY, stroke_width=1.5)
            lbl = Text(lbl_txt, font_size=26, color=colour).next_to(ax, LEFT, buff=0.1)
            mean_line = DashedLine(
                [0, y0 - 0.4, 0], [0, y0 + 0.4, 0],
                color=C_MEAN, stroke_width=2,
            )
            mean_tex = Text("x̄", font_size=24, color=C_MEAN).next_to(mean_line, UP, buff=0.05)

            self.play(Create(ax), FadeIn(lbl), Create(mean_line), Write(mean_tex),
                      run_time=0.5)

            # dots start at mean
            dots = VGroup(*[
                Dot(point=[0, y0, 0], color=colour, radius=0.13)
                for _ in data
            ])
            self.play(FadeIn(dots))

            # explode to actual positions
            scale_x = 0.5
            anims = []
            for dot, val in zip(dots, data):
                target_x = (val - mean_val) * scale_x
                anims.append(dot.animate.move_to([target_x, y0, 0]))

            self.play(*anims, run_time=1.2)

            # deviation arrows
            arrows = VGroup()
            for dot, val in zip(dots, data):
                tx = (val - mean_val) * scale_x
                if abs(tx) > 0.05:
                    arr = Arrow(
                        [0, y0, 0], [tx, y0, 0],
                        buff=0, stroke_width=1.5,
                        color=colour, tip_length=0.12,
                        max_stroke_width_to_length_ratio=999,
                    )
                    arrows.add(arr)
            self.play(Create(arrows), run_time=0.6)
            axes_list.append((dots, arrows))

        # label spread difference
        note = Text("Wider spread  →  Higher σ  →  More instability",
                    font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(note))
        self.wait(2.5)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 3 – Standard Deviation Formula Build-Up
# ═══════════════════════════════════════════════════════════════════════════
class StdDevFormulaScene(Scene):
    """Step-by-step construction of the σ formula with a worked example."""

    DATA = [2, 4, 4, 4, 5, 5, 7, 9]

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Building the Formula", font_size=38, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        data   = self.DATA
        mean   = np.mean(data)
        devs   = [(x - mean) for x in data]
        sq_devs = [d**2 for d in devs]
        variance = np.mean(sq_devs)
        sigma  = np.sqrt(variance)

        # ── Step 1: show dataset ─────────────────────────────────────────
        step_lbl = Text("Step 1 – Dataset", font_size=28, color=YELLOW).shift(UP*2.2)
        data_txt = Text(str(data), font_size=28, color=WHITE).next_to(step_lbl, DOWN)
        self.play(FadeIn(step_lbl), Write(data_txt))
        self.wait(0.8)

        # ── Step 2: mean ─────────────────────────────────────────────────
        step2 = Text("Step 2 – Mean", font_size=28, color=YELLOW).shift(UP*2.2)
        mean_eq = Text(
            f"x̄ = Σxᵢ / n = {sum(data)} / {len(data)} = {mean}",
            font_size=28, color=WHITE,
        ).next_to(step2, DOWN)
        self.play(
            Transform(step_lbl, step2),
            Transform(data_txt, mean_eq),
        )
        self.wait(1)

        # ── Step 3: squared deviations ───────────────────────────────────
        step3 = Text("Step 3 – Squared Deviations  (x − x̄)²", font_size=26,
                     color=YELLOW).shift(UP*2.2)
        pairs = [(x, d, s) for x, d, s in zip(data, devs, sq_devs)]
        pair_strs = "  ".join([f"({x}−{mean:.0f})²={s:.0f}" for x, _, s in pairs[:4]])
        pair_strs2 = "  ".join([f"({x}−{mean:.0f})²={s:.0f}" for x, _, s in pairs[4:]])
        sq_txt = VGroup(
            Text(pair_strs,  font_size=20, color=C_MID),
            Text(pair_strs2, font_size=20, color=C_MID),
        ).arrange(DOWN, buff=0.1).next_to(step3, DOWN)
        self.play(
            Transform(step_lbl, step3),
            Transform(data_txt, sq_txt),
        )
        self.wait(1.2)

        # ── Step 4: full formula ─────────────────────────────────────────
        step4 = Text("Step 4 – Standard Deviation", font_size=28,
                     color=YELLOW).shift(UP*2.2)
        formula = Text(
            "σ = √( Σ(xᵢ − x̄)² / n )",
            font_size=38, color=WHITE,
        )
        result = Text(
            f"σ = √({variance:.2f})  ≈  {sigma:.2f}",
            font_size=32, color=C_HIGH,
        )
        formula_grp = VGroup(formula, result).arrange(DOWN, buff=0.4).next_to(step4, DOWN)
        self.play(
            Transform(step_lbl, step4),
            Transform(data_txt, formula_grp),
        )
        self.wait(2)

        # interpretation
        interp = Text(f"σ = {sigma:.2f}  → every value is ~{sigma:.1f} units from the mean",
                      font_size=22, color=GRAY_A).to_edge(DOWN)
        self.play(FadeIn(interp))
        self.wait(2)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 4 – Stability Comparison (the core message)
# ═══════════════════════════════════════════════════════════════════════════
class StabilityCompareScene(Scene):
    """Side-by-side animated line graphs — low σ vs high σ."""

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("σ and Data Instability", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))

        np.random.seed(7)
        n = 20
        t = np.linspace(0, 1, n)

        low_data  = 10 + np.random.normal(0, 0.6, n)
        high_data = 10 + np.random.normal(0, 4.5, n)

        sig_low  = np.std(low_data)
        sig_high = np.std(high_data)

        ax_kw = dict(
            x_range=[0, n - 1, 5],
            y_range=[0, 22, 5],
            x_length=4.5,
            y_length=3.5,
            axis_config={"color": GRAY, "stroke_width": 1.5, "include_tip": False,
                         "include_numbers": False},
        )

        ax_l = Axes(**ax_kw).shift(LEFT * 3.2 + DOWN * 0.5)
        ax_h = Axes(**ax_kw).shift(RIGHT * 3.2 + DOWN * 0.5)

        lbl_l = VGroup(
            Text(f"Low σ = {sig_low:.2f}", font_size=26, color=C_LOW),
            Text("Stable", font_size=20, color=C_LOW, slant=ITALIC),
        ).arrange(DOWN, buff=0.1).next_to(ax_l, UP, buff=0.15)

        lbl_h = VGroup(
            Text(f"High σ = {sig_high:.2f}", font_size=26, color=C_HIGH),
            Text("Unstable / Chaotic", font_size=20, color=C_HIGH, slant=ITALIC),
        ).arrange(DOWN, buff=0.1).next_to(ax_h, UP, buff=0.15)

        self.play(Create(ax_l), Create(ax_h), FadeIn(lbl_l), FadeIn(lbl_h))

        # plot low σ line
        pts_l = [ax_l.c2p(i, v) for i, v in enumerate(low_data)]
        line_l = VMobject(color=C_LOW, stroke_width=2.5)
        line_l.set_points_as_corners(pts_l)

        # plot high σ line
        pts_h = [ax_h.c2p(i, v) for i, v in enumerate(high_data)]
        line_h = VMobject(color=C_HIGH, stroke_width=2.5)
        line_h.set_points_as_corners(pts_h)

        # mean reference lines
        mean_l = ax_l.plot(lambda x: np.mean(low_data),
                           color=C_MEAN, stroke_width=1, stroke_opacity=0.6)
        mean_h = ax_h.plot(lambda x: np.mean(high_data),
                           color=C_MEAN, stroke_width=1, stroke_opacity=0.6)

        self.play(Create(mean_l), Create(mean_h))
        self.play(Create(line_l), Create(line_h), run_time=2.5)

        # animate dots appearing at each data point
        dots_l = VGroup(*[Dot(p, color=C_LOW,  radius=0.07) for p in pts_l])
        dots_h = VGroup(*[Dot(p, color=C_HIGH, radius=0.07) for p in pts_h])
        self.play(FadeIn(dots_l), FadeIn(dots_h))

        # σ brackets
        brace_l = Brace(ax_l, direction=RIGHT, color=C_LOW, buff=0.05)
        brace_h = Brace(ax_h, direction=RIGHT, color=C_HIGH, buff=0.05)
        self.play(Create(brace_l), Create(brace_h))

        # bottom message
        msg = Text("Higher σ  →  Wider swings  →  Less predictable",
                   font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(msg))
        self.wait(2.5)


# ═══════════════════════════════════════════════════════════════════════════
# SCENE 5 – Real-World Analogy (Stock-like data)
# ═══════════════════════════════════════════════════════════════════════════
class RealWorldScene(Scene):
    """Simulate two 'assets' over time with different volatility."""

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Real-World Impact", font_size=40, color=WHITE)
        subtitle = Text("Two assets — same average return, different volatility",
                        font_size=22, color=GRAY).next_to(title, DOWN, buff=0.15)
        VGroup(title, subtitle).to_edge(UP)
        self.play(Write(title), FadeIn(subtitle))

        np.random.seed(42)
        n = 30
        xs = np.arange(n)

        # asset A: low volatility (σ~1)
        a_returns = np.cumsum(np.random.normal(0.3, 1.0, n)) + 100
        # asset B: high volatility (σ~4)
        b_returns = np.cumsum(np.random.normal(0.3, 4.0, n)) + 100

        ax = Axes(
            x_range=[0, n - 1, 5],
            y_range=[min(min(a_returns), min(b_returns)) - 5,
                     max(max(a_returns), max(b_returns)) + 5, 10],
            x_length=9,
            y_length=4.5,
            axis_config={"color": GRAY, "stroke_width": 1.5, "include_tip": False,
                         "include_numbers": False},
        ).shift(DOWN * 0.4)
        x_lbl = Text("Time",  font_size=22, color=GRAY).next_to(ax.x_axis, DOWN, buff=0.2)
        y_lbl = Text("Value", font_size=22, color=GRAY).next_to(ax.y_axis, LEFT, buff=0.2)
        self.play(Create(ax), Write(x_lbl), Write(y_lbl))

        pts_a = [ax.c2p(i, v) for i, v in zip(xs, a_returns)]
        pts_b = [ax.c2p(i, v) for i, v in zip(xs, b_returns)]

        line_a = VMobject(color=C_LOW,  stroke_width=2.5).set_points_as_corners(pts_a)
        line_b = VMobject(color=C_HIGH, stroke_width=2.5).set_points_as_corners(pts_b)

        leg_a = VGroup(
            Line(ORIGIN, RIGHT * 0.6, color=C_LOW,  stroke_width=3),
            Text(f"Asset A  σ={np.std(np.diff(a_returns)):.1f}  (stable)",
                 font_size=20, color=C_LOW),
        ).arrange(RIGHT, buff=0.15).to_corner(DR).shift(UP * 0.5)

        leg_b = VGroup(
            Line(ORIGIN, RIGHT * 0.6, color=C_HIGH, stroke_width=3),
            Text(f"Asset B  σ={np.std(np.diff(b_returns)):.1f}  (volatile)",
                 font_size=20, color=C_HIGH),
        ).arrange(RIGHT, buff=0.15).next_to(leg_a, UP, buff=0.2)

        self.play(Create(line_a), Create(line_b), run_time=3)
        self.play(FadeIn(leg_a), FadeIn(leg_b))

        # annotation box
        box_txt = Text(
            "Low σ  →  Predictable, lower risk\n"
            "High σ  →  Unpredictable, higher risk",
            font_size=22, color=WHITE,
        )
        box = SurroundingRectangle(box_txt, color=YELLOW, buff=0.2)
        grp = VGroup(box, box_txt).to_edge(DOWN)
        self.play(FadeIn(grp))
        self.wait(3)
