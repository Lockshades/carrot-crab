"""
Theory of Consumer Behaviour — Teaching Edition
================================================
Seven self-contained Manim scenes aligned with the JAMB/UTME syllabus.

No LaTeX required — all math uses Text() with Unicode symbols.
All datasets numerically verified. Scenes connect with breadcrumb sentences.

Scenes:
  UtilityScene              – TU / MU / AU table + dual curves; Law of Diminishing MU
  IndifferenceCurveScene    – 3 ICs + budget line + consumer equilibrium
  CardinalEquilibriumScene  – MUx/Px = MUy/Py dual-column computation table
  BudgetShiftsScene         – income parallel shifts + price pivot illustration
  IncomeSubstitutionScene   – Hicks decomposition A → C → B
  ConsumerSurplusScene      – demand curve + surplus shading + area proof
  DiminishingMUDemandScene  – MU table → demand curve derivation step by step
"""

from manim import *
import numpy as np

# ── palette ───────────────────────────────────────────────────────────────────
C_BG     = "#1a1a2e"
C_TU     = GREEN
C_MU     = YELLOW
C_AU     = BLUE
C_IC1    = "#e74c3c"
C_IC2    = "#f39c12"
C_IC3    = "#2ecc71"
C_BL     = WHITE
C_SHADE  = BLUE
C_DEMAND = "#e74c3c"

# ── verified dataset (Law of Diminishing MU) ─────────────────────────────────
QTY  = [1, 2, 3, 4,  5,  6,  7]
TU   = [10, 18, 24, 28, 30, 30, 28]
MU   = [10,  8,  6,  4,  2,  0, -2]   # TU differences (TU[0] assumed from Q=0 TU=0)
AU   = [10,  9,  8,  7,  6,  5,  4]   # TU / Q


# ═══════════════════════════════════════════════════════════════════════════════
# Shared helper functions (same LaTeX-free pattern as std_dev_viz.py)
# ═══════════════════════════════════════════════════════════════════════════════

def _trow(vals, widths, row_h, accent=YELLOW, is_header=False):
    """One table row: list of (background rect + text) pairs as a VGroup."""
    g  = VGroup()
    x0 = -sum(widths) / 2
    for val, w in zip(vals, widths):
        bg = Rectangle(
            width=w, height=row_h,
            fill_color=accent, fill_opacity=0.18 if is_header else 0.0,
            stroke_color=GRAY, stroke_width=0.65,
        ).move_to([x0 + w / 2, -row_h / 2, 0])
        txt = Text(
            str(val),
            font_size=16 if is_header else 14,
            color=accent if is_header else WHITE,
        ).move_to(bg)
        g.add(bg, txt)
        x0 += w
    return g


def _table(headers, rows, col_widths, row_h=0.38, accent=YELLOW):
    """Stack rows into a VGroup. Each child is a row VGroup."""
    all_rows = VGroup()
    header = _trow(headers, col_widths, row_h, accent=accent, is_header=True)
    all_rows.add(header)
    for row in rows:
        r = _trow(row, col_widths, row_h, accent=accent, is_header=False)
        r.next_to(all_rows, DOWN, buff=0)
        all_rows.add(r)
    return all_rows


def _y_nums(ax, tick_vals, fs=13, color=GRAY):
    """Text tick-labels on the y-axis of an Axes object."""
    g = VGroup()
    for v in tick_vals:
        lbl = Text(str(v), font_size=fs, color=color)
        lbl.next_to(ax.c2p(ax.x_range[0], v), LEFT, buff=0.12)
        g.add(lbl)
    return g


def _x_nums(ax, tick_vals, labels=None, fs=13, color=GRAY):
    """Text tick-labels on the x-axis of an Axes object."""
    g = VGroup()
    for i, v in enumerate(tick_vals):
        lbl = Text(labels[i] if labels else str(v), font_size=fs, color=color)
        lbl.next_to(ax.c2p(v, ax.y_range[0]), DOWN, buff=0.10)
        g.add(lbl)
    return g


def _breadcrumb(text):
    """Dim grey hint at the bottom of the frame linking to next scene."""
    return Text(text, font_size=17, color=GRAY, slant=ITALIC).to_edge(DOWN)


def _axis_label(text, fs=16, color=GRAY):
    return Text(text, font_size=fs, color=color)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 1 — Utility: TU, MU, AU + Diminishing Marginal Utility
# ═══════════════════════════════════════════════════════════════════════════════
class UtilityScene(Scene):
    """
    Step 1 – TU / MU / AU data table built row by row.
    Step 2 – Dual-curve chart: TU rises then flattens; MU falls to zero then negative.
    Concept: Law of Diminishing Marginal Utility.
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Total, Marginal & Average Utility", font_size=36, color=WHITE).to_edge(UP)
        sub   = Text("Law of Diminishing Marginal Utility",
                     font_size=20, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: data table ──────────────────────────────────────────────────
        step1 = Text("Step 1 — Compute TU, MU and AU", font_size=20, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(step1))

        headers = ["Q", "TU", "MU", "AU"]
        widths  = [0.55, 0.60, 0.60, 0.60]
        rows = [
            [str(q), str(tu), str(mu), str(au)]
            for q, tu, mu, au in zip(QTY, TU, MU, AU)
        ]
        tbl = _table(headers, rows, widths, row_h=0.34, accent=YELLOW)

        # colour-code MU column
        for i, row_grp in enumerate(tbl[1:], 0):   # skip header
            mu_val = MU[i]
            # cells at index 4,5 (3rd column = MU)
            colour = C_MU if mu_val > 0 else (RED if mu_val < 0 else GRAY)
            row_grp[4].set_color(colour)  # bg rect tint
            row_grp[5].set_color(colour)  # text

        tbl.scale(0.95).next_to(step1, DOWN, buff=0.20)
        for row in tbl:
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.35)
        self.wait(0.4)

        # callout: MU = 0 at Q=6, negative at Q=7
        callout = Text("MU = 0 at Q = 6  →  saturation point; MU < 0 at Q = 7  →  disutility",
                       font_size=16, color=YELLOW).to_edge(DOWN, buff=0.55)
        box = SurroundingRectangle(tbl[6], color=YELLOW, buff=0.04, corner_radius=0.04)
        self.play(Create(box), Write(callout))
        self.wait(1.5)

        # ── STEP 2: dual curves ─────────────────────────────────────────────────
        step2 = Text("Step 2 — Graphing TU & MU", font_size=20, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.18)
        self.play(
            FadeOut(step1), FadeOut(tbl), FadeOut(box), FadeOut(callout),
            FadeIn(step2),
        )

        # TU axes
        ax_tu = Axes(
            x_range=[0, 8, 1], y_range=[0, 35, 5],
            x_length=5.5, y_length=2.8,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(LEFT * 0.5 + UP * 0.8)

        tu_pts = [(q, tu) for q, tu in zip([0] + QTY, [0] + TU)]
        tu_graph = ax_tu.plot_line_graph(
            [p[0] for p in tu_pts], [p[1] for p in tu_pts],
            line_color=C_TU, vertex_dot_radius=0.05,
        )
        tu_lbl = _axis_label("TU", color=C_TU).next_to(ax_tu, LEFT, buff=0.05).shift(UP * 0.4)
        tu_y   = _y_nums(ax_tu, [0, 10, 20, 30])
        tu_x   = _x_nums(ax_tu, list(range(1, 8)))
        tu_title = Text("Total Utility (TU)", font_size=16, color=C_TU).next_to(ax_tu, UP, buff=0.04)

        # MU axes (below)
        ax_mu = Axes(
            x_range=[0, 8, 1], y_range=[-4, 12, 2],
            x_length=5.5, y_length=2.0,
            axis_config={"include_numbers": False, "include_tip": False},
        ).next_to(ax_tu, DOWN, buff=0.35).align_to(ax_tu, LEFT)

        mu_pts = [(q, mu) for q, mu in zip([0] + QTY, [0] + MU)]
        mu_graph = ax_mu.plot_line_graph(
            [p[0] for p in mu_pts], [p[1] for p in mu_pts],
            line_color=C_MU, vertex_dot_radius=0.05,
        )
        zero_line = DashedLine(
            ax_mu.c2p(0, 0), ax_mu.c2p(8, 0),
            color=GRAY, stroke_width=1.2, dash_length=0.10,
        )
        mu_y  = _y_nums(ax_mu, [-2, 0, 5, 10])
        mu_x  = _x_nums(ax_mu, list(range(1, 8)))
        mu_title = Text("Marginal Utility (MU)", font_size=16, color=C_MU).next_to(ax_mu, DOWN, buff=0.04)

        chart_grp = VGroup(ax_tu, tu_graph, tu_y, tu_x, tu_title, tu_lbl,
                           ax_mu, mu_graph, zero_line, mu_y, mu_x, mu_title)
        chart_grp.shift(RIGHT * 0.6)

        self.play(Create(ax_tu), Create(ax_mu), FadeIn(tu_y), FadeIn(mu_y),
                  FadeIn(tu_x), FadeIn(mu_x), run_time=0.7)
        self.play(Create(tu_graph["line_graph"]), Write(tu_title), Write(tu_lbl))
        self.play(Create(mu_graph["line_graph"]), Create(zero_line), Write(mu_title))

        # annotation: TU max and MU=0 align
        dot_tu_max = Dot(ax_tu.c2p(6, 30), color=WHITE, radius=0.08)
        dot_mu_zero = Dot(ax_mu.c2p(6, 0), color=WHITE, radius=0.08)
        v_dash = DashedLine(ax_tu.c2p(6, 30), ax_mu.c2p(6, 0), color=WHITE, stroke_width=1)
        note = Text("TU is max when MU = 0  (Q = 6)", font_size=15, color=WHITE).to_edge(RIGHT).shift(UP * 0.3)
        self.play(FadeIn(dot_tu_max), FadeIn(dot_mu_zero), Create(v_dash), Write(note))
        self.wait(1.8)

        crumb = _breadcrumb("Next: Indifference Curves — choosing between two goods simultaneously")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 2 — Indifference Curves + Budget Line + Equilibrium
# ═══════════════════════════════════════════════════════════════════════════════
class IndifferenceCurveScene(Scene):
    """
    Step 1 – Budget constraint data table (Px=2, Py=1, I=12).
    Step 2 – Three ICs (U=12, 18, 24) + budget line + equilibrium point.
    Concept: Consumer reaches highest reachable IC.
    """

    # Px=2, Py=1, I=12
    # Budget: 2x + y = 12  →  y = 12 - 2x
    # Equilibrium: MRS = Px/Py = 2  → on U=xy: MRS = y/x = 2 → y=2x; and 2x+y=12 → x=3, y=6

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Indifference Curves & Consumer Equilibrium", font_size=33, color=WHITE).to_edge(UP)
        sub   = Text("Px = 2,  Py = 1,  Income = ₦12",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: budget table ────────────────────────────────────────────────
        step1 = Text("Step 1 — Budget combinations (y = 12 − 2x)", font_size=19, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(step1))

        brows = [(str(x), str(12 - 2*x)) for x in range(0, 7)]
        btbl  = _table(["Qty X", "Qty Y"], brows, [0.70, 0.70], row_h=0.33, accent=YELLOW)
        btbl.scale(0.95).next_to(step1, DOWN, buff=0.18)
        self.play(FadeIn(btbl))
        self.wait(1.0)

        # ── STEP 2: IC map ──────────────────────────────────────────────────────
        step2 = Text("Step 2 — Indifference Map + Budget Line", font_size=19, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.18)
        self.play(FadeOut(step1), FadeOut(btbl), FadeIn(step2))

        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 20, 2],
            x_length=5.8, y_length=4.5,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(RIGHT * 0.8 + DOWN * 0.4)

        x_lbl = _axis_label("Qty of Good X").next_to(ax, DOWN, buff=0.05)
        y_lbl = _axis_label("Qty of Good Y").next_to(ax, LEFT, buff=0.05).rotate(PI/2)
        x_tks = _x_nums(ax, list(range(1, 10)))
        y_tks = _y_nums(ax, [2, 4, 6, 8, 10, 12, 14, 16, 18])

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_tks), FadeIn(y_tks))

        # IC curves: y = U/x
        ic_data = [(12, C_IC1, "U₁=12"), (18, C_IC2, "U₂=18"), (24, C_IC3, "U₃=24")]
        for U, colour, label in ic_data:
            ic = ax.plot(lambda x, U=U: U / x, x_range=[U/18.5, 9.5], color=colour, stroke_width=2)
            ic_lbl = Text(label, font_size=15, color=colour)
            ic_lbl.next_to(ax.c2p(9.3, U/9.3), RIGHT, buff=0.06)
            self.play(Create(ic), Write(ic_lbl), run_time=0.55)

        # budget line: y = 12 - 2x
        bl = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=C_BL, stroke_width=2)
        bl_lbl = Text("Budget Line\n2x+y=12", font_size=14, color=WHITE)
        bl_lbl.next_to(ax.c2p(0.3, 11), RIGHT, buff=0.06)
        self.play(Create(bl), Write(bl_lbl), run_time=0.55)

        # equilibrium E (3, 6)
        eq_dot = Dot(ax.c2p(3, 6), color=WHITE, radius=0.10)
        eq_lbl = Text("E (3, 6)\nEquilibrium", font_size=14, color=WHITE)
        eq_lbl.next_to(ax.c2p(3, 6), UR, buff=0.12)
        self.play(FadeIn(eq_dot), Write(eq_lbl))

        note = Text("MRS = Px/Py = 2  →  Consumer maximises utility on U₂",
                    font_size=16, color=YELLOW).to_edge(DOWN, buff=0.55)
        self.play(Write(note))
        self.wait(1.8)

        crumb = _breadcrumb("Next: Cardinal Equilibrium — exact MU/P ratios")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 3 — Cardinal Equilibrium: MUx/Px = MUy/Py
# ═══════════════════════════════════════════════════════════════════════════════
class CardinalEquilibriumScene(Scene):
    """
    Step 1 – Separate MUx/Px and MUy/Py tables (Px=2, Py=1, I=10).
    Step 2 – Highlight the matching ratio; confirm budget is exhausted.
    Concept: Cardinal utility — equi-marginal principle.

    Verified:
      Px=2, Py=1, I=10
      MUx at x=1..5: 20,16,12,8,4   → MUx/Px: 10,8,6,4,2
      MUy at y=1..5: 6,5,4,3,2      → MUy/Py: 6,5,4,3,2
      Equilibrium: MUx/Px = MUy/Py = 6  → x=3, y=4  → spend: 2×3+1×4=10 ✓
    """

    MUX = [20, 16, 12,  8, 4]
    MUY = [ 6,  5,  4,  3, 2]
    PX  = 2
    PY  = 1

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Cardinal Equilibrium  —  Equi-Marginal Principle", font_size=32, color=WHITE).to_edge(UP)
        sub   = Text("Px = 2,  Py = 1,  Income = ₦10",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── formula banner ──────────────────────────────────────────────────────
        formula = Text("Equilibrium:  MUx / Px  =  MUy / Py  =  λ",
                       font_size=20, color=YELLOW).next_to(sub, DOWN, buff=0.15)
        self.play(FadeIn(formula))

        # ── STEP 1: dual tables ─────────────────────────────────────────────────
        step1 = Text("Step 1 — Compute MU/P ratios", font_size=19, color=YELLOW)
        step1.next_to(formula, DOWN, buff=0.15)
        self.play(FadeIn(step1))

        # Good X table
        x_rows = [
            [str(i+1), str(mx), f"{mx}/{self.PX}", str(mx//self.PX)]
            for i, mx in enumerate(self.MUX)
        ]
        x_tbl = _table(["Qx", "MUx", "MUx/Px", "λx"], x_rows,
                        [0.50, 0.65, 0.72, 0.55], row_h=0.36, accent=C_IC3)

        # Good Y table
        y_rows = [
            [str(i+1), str(my), f"{my}/{self.PY}", str(my//self.PY)]
            for i, my in enumerate(self.MUY)
        ]
        y_tbl = _table(["Qy", "MUy", "MUy/Py", "λy"], y_rows,
                        [0.50, 0.65, 0.72, 0.55], row_h=0.36, accent=C_IC2)

        dual = VGroup(
            VGroup(Text("Good X  (Px=2)", font_size=16, color=C_IC3), x_tbl).arrange(DOWN, buff=0.08),
            VGroup(Text("Good Y  (Py=1)", font_size=16, color=C_IC2), y_tbl).arrange(DOWN, buff=0.08),
        ).arrange(RIGHT, buff=0.60).next_to(step1, DOWN, buff=0.18)

        for col in dual:
            self.play(FadeIn(col, shift=UP * 0.1), run_time=0.6)

        # ── STEP 2: highlight equilibrium rows ──────────────────────────────────
        # x=3 → row index 3 in x_tbl; y=4 → row index 4 in y_tbl
        eq_x_row = x_tbl[3]   # 0=header, 1=Qx=1, 2=Qx=2, 3=Qx=3
        eq_y_row = y_tbl[4]   # 0=header, 1=Qy=1, 2=Qy=2, 3=Qy=3, 4=Qy=4

        box_x = SurroundingRectangle(eq_x_row, color=YELLOW, buff=0.04, corner_radius=0.04)
        box_y = SurroundingRectangle(eq_y_row, color=YELLOW, buff=0.04, corner_radius=0.04)
        self.play(Create(box_x), Create(box_y))

        result = Text(
            "At Qx=3, Qy=4:  MUx/Px = MUy/Py = 6  and  2×3 + 1×4 = 10 = Income  ✓",
            font_size=16, color=YELLOW,
        ).to_edge(DOWN, buff=0.55)
        self.play(Write(result))
        self.wait(2.0)

        crumb = _breadcrumb("Next: Budget Shifts — what happens when income or price changes?")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 4 — Budget Line Shifts: Income & Price Changes
# ═══════════════════════════════════════════════════════════════════════════════
class BudgetShiftsScene(Scene):
    """
    Step 1 – Show budget table for base case (Px=2, Py=1, I=12).
    Step 2 – Income rise to I=18 and fall to I=8 → parallel shifts.
    Step 3 – Price of X falls to Px=1 → pivot (x-intercept doubles).
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Budget Line Shifts", font_size=38, color=WHITE).to_edge(UP)
        sub   = Text("Income changes → parallel shift  |  Price changes → pivot",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: base table ──────────────────────────────────────────────────
        step1 = Text("Step 1 — Base Budget  (Px=2, Py=1, I=12)", font_size=19, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(step1))

        brows = [(str(x), str(12 - 2*x)) for x in range(0, 7)]
        btbl  = _table(["Qty X", "Qty Y"], brows, [0.70, 0.70], row_h=0.32, accent=YELLOW)
        btbl.next_to(step1, DOWN, buff=0.18)
        self.play(FadeIn(btbl))
        self.wait(1.0)

        # ── STEP 2: axes + budget line animation ────────────────────────────────
        step2 = Text("Step 2 & 3 — Graphing the Shifts", font_size=19, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.18)
        self.play(FadeOut(step1), FadeOut(btbl), FadeIn(step2))

        ax = Axes(
            x_range=[0, 12, 2], y_range=[0, 20, 4],
            x_length=6.0, y_length=4.2,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(RIGHT * 0.5 + DOWN * 0.4)

        x_lbl = _axis_label("Qty X").next_to(ax, DOWN, buff=0.05)
        y_lbl = _axis_label("Qty Y").next_to(ax, LEFT, buff=0.05).rotate(PI/2)
        x_tks = _x_nums(ax, [2, 4, 6, 8, 10, 12])
        y_tks = _y_nums(ax, [4, 8, 12, 16, 18])
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_tks), FadeIn(y_tks))

        # base BL: y = 12 - 2x  (x: 0..6)
        bl_base = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=WHITE, stroke_width=2.5)
        lbl_base = Text("I=12 (Base)", font_size=14, color=WHITE).next_to(ax.c2p(0.3, 11.5), RIGHT, buff=0.06)
        self.play(Create(bl_base), Write(lbl_base))
        self.wait(0.5)

        # income rise: y = 18 - 2x  (x: 0..9)
        bl_up = ax.plot(lambda x: 18 - 2*x, x_range=[0, 9], color=C_IC3, stroke_width=2, stroke_opacity=0.9)
        lbl_up = Text("I=18 (Higher)", font_size=14, color=C_IC3).next_to(ax.c2p(0.3, 17.5), RIGHT, buff=0.06)
        self.play(Create(bl_up), Write(lbl_up))

        # income fall: y = 8 - 2x  (x: 0..4)
        bl_dn = ax.plot(lambda x: 8 - 2*x, x_range=[0, 4], color=C_IC1, stroke_width=2, stroke_opacity=0.9)
        lbl_dn = Text("I=8 (Lower)", font_size=14, color=C_IC1).next_to(ax.c2p(0.3, 7.5), RIGHT, buff=0.06)
        self.play(Create(bl_dn), Write(lbl_dn))

        note1 = Text("Income change → parallel shift (same slope)", font_size=15, color=YELLOW).to_edge(DOWN, buff=0.55)
        self.play(Write(note1))
        self.wait(1.2)

        # price pivot: Px=1 (halved) → y = 12 - x (x: 0..12)
        bl_px = ax.plot(lambda x: 12 - x, x_range=[0, 12], color=C_IC2, stroke_width=2,
                        stroke_opacity=0.9)
        lbl_px = Text("Px=1 (Pivot)", font_size=14, color=C_IC2).next_to(ax.c2p(9, 3), UR, buff=0.06)
        self.play(Create(bl_px), Write(lbl_px))

        note2 = Text("Px falls → x-intercept moves right; y-intercept unchanged → pivot",
                     font_size=15, color=C_IC2).to_edge(DOWN, buff=0.55)
        self.play(ReplacementTransform(note1, note2))
        self.wait(1.8)

        crumb = _breadcrumb("Next: Income & Substitution Effects — breaking down a price change")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 5 — Income & Substitution Effects (Hicks Decomposition)
# ═══════════════════════════════════════════════════════════════════════════════
class IncomeSubstitutionScene(Scene):
    """
    Step 1 – Summary table: Points A, C, B with coordinates and effects.
    Step 2 – Graph showing A→C (Substitution Effect) and C→B (Income Effect).

    Data (U = x·y, Px falls from 2 → 1, Py=1, I=12):
      A = (3,  6)   original equilibrium on U=18
      C = (√18, √18) ≈ (4.24, 4.24)  same IC after price fall, Hicks compensated BL
      B = (6,  6)   new equilibrium on U=36 with new BL (Px=1, I=12)

      SE = Cx − Ax = 4.24 − 3 ≈ +1.24   (more X due to cheaper price)
      IE = Bx − Cx = 6 − 4.24 ≈ +1.76   (more X due to higher real income)
      TE = Bx − Ax = 6 − 3 = +3          (total: buy 3 more units of X)
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Income & Substitution Effects (Hicks)", font_size=34, color=WHITE).to_edge(UP)
        sub   = Text("Px falls: 2 → 1  |  Py=1  |  I=12",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: summary table ───────────────────────────────────────────────
        step1 = Text("Step 1 — Decomposition Summary Table", font_size=19, color=YELLOW)
        step1.next_to(sub, DOWN, buff=0.15)
        self.play(FadeIn(step1))

        tbl = _table(
            headers=["Point", "Qx", "Qy", "On IC", "Meaning"],
            rows=[
                ["A", "3",    "6",    "U=18", "Original equilibrium"],
                ["C", "4.24", "4.24", "U=18", "Compensated (SE only)"],
                ["B", "6",    "6",    "U=36", "New equilibrium"],
            ],
            col_widths=[0.55, 0.50, 0.50, 0.65, 2.20],
            row_h=0.36, accent=YELLOW,
        )
        eff_tbl = _table(
            headers=["Effect", "ΔQx", "Interpretation"],
            rows=[
                ["Substitution (SE)", "+1.24", "A → C  (Px cheaper, stay on U=18)"],
                ["Income (IE)",       "+1.76", "C → B  (higher real income)"],
                ["Total (TE)",        "+3.00", "A → B  (SE + IE)"],
            ],
            col_widths=[1.50, 0.65, 2.50],
            row_h=0.36, accent=C_MU,
        )
        VGroup(tbl, eff_tbl).arrange(DOWN, buff=0.25).next_to(step1, DOWN, buff=0.18)
        self.play(FadeIn(tbl), run_time=0.6)
        self.play(FadeIn(eff_tbl), run_time=0.6)
        self.wait(1.2)

        # ── STEP 2: graph ───────────────────────────────────────────────────────
        step2 = Text("Step 2 — Graph: A → C → B", font_size=19, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.15)
        self.play(FadeOut(step1), FadeOut(tbl), FadeOut(eff_tbl), FadeIn(step2))

        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 14, 2],
            x_length=5.8, y_length=4.2,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(RIGHT * 0.5 + DOWN * 0.4)

        x_lbl = _axis_label("Qty X").next_to(ax, DOWN, buff=0.05)
        y_lbl = _axis_label("Qty Y").next_to(ax, LEFT, buff=0.05).rotate(PI/2)
        x_tks = _x_nums(ax, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        y_tks = _y_nums(ax, [2, 4, 6, 8, 10, 12])
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_tks), FadeIn(y_tks))

        # ICs
        ic18 = ax.plot(lambda x: 18/x, x_range=[1.3, 9.5], color=C_IC2, stroke_width=2)
        ic36 = ax.plot(lambda x: 36/x, x_range=[2.6, 9.5], color=C_IC3, stroke_width=2)
        lbl18 = Text("U=18", font_size=13, color=C_IC2).next_to(ax.c2p(9.3, 18/9.3), RIGHT, buff=0.04)
        lbl36 = Text("U=36", font_size=13, color=C_IC3).next_to(ax.c2p(9.3, 36/9.3), RIGHT, buff=0.04)
        self.play(Create(ic18), Create(ic36), Write(lbl18), Write(lbl36))

        # Budget lines
        # Original BL: Px=2, I=12 → y=12-2x (x:0..6)
        bl_orig = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=C_IC1, stroke_width=1.8)
        # Compensated BL (same slope as new BL but tangent to U=18): Px=1
        # compensated income needed: MRS = Px/Py=1, on U=18: y/x=1→x=y; xy=18→x=y=√18≈4.24
        # compensated I = 1*4.24+1*4.24 = 8.49
        bl_comp = ax.plot(lambda x: 8.49 - x, x_range=[0, 8.49], color=GRAY, stroke_width=1.5,
                          stroke_opacity=0.7)
        # New BL: Px=1, I=12 → y=12-x (x:0..12)
        bl_new = ax.plot(lambda x: 12 - x, x_range=[0, 12], color=WHITE, stroke_width=1.8)

        self.play(Create(bl_orig), Create(bl_comp), Create(bl_new))
        lbl_comp = Text("Comp. BL", font_size=12, color=GRAY).next_to(ax.c2p(8, 0.49), UR, buff=0.04)
        lbl_new  = Text("New BL", font_size=12, color=WHITE).next_to(ax.c2p(10, 2.0), UR, buff=0.04)
        self.play(Write(lbl_comp), Write(lbl_new))

        # Points A, C, B
        pt_A = Dot(ax.c2p(3, 6), color=C_IC1, radius=0.09)
        pt_C = Dot(ax.c2p(4.24, 4.24), color=GRAY, radius=0.09)
        pt_B = Dot(ax.c2p(6, 6), color=C_IC3, radius=0.09)
        lA = Text("A(3,6)", font_size=13, color=C_IC1).next_to(ax.c2p(3, 6), UL, buff=0.06)
        lC = Text("C(4.24,4.24)", font_size=12, color=GRAY).next_to(ax.c2p(4.24, 4.24), DR, buff=0.06)
        lB = Text("B(6,6)", font_size=13, color=C_IC3).next_to(ax.c2p(6, 6), UR, buff=0.06)
        self.play(FadeIn(pt_A), FadeIn(pt_C), FadeIn(pt_B),
                  Write(lA), Write(lC), Write(lB))

        # SE and IE arrows
        arr_SE = Arrow(ax.c2p(3, 0.3), ax.c2p(4.24, 0.3), color=C_MU,
                       buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        arr_IE = Arrow(ax.c2p(4.24, 0.3), ax.c2p(6, 0.3), color=C_IC3,
                       buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        se_lbl = Text("SE +1.24", font_size=12, color=C_MU).next_to(arr_SE, DOWN, buff=0.05)
        ie_lbl = Text("IE +1.76", font_size=12, color=C_IC3).next_to(arr_IE, DOWN, buff=0.05)
        self.play(Create(arr_SE), Write(se_lbl))
        self.play(Create(arr_IE), Write(ie_lbl))

        final = Text("TE = SE + IE = 1.24 + 1.76 = 3.00 units", font_size=15, color=YELLOW).to_edge(DOWN, buff=0.55)
        self.play(Write(final))
        self.wait(1.8)

        crumb = _breadcrumb("Next: Consumer Surplus — value above what you pay")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 6 — Consumer Surplus
# ═══════════════════════════════════════════════════════════════════════════════
class ConsumerSurplusScene(Scene):
    """
    Step 1 – Data table: price-quantity schedule + CS per unit.
    Step 2 – Demand curve + horizontal price line + shaded CS triangle.

    Demand: P = 12 − Q
    Market price P* = 4  →  Q* = 8
    CS = ½ × base × height = ½ × 8 × (12−4) = ½ × 8 × 8 = 32
    """

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Consumer Surplus", font_size=40, color=WHITE).to_edge(UP)
        sub   = Text("Demand: P = 12 − Q  |  Market price P* = ₦4",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: data table ──────────────────────────────────────────────────
        step1 = Text("Step 1 — Price-Quantity Schedule & Consumer Surplus per Unit",
                     font_size=18, color=YELLOW).next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(step1))

        P_star = 4
        rows = []
        for q in range(1, 9):
            p_will = 12 - q
            cs_unit = p_will - P_star
            rows.append([str(q), f"₦{p_will}", f"₦{P_star}", f"₦{cs_unit}"])

        tbl = _table(
            headers=["Q", "Max Willingness (P)", "Market P*", "CS per unit"],
            rows=rows,
            col_widths=[0.45, 1.65, 0.90, 0.90],
            row_h=0.33, accent=YELLOW,
        )
        tbl.scale(0.90).next_to(step1, DOWN, buff=0.15)
        self.play(FadeIn(tbl))

        total_note = Text("Total CS = ½ × 8 × 8 = ₦32  (triangle area)", font_size=16, color=YELLOW)
        total_note.to_edge(DOWN, buff=0.55)
        self.play(Write(total_note))
        self.wait(1.2)

        # ── STEP 2: demand curve + shading ─────────────────────────────────────
        step2 = Text("Step 2 — Consumer Surplus on Graph", font_size=19, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.18)
        self.play(FadeOut(step1), FadeOut(tbl), FadeOut(total_note), FadeIn(step2))

        ax = Axes(
            x_range=[0, 12, 1], y_range=[0, 14, 2],
            x_length=5.8, y_length=4.2,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(RIGHT * 0.4 + DOWN * 0.4)

        x_lbl = _axis_label("Quantity (Q)").next_to(ax, DOWN, buff=0.05)
        y_lbl = _axis_label("Price (P)").next_to(ax, LEFT, buff=0.05).rotate(PI/2)
        x_tks = _x_nums(ax, list(range(0, 11, 2)))
        y_tks = _y_nums(ax, [2, 4, 6, 8, 10, 12])
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_tks), FadeIn(y_tks))

        demand = ax.plot(lambda q: 12 - q, x_range=[0, 11], color=C_DEMAND, stroke_width=2.5)
        d_lbl  = Text("D: P=12-Q", font_size=15, color=C_DEMAND).next_to(ax.c2p(0.3, 11.5), RIGHT, buff=0.06)
        self.play(Create(demand), Write(d_lbl))

        # price line P*=4
        p_line = ax.plot(lambda q: 4, x_range=[0, 11], color=WHITE, stroke_width=1.8,
                         stroke_opacity=0.8)
        p_lbl  = Text("P*=4", font_size=14, color=WHITE).next_to(ax.c2p(0, 4), LEFT, buff=0.06)
        self.play(Create(p_line), Write(p_lbl))

        # Q* = 8 vertical dashed line
        q_line = DashedLine(ax.c2p(8, 0), ax.c2p(8, 4), color=GRAY, stroke_width=1.2)
        q_lbl  = Text("Q*=8", font_size=13, color=GRAY).next_to(ax.c2p(8, 0), DOWN, buff=0.10)
        self.play(Create(q_line), Write(q_lbl))

        # shade CS triangle using polygon
        cs_poly = Polygon(
            ax.c2p(0, 12),   # top of demand (intercept)
            ax.c2p(8, 4),    # equilibrium point
            ax.c2p(0, 4),    # left on price line
            color=C_SHADE, fill_color=C_SHADE, fill_opacity=0.35, stroke_width=0,
        )
        self.play(FadeIn(cs_poly))

        cs_text = Text("CS = ₦32", font_size=18, color=C_SHADE).move_to(ax.c2p(2.0, 8))
        self.play(Write(cs_text))

        note = Text("Consumer Surplus = area where willingness to pay > market price",
                    font_size=15, color=YELLOW).to_edge(DOWN, buff=0.55)
        self.play(Write(note))
        self.wait(1.8)

        crumb = _breadcrumb("Next: From Diminishing MU to the Demand Curve — connecting the two laws")
        self.play(FadeIn(crumb))
        self.wait(1.2)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 7 — From Diminishing MU to the Demand Curve
# ═══════════════════════════════════════════════════════════════════════════════
class DiminishingMUDemandScene(Scene):
    """
    Step 1 – MU table (same data as Scene 1) — price a consumer is willing to pay.
    Step 2 – Plot MU as a downward-sloping demand curve.
    Concept: The demand curve IS the MU curve (willingness to pay).
    """

    # Assume MU represents willingness to pay (₦ per unit)
    WTP = [10, 8, 6, 4, 2, 0]   # at Q=1..6 (Q=7 excluded: negative WTP)

    def construct(self):
        self.camera.background_color = C_BG

        title = Text("Diminishing MU  →  The Demand Curve", font_size=34, color=WHITE).to_edge(UP)
        sub   = Text("MU = Marginal Utility = Willingness to Pay",
                     font_size=19, color=GRAY, slant=ITALIC).next_to(title, DOWN, buff=0.08)
        self.play(Write(title), FadeIn(sub))

        # ── STEP 1: MU as WTP table ─────────────────────────────────────────────
        step1 = Text("Step 1 — MU = Max Price Consumer Will Pay Per Unit",
                     font_size=18, color=YELLOW).next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(step1))

        rows = [[str(q), f"₦{mu}"] for q, mu in zip(range(1, 7), self.WTP)]
        tbl = _table(
            headers=["Qty (Q)", "MU / Willingness to Pay (₦)"],
            rows=rows,
            col_widths=[0.70, 2.20],
            row_h=0.36, accent=C_MU,
        )
        tbl.next_to(step1, DOWN, buff=0.18)

        for row in tbl:
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.30)

        note1 = Text("As Q rises, MU falls — each extra unit is worth less",
                     font_size=15, color=YELLOW).to_edge(DOWN, buff=0.55)
        self.play(Write(note1))
        self.wait(1.0)

        # ── STEP 2: demand curve from MU ───────────────────────────────────────
        step2 = Text("Step 2 — MU Becomes the Demand Curve", font_size=19, color=YELLOW)
        step2.next_to(sub, DOWN, buff=0.18)
        self.play(FadeOut(step1), FadeOut(tbl), FadeOut(note1), FadeIn(step2))

        ax = Axes(
            x_range=[0, 8, 1], y_range=[0, 12, 2],
            x_length=5.8, y_length=4.0,
            axis_config={"include_numbers": False, "include_tip": False},
        ).shift(RIGHT * 0.5 + DOWN * 0.4)

        x_lbl = _axis_label("Quantity (Q)").next_to(ax, DOWN, buff=0.05)
        y_lbl = _axis_label("Price / MU (₦)").next_to(ax, LEFT, buff=0.05).rotate(PI/2)
        x_tks = _x_nums(ax, list(range(1, 8)))
        y_tks = _y_nums(ax, [0, 2, 4, 6, 8, 10])
        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_tks), FadeIn(y_tks))

        # plot MU/demand stepwise then smooth line
        pts_x = [0] + list(range(1, 7))
        pts_y = [10] + self.WTP        # extended to Q=0 at MU=10 (y-intercept)

        demand_curve = ax.plot_line_graph(
            pts_x, pts_y,
            line_color=C_DEMAND, vertex_dot_radius=0.07,
        )
        self.play(Create(demand_curve["line_graph"]), run_time=1.0)
        self.play(FadeIn(demand_curve["vertex_dots"]))

        d_lbl = Text("D = MU Curve", font_size=15, color=C_DEMAND).next_to(ax.c2p(5.5, 2.5), RIGHT, buff=0.06)
        self.play(Write(d_lbl))

        # label each dot
        for q, mu in zip(range(1, 7), self.WTP):
            dot_lbl = Text(f"({q},{mu})", font_size=11, color=GRAY)
            dot_lbl.next_to(ax.c2p(q, mu), UR, buff=0.04)
            self.add(dot_lbl)

        final = Text(
            "Law of Demand follows directly from Diminishing Marginal Utility",
            font_size=16, color=YELLOW,
        ).to_edge(DOWN, buff=0.55)
        self.play(Write(final))
        self.wait(2.0)

        crumb = _breadcrumb("End of Consumer Behaviour series. Review: Utility → IC → Equilibrium → Surplus")
        self.play(FadeIn(crumb))
        self.wait(1.5)
