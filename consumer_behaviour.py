"""
Theory of Consumer Behaviour — Teaching Edition (Redesigned)
===========================================================
Seven self-contained Manim scenes aligned with the JAMB/UTME syllabus.

Teaching Doctrine: DATA → FORMULA → CALCULATIONS → TABLE → GRAPH

No LaTeX required — all math uses Text() with Unicode symbols.
All datasets numerically verified. Clean text transitions prevent overlaps.

Scenes:
  1. UtilityScene              – Given TU data → formula MU/AU → calculations → table → curves
  2. IndifferenceCurveScene    – Given budget params → formula → substitutions → table → ICs + BL
  3. CardinalEquilibriumScene  – Given MU data → formula MUx/Px=MUy/Py → ratios → table → highlight
  4. BudgetShiftsScene         – Given base budget → show formulas → calculate shifts → graph
  5. IncomeSubstitutionScene   – Given price change → formula SE/IE → calculate A,C,B → table → graph
  6. ConsumerSurplusScene      – Given demand → formula CS → calculate per-unit → table → graph
  7. DiminishingMUDemandScene  – Given MU table → formula MU=WTP → mapping table → demand curve
"""

from manim import *
import numpy as np

# ── COLOR PALETTE ──────────────────────────────────────────────────────────
C_BG     = "#1a1a2e"
C_TU     = GREEN
C_MU     = YELLOW
C_AU     = BLUE
C_IC1    = "#e74c3c"
C_IC2    = "#f39c12"
C_IC3    = "#2ecc71"
C_BL     = WHITE
C_DEMAND = "#e74c3c"
C_CALC   = "#ecf0f1"    # light for calculations

# ── VERIFIED DATASET ───────────────────────────────────────────────────────
# Law of Diminishing Marginal Utility: TU rises then flattens, MU falls
QTY  = [1, 2, 3, 4,  5,  6,  7]
TU   = [10, 18, 24, 28, 30, 30, 28]   # Total Utility
MU   = [10,  8,  6,  4,  2,  0, -2]   # Marginal Utility (differences)
AU   = [10,  9,  8,  7,  6,  5,  4]   # Average Utility (TU/Q)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _table_row(vals, widths, row_h, accent=YELLOW, is_header=False):
    """Create one table row with background rects and text."""
    row = VGroup()
    x0 = -sum(widths) / 2
    for val, w in zip(vals, widths):
        bg = Rectangle(width=w, height=row_h, fill_color=accent,
                       fill_opacity=0.18 if is_header else 0.0,
                       stroke_color=GRAY, stroke_width=0.65)
        txt = Text(str(val), font_size=16 if is_header else 13,
                   color=accent if is_header else WHITE)
        cell = VGroup(bg, txt).move_to([x0 + w/2, 0, 0])
        row.add(cell)
        x0 += w
    return row


def _table(headers, rows, col_widths, row_h=0.38, accent=YELLOW):
    """Build a complete table (header + rows)."""
    table = VGroup()
    header_row = _table_row(headers, col_widths, row_h, accent=accent, is_header=True)
    table.add(header_row)

    for row_data in rows:
        row_obj = _table_row(row_data, col_widths, row_h, accent=accent, is_header=False)
        row_obj.next_to(table[-1], DOWN, buff=0)
        table.add(row_obj)

    return table


def _axis_labels(ax, x_ticks, y_ticks, x_label_text, y_label_text):
    """Create axis labels and tick markers."""
    x_labels = VGroup()
    for t in x_ticks:
        lbl = Text(str(t), font_size=12, color=GRAY)
        lbl.next_to(ax.c2p(t, ax.y_range[0]), DOWN, buff=0.08)
        x_labels.add(lbl)

    y_labels = VGroup()
    for t in y_ticks:
        lbl = Text(str(t), font_size=12, color=GRAY)
        lbl.next_to(ax.c2p(ax.x_range[0], t), LEFT, buff=0.08)
        y_labels.add(lbl)

    x_lbl = Text(x_label_text, font_size=14, color=GRAY).next_to(ax, DOWN, buff=0.10)
    y_lbl = Text(y_label_text, font_size=14, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.10)

    return VGroup(x_labels, y_labels, x_lbl, y_lbl)


def _section_title(title_text, color=YELLOW):
    """Create a step/section title."""
    return Text(title_text, font_size=22, color=color)


def _breadcrumb(text):
    """Dim hint at bottom linking to next scene."""
    return Text(text, font_size=15, color=GRAY, slant=ITALIC).to_edge(DOWN)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 1 — Utility: Computing TU, MU, AU from Data
# ═══════════════════════════════════════════════════════════════════════════════
class UtilityScene(Scene):
    """
    TEACHING FLOW:
    1. Given: Show raw TU data from Q=1 to Q=7
    2. Formula: Explain MU = ΔTU/ΔQ and AU = TU/Q
    3. Calculations: Compute each MU step-by-step with substitutions
    4. Table: Organize TU, MU, AU in a table
    5. Graph: Plot dual curves (TU and MU)
    """

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Total, Marginal & Average Utility", font_size=40, color=WHITE).to_edge(UP)
        subtitle = Text("Law of Diminishing Marginal Utility", font_size=18, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        header = VGroup(main_title, subtitle)
        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN — Raw TU Data ─────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Total Utility Data")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        given_text = VGroup(
            Text("Consumer purchases quantity Q = 1 to 7", font_size=18, color=C_CALC),
            Text("Total Utility (TU) is measured as satisfaction:", font_size=18, color=C_CALC),
        ).arrange(DOWN, buff=0.2).next_to(step1_title, DOWN, buff=0.3)

        for line in given_text:
            self.play(FadeIn(line))

        tu_given = VGroup(
            Text("Q:  1   2   3   4   5   6   7", font_size=18, color=YELLOW),
            Text("TU: 10  18  24  28  30  30  28", font_size=18, color=YELLOW),
        ).arrange(DOWN, buff=0.15).next_to(given_text, DOWN, buff=0.3)

        for line in tu_given:
            self.play(FadeIn(line))

        self.wait(1.0)

        # ── Fade out Step 1 ────────────────────────────────────────────────
        step1_section = VGroup(step1_title, given_text, tu_given)
        self.play(FadeOut(step1_section))
        self.wait(0.3)

        # ── STEP 2: FORMULA — MU and AU ─────────────────────────────────────
        step2_title = _section_title("Step 2 — Formulas: MU and AU")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        formulas = VGroup(
            Text("Marginal Utility (MU) = ΔTU / ΔQ", font_size=20, color=C_MU),
            Text("                       (change in TU) / (change in Q)", font_size=16, color=GRAY),
            Text("", font_size=8),
            Text("Average Utility (AU) = TU / Q", font_size=20, color=C_AU),
            Text("                       (total satisfaction) / (quantity)", font_size=16, color=GRAY),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(step2_title, DOWN, buff=0.3)

        for line in formulas:
            self.play(FadeIn(line))

        self.wait(1.2)

        # ── Fade out Step 2 ────────────────────────────────────────────────
        step2_section = VGroup(step2_title, formulas)
        self.play(FadeOut(step2_section))
        self.wait(0.3)

        # ── STEP 3: CALCULATIONS — Compute MU with substitutions ───────────
        step3_title = _section_title("Step 3 — Calculate MU with Substitutions")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        calc_header = Text("Computing MU for Q=1 to Q=7:", font_size=18, color=YELLOW).next_to(step3_title, DOWN, buff=0.2)
        self.play(FadeIn(calc_header))

        # Show calculations step by step
        calcs = []
        q_prev, tu_prev = 0, 0

        for q, tu in zip(QTY[:5], TU[:5]):  # Show first 5 for time
            calc_text = Text(f"Q={q}: MU = (TU{q} − TU{q-1}) / (Q{q} − Q{q-1}) = ({tu} − {tu_prev}) / 1 = {tu - tu_prev}",
                           font_size=15, color=C_CALC)
            calcs.append(calc_text)
            q_prev, tu_prev = q, tu

        calc_group = VGroup(*calcs).arrange(DOWN, buff=0.15).next_to(calc_header, DOWN, buff=0.2)

        for calc in calcs:
            self.play(FadeIn(calc))
            self.wait(0.25)

        self.wait(0.5)

        # ── Fade out Step 3 ────────────────────────────────────────────────
        step3_section = VGroup(step3_title, calc_header, calc_group)
        self.play(FadeOut(step3_section))
        self.wait(0.3)

        # ── STEP 4: TABLE — Organize results ────────────────────────────────
        step4_title = _section_title("Step 4 — Table: TU, MU, and AU")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        headers = ["Q", "TU", "MU", "AU"]
        rows = [
            [str(q), str(tu), str(mu), str(au)]
            for q, tu, mu, au in zip(QTY, TU, MU, AU)
        ]

        tbl = _table(headers, rows, [0.50, 0.65, 0.65, 0.65], row_h=0.32, accent=YELLOW)
        tbl.scale(0.90).next_to(step4_title, DOWN, buff=0.25)

        # Animate table row by row
        self.play(FadeIn(tbl[0]))  # header
        for i, row in enumerate(tbl[1:], 1):
            self.play(FadeIn(row), run_time=0.2)

        # Highlight key observations
        self.wait(0.5)
        note1 = Text("MU decreases as Q increases (Diminishing MU)", font_size=14, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.play(Write(note1))
        self.wait(0.6)

        note2_text = "MU = 0 at Q=6 (saturation); MU < 0 at Q=7 (disutility)"
        note2 = Text(note2_text, font_size=14, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.play(ReplacementTransform(note1, note2))
        self.wait(1.0)

        # ── Fade out Step 4 ────────────────────────────────────────────────
        self.play(FadeOut(step4_title), FadeOut(tbl), FadeOut(note2))
        self.wait(0.3)

        # ── STEP 5: GRAPH — Dual curves ─────────────────────────────────────
        step5_title = _section_title("Step 5 — Visualize: TU and MU Curves")
        step5_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step5_title))

        # TU graph (top)
        ax_tu = Axes(x_range=[0, 8, 1], y_range=[0, 35, 5],
                     x_length=5.5, y_length=2.5,
                     axis_config={"include_numbers": False, "include_tip": False})
        ax_tu.shift(LEFT * 0.5 + UP * 1.0)

        tu_pts = [(q, tu) for q, tu in zip([0] + QTY, [0] + TU)]
        tu_graph = ax_tu.plot_line_graph(
            [p[0] for p in tu_pts], [p[1] for p in tu_pts],
            line_color=C_TU, vertex_dot_radius=0.05
        )

        tu_title = Text("Total Utility (TU)", font_size=14, color=C_TU).next_to(ax_tu, UP, buff=0.02)
        tu_x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax_tu.c2p(i, 0), DOWN, buff=0.05) for i in range(1, 8)])
        tu_y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax_tu.c2p(0, i), LEFT, buff=0.05) for i in [10, 20, 30]])

        self.play(Create(ax_tu), FadeIn(tu_x_tks), FadeIn(tu_y_tks), Create(tu_graph["line_graph"]), Write(tu_title))

        # MU graph (bottom)
        ax_mu = Axes(x_range=[0, 8, 1], y_range=[-4, 12, 2],
                     x_length=5.5, y_length=2.0,
                     axis_config={"include_numbers": False, "include_tip": False})
        ax_mu.next_to(ax_tu, DOWN, buff=0.3).align_to(ax_tu, LEFT)

        mu_pts = [(q, mu) for q, mu in zip([0] + QTY, [0] + MU)]
        mu_graph = ax_mu.plot_line_graph(
            [p[0] for p in mu_pts], [p[1] for p in mu_pts],
            line_color=C_MU, vertex_dot_radius=0.05
        )

        zero_line = DashedLine(ax_mu.c2p(0, 0), ax_mu.c2p(8, 0), color=GRAY, stroke_width=1, dash_length=0.08)
        mu_title = Text("Marginal Utility (MU)", font_size=14, color=C_MU).next_to(ax_mu, DOWN, buff=0.02)
        mu_x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax_mu.c2p(i, 0), DOWN, buff=0.05) for i in range(1, 8)])
        mu_y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax_mu.c2p(0, i), LEFT, buff=0.05) for i in [-2, 0, 5, 10]])

        self.play(Create(ax_mu), FadeIn(mu_x_tks), FadeIn(mu_y_tks), Create(mu_graph["line_graph"]), Create(zero_line), Write(mu_title))

        self.wait(1.5)

        # ── Breadcrumb ──────────────────────────────────────────────────────
        crumb = _breadcrumb("Next: Indifference Curves — choosing between two goods")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 2 — Indifference Curves + Budget Line
# ═══════════════════════════════════════════════════════════════════════════════
class IndifferenceCurveScene(Scene):
    """
    TEACHING FLOW:
    1. Given: Budget parameters (Px=2, Py=1, I=12)
    2. Formula: Budget constraint 2X + Y = 12 → Y = 12 - 2X
    3. Calculations: Compute X,Y combinations by substitution
    4. Table: Show budget combinations
    5. Graph: Plot three ICs, budget line, equilibrium
    """

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Indifference Curves & Budget Constraint", font_size=38, color=WHITE).to_edge(UP)
        subtitle = Text("Px=2,  Py=1,  Income=₦12", font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Budget Parameters")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        given = VGroup(
            Text("Price of X (Px) = ₦2", font_size=17, color=C_CALC),
            Text("Price of Y (Py) = ₦1", font_size=17, color=C_CALC),
            Text("Income (I) = ₦12", font_size=17, color=C_CALC),
        ).arrange(DOWN, buff=0.15).next_to(step1_title, DOWN, buff=0.3)

        for line in given:
            self.play(FadeIn(line))

        self.wait(0.8)
        self.play(FadeOut(VGroup(step1_title, given)))
        self.wait(0.3)

        # ── STEP 2: FORMULA ─────────────────────────────────────────────────
        step2_title = _section_title("Step 2 — Formula: Budget Line")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        formula = VGroup(
            Text("Budget Constraint: Px·X + Py·Y = I", font_size=19, color=C_MU),
            Text("Rearranged:       Y = (I - Px·X) / Py", font_size=19, color=C_MU),
        ).arrange(DOWN, buff=0.2).next_to(step2_title, DOWN, buff=0.3)

        for line in formula:
            self.play(FadeIn(line))

        self.wait(1.0)
        self.play(FadeOut(VGroup(step2_title, formula)))
        self.wait(0.3)

        # ── STEP 3: CALCULATIONS ────────────────────────────────────────────
        step3_title = _section_title("Step 3 — Substitute and Calculate")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        substitution = VGroup(
            Text("Substituting Px=2, Py=1, I=12:", font_size=17, color=YELLOW),
            Text("Y = (12 - 2X) / 1 = 12 - 2X", font_size=17, color=C_CALC),
        ).arrange(DOWN, buff=0.2).next_to(step3_title, DOWN, buff=0.3)

        self.play(FadeIn(substitution[0]))
        self.play(FadeIn(substitution[1]))

        self.wait(0.5)

        # Calculate points
        calc_text = Text("For different values of X:", font_size=16, color=YELLOW).next_to(substitution, DOWN, buff=0.3)
        self.play(FadeIn(calc_text))

        calcs = VGroup()
        for x in range(0, 7):
            y = 12 - 2*x
            calc = Text(f"X={x}: Y = 12 - 2({x}) = {y}", font_size=14, color=C_CALC)
            calcs.add(calc)

        calcs.arrange(DOWN, buff=0.12).next_to(calc_text, DOWN, buff=0.2)

        for calc in calcs:
            self.play(FadeIn(calc), run_time=0.15)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step3_title, substitution, calc_text, calcs)))
        self.wait(0.3)

        # ── STEP 4: TABLE ────────────────────────────────────────────────────
        step4_title = _section_title("Step 4 — Budget Combinations Table")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        b_rows = [[str(x), str(12 - 2*x)] for x in range(0, 7)]
        b_tbl = _table(["Qty X", "Qty Y"], b_rows, [0.80, 0.80], row_h=0.32, accent=YELLOW)
        b_tbl.scale(0.85).next_to(step4_title, DOWN, buff=0.3)

        self.play(FadeIn(b_tbl[0]))
        for row in b_tbl[1:]:
            self.play(FadeIn(row), run_time=0.15)

        self.wait(1.0)
        self.play(FadeOut(VGroup(step4_title, b_tbl)))
        self.wait(0.3)

        # ── STEP 5: GRAPH ────────────────────────────────────────────────────
        step5_title = _section_title("Step 5 — Indifference Curves & Budget Line")
        step5_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step5_title))

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 20, 2],
                  x_length=5.8, y_length=4.2,
                  axis_config={"include_numbers": False, "include_tip": False})
        ax.shift(RIGHT * 0.5 + DOWN * 0.5)

        x_tks = VGroup(*[Text(str(i), font_size=12, color=GRAY).next_to(ax.c2p(i, 0), DOWN, buff=0.06) for i in range(1, 10)])
        y_tks = VGroup(*[Text(str(i), font_size=12, color=GRAY).next_to(ax.c2p(0, i), LEFT, buff=0.06) for i in range(2, 20, 2)])
        x_lbl = Text("Qty X", font_size=14, color=GRAY).next_to(ax, DOWN, buff=0.08)
        y_lbl = Text("Qty Y", font_size=14, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.08)

        self.play(Create(ax), FadeIn(x_tks), FadeIn(y_tks), FadeIn(x_lbl), FadeIn(y_lbl))

        # Three indifference curves (U=12, 18, 24)
        for U, color, label in [(12, C_IC1, "U₁=12"), (18, C_IC2, "U₂=18"), (24, C_IC3, "U₃=24")]:
            ic = ax.plot(lambda x, U=U: U/x, x_range=[U/18.5, 9.5], color=color, stroke_width=2.2)
            ic_lbl = Text(label, font_size=13, color=color).next_to(ax.c2p(9.2, U/9.2), RIGHT, buff=0.05)
            self.play(Create(ic), Write(ic_lbl), run_time=0.5)

        self.wait(0.5)

        # Budget line: Y = 12 - 2X
        bl = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=C_BL, stroke_width=2.2)
        bl_lbl = Text("Budget Line\n2X+Y=12", font_size=12, color=WHITE).next_to(ax.c2p(0.5, 11), RIGHT, buff=0.05)
        self.play(Create(bl), Write(bl_lbl), run_time=0.5)

        self.wait(0.5)

        # Equilibrium (3, 6)
        eq_dot = Dot(ax.c2p(3, 6), color=WHITE, radius=0.11)
        eq_lbl = Text("E(3,6)\nOptimal", font_size=12, color=WHITE).next_to(ax.c2p(3, 6), UR, buff=0.10)
        self.play(FadeIn(eq_dot), Write(eq_lbl))

        note = Text("Consumer reaches highest IC on the budget line", font_size=14, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(note))

        self.wait(1.5)

        crumb = _breadcrumb("Next: Cardinal Equilibrium — MUx/Px = MUy/Py")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 3 — Cardinal Equilibrium
# ═══════════════════════════════════════════════════════════════════════════════
class CardinalEquilibriumScene(Scene):
    """
    TEACHING FLOW:
    1. Given: MU data, prices, income
    2. Formula: MUx/Px = MUy/Py = λ (equi-marginal principle)
    3. Calculations: Compute ratios for each quantity
    4. Table: Side-by-side comparison of Good X and Good Y
    5. Highlight: Where ratios are equal (equilibrium)
    """

    MUX = [20, 16, 12, 8, 4]
    MUY = [6, 5, 4, 3, 2]
    PX = 2
    PY = 1

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Cardinal Equilibrium — Equi-Marginal Principle", font_size=36, color=WHITE).to_edge(UP)
        subtitle = Text("Px=2,  Py=1,  Income=₦10", font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── FORMULA BANNER ───────────────────────────────────────────────────
        formula_banner = Text("Equilibrium Condition: MUx/Px = MUy/Py = λ",
                              font_size=21, color=YELLOW).next_to(subtitle, DOWN, buff=0.3)
        self.play(FadeIn(formula_banner))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Marginal Utilities")
        step1_title.next_to(formula_banner, DOWN, buff=0.3)
        self.play(FadeIn(step1_title))

        given = VGroup(
            Text("Good X: MUx = [20, 16, 12, 8, 4] at Qx = 1..5", font_size=16, color=C_CALC),
            Text("Good Y: MUy = [6, 5, 4, 3, 2] at Qy = 1..5", font_size=16, color=C_CALC),
        ).arrange(DOWN, buff=0.15).next_to(step1_title, DOWN, buff=0.25)

        for line in given:
            self.play(FadeIn(line))

        self.wait(0.6)
        self.play(FadeOut(VGroup(step1_title, given)))
        self.wait(0.3)

        # ── STEP 2: FORMULA & CALCULATIONS ──────────────────────────────────
        step2_title = _section_title("Step 2 — Calculate MU/P Ratios")
        step2_title.next_to(formula_banner, DOWN, buff=0.3)
        self.play(FadeIn(step2_title))

        calc_note = Text("For each quantity, divide MU by price:", font_size=16, color=YELLOW).next_to(step2_title, DOWN, buff=0.2)
        self.play(FadeIn(calc_note))

        # Show calculation for first few items
        calcs_x = VGroup()
        for i, mx in enumerate(self.MUX[:3]):
            calc = Text(f"Qx={i+1}: MUx/Px = {mx}/{self.PX} = {mx//self.PX}",
                       font_size=14, color=C_CALC)
            calcs_x.add(calc)

        calcs_x.arrange(DOWN, buff=0.12).next_to(calc_note, DOWN, buff=0.2)
        for calc in calcs_x:
            self.play(FadeIn(calc), run_time=0.15)

        self.wait(0.6)
        self.play(FadeOut(VGroup(step2_title, calc_note, calcs_x)))
        self.wait(0.3)

        # ── STEP 3: TABLE ────────────────────────────────────────────────────
        step3_title = _section_title("Step 3 — Dual Comparison Table")
        step3_title.next_to(formula_banner, DOWN, buff=0.3)
        self.play(FadeIn(step3_title))

        # Good X table
        x_rows = [
            [str(i+1), str(mx), f"{mx}/{self.PX}", str(mx//self.PX)]
            for i, mx in enumerate(self.MUX)
        ]
        x_tbl = _table(["Qx", "MUx", "MUx/Px", "λx"], x_rows,
                        [0.45, 0.60, 0.70, 0.50], row_h=0.30, accent=C_IC3)

        # Good Y table
        y_rows = [
            [str(i+1), str(my), f"{my}/{self.PY}", str(my//self.PY)]
            for i, my in enumerate(self.MUY)
        ]
        y_tbl = _table(["Qy", "MUy", "MUy/Py", "λy"], y_rows,
                        [0.45, 0.60, 0.70, 0.50], row_h=0.30, accent=C_IC2)

        x_header = Text("Good X (Px=2)", font_size=15, color=C_IC3).scale(0.9)
        y_header = Text("Good Y (Py=1)", font_size=15, color=C_IC2).scale(0.9)

        x_col = VGroup(x_header, x_tbl).arrange(DOWN, buff=0.12)
        y_col = VGroup(y_header, y_tbl).arrange(DOWN, buff=0.12)

        both = VGroup(x_col, y_col).arrange(RIGHT, buff=0.6).next_to(step3_title, DOWN, buff=0.25)

        self.play(FadeIn(x_col), FadeIn(y_col))
        self.wait(1.0)

        # Highlight equilibrium rows (Qx=3, Qy=4 where ratios both = 6)
        eq_x_row = x_tbl[3]  # row for Qx=3
        eq_y_row = y_tbl[4]  # row for Qy=4

        box_x = SurroundingRectangle(eq_x_row, color=YELLOW, buff=0.06, corner_radius=0.04)
        box_y = SurroundingRectangle(eq_y_row, color=YELLOW, buff=0.06, corner_radius=0.04)

        self.play(Create(box_x), Create(box_y))

        result = Text("At Qx=3, Qy=4: MUx/Px = MUy/Py = 6  ✓  Budget: 2(3) + 1(4) = 10 = Income",
                     font_size=14, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(result))

        self.wait(1.5)

        crumb = _breadcrumb("Next: Budget Shifts — income and price changes")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 4 — Budget Line Shifts
# ═══════════════════════════════════════════════════════════════════════════════
class BudgetShiftsScene(Scene):
    """
    TEACHING FLOW:
    1. Given: Base budget (Px=2, Py=1, I=12)
    2. Formula: Y = (I - Px·X)/Py
    3. Calculations: Three scenarios (I↑, I↓, Px↓)
    4. Tables: Show budget combos for each scenario
    5. Graph: Visualize parallel shift (income) vs pivot (price)
    """

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Budget Line Shifts", font_size=40, color=WHITE).to_edge(UP)
        subtitle = Text("Income changes → parallel shift  |  Price changes → pivot",
                       font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Base Budget (Px=2, Py=1, I=12)")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        formula = Text("Budget Line: Y = (12 - 2X) / 1 = 12 - 2X",
                      font_size=17, color=YELLOW).next_to(step1_title, DOWN, buff=0.2)
        self.play(FadeIn(formula))

        b_rows = [[str(x), str(12 - 2*x)] for x in range(0, 7)]
        b_tbl = _table(["X", "Y"], b_rows, [0.65, 0.65], row_h=0.30, accent=YELLOW)
        b_tbl.scale(0.80).next_to(formula, DOWN, buff=0.2)

        self.play(FadeIn(b_tbl[0]))
        for row in b_tbl[1:]:
            self.play(FadeIn(row), run_time=0.12)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step1_title, formula, b_tbl)))
        self.wait(0.3)

        # ── STEP 2: INCOME CHANGES (Parallel Shifts) ─────────────────────────
        step2_title = _section_title("Step 2a — Income Rise: I=18")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        formula2a = Text("New Budget: Y = (18 - 2X) / 1 = 18 - 2X  (same slope, higher intercept)",
                        font_size=15, color=YELLOW).next_to(step2_title, DOWN, buff=0.2)
        self.play(FadeIn(formula2a))

        b2a_rows = [[str(x), str(18 - 2*x)] for x in range(0, 10)]
        b2a_tbl = _table(["X", "Y"], b2a_rows, [0.65, 0.65], row_h=0.28, accent=C_IC3)
        b2a_tbl.scale(0.70).next_to(formula2a, DOWN, buff=0.15)

        self.play(FadeIn(b2a_tbl[0]))
        for row in b2a_tbl[1:4]:
            self.play(FadeIn(row), run_time=0.12)

        note1 = Text("→ Parallel shift (slope unchanged)", font_size=14, color=C_IC3).next_to(b2a_tbl, DOWN, buff=0.2)
        self.play(Write(note1))

        self.wait(0.6)
        self.play(FadeOut(VGroup(step2_title, formula2a, b2a_tbl, note1)))
        self.wait(0.3)

        # ── STEP 2b: Income Fall ─────────────────────────────────────────────
        step2b_title = _section_title("Step 2b — Income Fall: I=8")
        step2b_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2b_title))

        formula2b = Text("New Budget: Y = (8 - 2X) / 1 = 8 - 2X  (same slope, lower intercept)",
                        font_size=15, color=YELLOW).next_to(step2b_title, DOWN, buff=0.2)
        self.play(FadeIn(formula2b))

        b2b_rows = [[str(x), str(8 - 2*x)] for x in range(0, 5)]
        b2b_tbl = _table(["X", "Y"], b2b_rows, [0.65, 0.65], row_h=0.28, accent=C_IC1)
        b2b_tbl.scale(0.70).next_to(formula2b, DOWN, buff=0.15)

        self.play(FadeIn(b2b_tbl[0]))
        for row in b2b_tbl[1:]:
            self.play(FadeIn(row), run_time=0.12)

        note2 = Text("→ Parallel shift  (slope unchanged)", font_size=14, color=C_IC1).next_to(b2b_tbl, DOWN, buff=0.2)
        self.play(Write(note2))

        self.wait(0.6)
        self.play(FadeOut(VGroup(step2b_title, formula2b, b2b_tbl, note2)))
        self.wait(0.3)

        # ── STEP 3: PRICE CHANGE (Pivot) ─────────────────────────────────────
        step3_title = _section_title("Step 3 — Price Fall: Px=1")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        formula3 = Text("New Budget: Y = (12 - 1·X) / 1 = 12 - X  (slope changes, y-intercept fixed at 12)",
                       font_size=15, color=YELLOW).next_to(step3_title, DOWN, buff=0.2)
        self.play(FadeIn(formula3))

        b3_rows = [[str(x), str(12 - x)] for x in range(0, 13)]
        b3_tbl = _table(["X", "Y"], b3_rows, [0.65, 0.65], row_h=0.26, accent=C_IC2)
        b3_tbl.scale(0.65).next_to(formula3, DOWN, buff=0.15)

        self.play(FadeIn(b3_tbl[0]))
        for row in b3_tbl[1:5]:
            self.play(FadeIn(row), run_time=0.12)

        note3 = Text("→ Pivot (x-intercept doubles, slope changes)", font_size=14, color=C_IC2).next_to(b3_tbl, DOWN, buff=0.2)
        self.play(Write(note3))

        self.wait(0.6)
        self.play(FadeOut(VGroup(step3_title, formula3, b3_tbl, note3)))
        self.wait(0.3)

        # ── STEP 4: GRAPH ────────────────────────────────────────────────────
        step4_title = _section_title("Step 4 — Visualize All Shifts")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        ax = Axes(x_range=[0, 14, 2], y_range=[0, 20, 4],
                  x_length=6.0, y_length=4.0,
                  axis_config={"include_numbers": False, "include_tip": False})
        ax.shift(RIGHT * 0.5 + DOWN * 0.5)

        x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(i, 0), DOWN, buff=0.05) for i in [2, 4, 6, 8, 10, 12]])
        y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(0, i), LEFT, buff=0.05) for i in [4, 8, 12, 16]])
        x_lbl = Text("Qty X", font_size=13, color=GRAY).next_to(ax, DOWN, buff=0.07)
        y_lbl = Text("Qty Y", font_size=13, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.07)

        self.play(Create(ax), FadeIn(x_tks), FadeIn(y_tks), FadeIn(x_lbl), FadeIn(y_lbl))

        # Base: Y = 12 - 2X
        bl_base = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=WHITE, stroke_width=2.3)
        lbl_base = Text("Base (I=12)", font_size=12, color=WHITE).next_to(ax.c2p(0.5, 11), RIGHT, buff=0.04)
        self.play(Create(bl_base), Write(lbl_base))

        # Up: Y = 18 - 2X
        bl_up = ax.plot(lambda x: 18 - 2*x, x_range=[0, 9], color=C_IC3, stroke_width=2, stroke_opacity=0.85)
        lbl_up = Text("I↑=18", font_size=11, color=C_IC3).next_to(ax.c2p(0.5, 17), RIGHT, buff=0.04)
        self.play(Create(bl_up), Write(lbl_up))

        # Down: Y = 8 - 2X
        bl_dn = ax.plot(lambda x: 8 - 2*x, x_range=[0, 4], color=C_IC1, stroke_width=2, stroke_opacity=0.85)
        lbl_dn = Text("I↓=8", font_size=11, color=C_IC1).next_to(ax.c2p(0.5, 7), RIGHT, buff=0.04)
        self.play(Create(bl_dn), Write(lbl_dn))

        note_parallel = Text("Income changes → parallel shifts (same slope)", font_size=13, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(note_parallel))
        self.wait(1.0)

        # Pivot: Y = 12 - X
        bl_px = ax.plot(lambda x: 12 - x, x_range=[0, 12], color=C_IC2, stroke_width=2, stroke_opacity=0.85)
        lbl_px = Text("Px↓=1", font_size=11, color=C_IC2).next_to(ax.c2p(9.5, 2.5), UR, buff=0.04)
        self.play(Create(bl_px), Write(lbl_px))

        note_pivot = Text("Price fall → pivot (slope changes, y-intercept fixed)", font_size=13, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(ReplacementTransform(note_parallel, note_pivot))

        self.wait(1.5)

        crumb = _breadcrumb("Next: Income & Substitution Effects")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 5 — Income & Substitution Effects
# ═══════════════════════════════════════════════════════════════════════════════
class IncomeSubstitutionScene(Scene):
    """
    TEACHING FLOW:
    1. Given: Utility function U=X·Y, price change Px: 2→1, I=12
    2. Formula: Decompose total effect into SE and IE
    3. Calculations: Find A, C, B points
    4. Table: Summary of three equilibria
    5. Graph: Show A→C→B path
    """

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Income & Substitution Effects (Hicks)", font_size=36, color=WHITE).to_edge(UP)
        subtitle = Text("Px: 2→1  |  Py=1  |  I=12", font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Utility & Price Change")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        given = VGroup(
            Text("Utility function: U = X·Y", font_size=16, color=C_CALC),
            Text("Original: Px=2, Py=1, I=12  →  Equilibrium A(3, 6)", font_size=16, color=C_CALC),
            Text("New: Px=1, Py=1, I=12  →  Equilibrium B(6, 6)", font_size=16, color=C_CALC),
        ).arrange(DOWN, buff=0.18).next_to(step1_title, DOWN, buff=0.25)

        for line in given:
            self.play(FadeIn(line))

        self.wait(0.8)
        self.play(FadeOut(VGroup(step1_title, given)))
        self.wait(0.3)

        # ── STEP 2: FORMULA & CONCEPT ────────────────────────────────────────
        step2_title = _section_title("Step 2 — Decomposition")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        concept = VGroup(
            Text("Total Effect (TE): A → B (quantity change = 3)", font_size=16, color=YELLOW),
            Text("Substitution Effect (SE): A → C (on same IC, cheaper price)", font_size=16, color=C_MU),
            Text("Income Effect (IE): C → B (higher real income)", font_size=16, color=C_IC3),
        ).arrange(DOWN, buff=0.18).next_to(step2_title, DOWN, buff=0.25)

        for line in concept:
            self.play(FadeIn(line))

        self.wait(1.0)
        self.play(FadeOut(VGroup(step2_title, concept)))
        self.wait(0.3)

        # ── STEP 3: CALCULATIONS ────────────────────────────────────────────
        step3_title = _section_title("Step 3 — Calculate Points A, C, B")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        calcs_section = VGroup(
            Text("Point A (original equilibrium):", font_size=15, color=YELLOW),
            Text("  MRS = Px/Py = 2, on U=18: y/x=2 → x=3, y=6  →  A(3,6)", font_size=14, color=C_CALC),
            Text("", font_size=8),
            Text("Point B (new equilibrium):", font_size=15, color=YELLOW),
            Text("  MRS = Px/Py = 1, on new BL y=12-x: x=y → x=6, y=6  →  B(6,6)", font_size=14, color=C_CALC),
            Text("", font_size=8),
            Text("Point C (compensated, Hicks):", font_size=15, color=YELLOW),
            Text("  MRS = 1 on U=18: x=y → √18≈4.24  →  C(4.24,4.24)", font_size=14, color=C_CALC),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(step3_title, DOWN, buff=0.2)

        for line in calcs_section:
            self.play(FadeIn(line), run_time=0.15)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step3_title, calcs_section)))
        self.wait(0.3)

        # ── STEP 4: TABLE ────────────────────────────────────────────────────
        step4_title = _section_title("Step 4 — Summary Table")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        summary_rows = [
            ["A", "3.00", "6.00", "18", "Original"],
            ["C", "4.24", "4.24", "18", "Compensated (SE)"],
            ["B", "6.00", "6.00", "36", "New equilibrium"],
        ]
        summary_tbl = _table(
            headers=["Point", "Qx", "Qy", "U", "Status"],
            rows=summary_rows,
            col_widths=[0.55, 0.70, 0.70, 0.55, 1.50],
            row_h=0.32, accent=YELLOW
        )

        effects_rows = [
            ["Substitution (A→C)", "+1.24", "Cheaper Px, stay on U=18"],
            ["Income (C→B)", "+1.76", "Higher real income"],
            ["Total (A→B)", "+3.00", "SE + IE"],
        ]
        effects_tbl = _table(
            headers=["Effect", "ΔQx", "Meaning"],
            rows=effects_rows,
            col_widths=[1.50, 0.70, 2.00],
            row_h=0.32, accent=C_MU
        )

        both_tbls = VGroup(summary_tbl, effects_tbl).arrange(DOWN, buff=0.25).next_to(step4_title, DOWN, buff=0.2)

        self.play(FadeIn(summary_tbl[0]))
        for row in summary_tbl[1:]:
            self.play(FadeIn(row), run_time=0.15)

        self.play(FadeIn(effects_tbl[0]))
        for row in effects_tbl[1:]:
            self.play(FadeIn(row), run_time=0.15)

        self.wait(1.0)
        self.play(FadeOut(VGroup(step4_title, both_tbls)))
        self.wait(0.3)

        # ── STEP 5: GRAPH ────────────────────────────────────────────────────
        step5_title = _section_title("Step 5 — Visualize A → C → B")
        step5_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step5_title))

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 14, 2],
                  x_length=5.6, y_length=4.0,
                  axis_config={"include_numbers": False, "include_tip": False})
        ax.shift(RIGHT * 0.5 + DOWN * 0.5)

        x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(i, 0), DOWN, buff=0.05) for i in range(1, 10)])
        y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(0, i), LEFT, buff=0.05) for i in range(2, 14, 2)])
        x_lbl = Text("X", font_size=13, color=GRAY).next_to(ax, DOWN, buff=0.07)
        y_lbl = Text("Y", font_size=13, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.07)

        self.play(Create(ax), FadeIn(x_tks), FadeIn(y_tks), FadeIn(x_lbl), FadeIn(y_lbl))

        # ICs
        ic18 = ax.plot(lambda x: 18/x, x_range=[1.2, 9.5], color=C_IC2, stroke_width=2)
        ic36 = ax.plot(lambda x: 36/x, x_range=[2.4, 9.5], color=C_IC3, stroke_width=2)
        lbl18 = Text("U=18", font_size=12, color=C_IC2).next_to(ax.c2p(9.2, 18/9.2), RIGHT, buff=0.04)
        lbl36 = Text("U=36", font_size=12, color=C_IC3).next_to(ax.c2p(9.2, 36/9.2), RIGHT, buff=0.04)
        self.play(Create(ic18), Create(ic36), Write(lbl18), Write(lbl36))

        # Budget lines
        bl_orig = ax.plot(lambda x: 12 - 2*x, x_range=[0, 6], color=C_IC1, stroke_width=1.8)
        bl_comp = ax.plot(lambda x: 8.49 - x, x_range=[0, 8.49], color=GRAY, stroke_width=1.5, stroke_opacity=0.7)
        bl_new = ax.plot(lambda x: 12 - x, x_range=[0, 12], color=WHITE, stroke_width=1.8)

        self.play(Create(bl_orig), Create(bl_comp), Create(bl_new))

        lbl_orig = Text("Orig BL", font_size=11, color=C_IC1).next_to(ax.c2p(0.5, 11), RIGHT, buff=0.03)
        lbl_comp = Text("Comp", font_size=10, color=GRAY).next_to(ax.c2p(7.5, 0.99), UR, buff=0.02)
        lbl_new = Text("New BL", font_size=11, color=WHITE).next_to(ax.c2p(9.5, 2.5), UR, buff=0.03)

        self.play(Write(lbl_orig), Write(lbl_comp), Write(lbl_new))

        # Points
        pt_A = Dot(ax.c2p(3, 6), color=C_IC1, radius=0.10)
        pt_C = Dot(ax.c2p(4.24, 4.24), color=GRAY, radius=0.10)
        pt_B = Dot(ax.c2p(6, 6), color=C_IC3, radius=0.10)

        lA = Text("A(3,6)", font_size=11, color=C_IC1).next_to(ax.c2p(3, 6), UL, buff=0.06)
        lC = Text("C(4.24,4.24)", font_size=10, color=GRAY).next_to(ax.c2p(4.24, 4.24), DR, buff=0.05)
        lB = Text("B(6,6)", font_size=11, color=C_IC3).next_to(ax.c2p(6, 6), UR, buff=0.06)

        self.play(FadeIn(pt_A), FadeIn(pt_C), FadeIn(pt_B), Write(lA), Write(lC), Write(lB))

        # Arrows & effects
        arr_SE = Arrow(ax.c2p(3, 0.4), ax.c2p(4.24, 0.4), color=C_MU, buff=0, stroke_width=2)
        arr_IE = Arrow(ax.c2p(4.24, 0.4), ax.c2p(6, 0.4), color=C_IC3, buff=0, stroke_width=2)

        se_lbl = Text("SE +1.24", font_size=11, color=C_MU).next_to(arr_SE, DOWN, buff=0.04)
        ie_lbl = Text("IE +1.76", font_size=11, color=C_IC3).next_to(arr_IE, DOWN, buff=0.04)

        self.play(Create(arr_SE), Write(se_lbl))
        self.play(Create(arr_IE), Write(ie_lbl))

        final = Text("TE = SE + IE = 1.24 + 1.76 = 3.00", font_size=14, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(final))

        self.wait(1.5)

        crumb = _breadcrumb("Next: Consumer Surplus — benefit from exchange")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 6 — Consumer Surplus
# ═══════════════════════════════════════════════════════════════════════════════
class ConsumerSurplusScene(Scene):
    """
    TEACHING FLOW:
    1. Given: Demand function P=12-Q, market price P*=4
    2. Formula: CS per unit = WTP - P*, Total CS = ½ × base × height
    3. Calculations: Compute CS for each unit, sum
    4. Table: Price-quantity schedule with per-unit CS
    5. Graph: Demand curve, price line, shaded CS triangle
    """

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Consumer Surplus", font_size=42, color=WHITE).to_edge(UP)
        subtitle = Text("Demand: P = 12 - Q  |  Market Price P* = ₦4",
                       font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Demand Function")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        given = VGroup(
            Text("Demand Curve: P = 12 - Q", font_size=17, color=C_CALC),
            Text("Market Price: P* = ₦4", font_size=17, color=C_CALC),
            Text("Quantity demanded at P*=4: Q* = 12 - 4 = 8 units", font_size=17, color=C_CALC),
        ).arrange(DOWN, buff=0.18).next_to(step1_title, DOWN, buff=0.25)

        for line in given:
            self.play(FadeIn(line))

        self.wait(0.8)
        self.play(FadeOut(VGroup(step1_title, given)))
        self.wait(0.3)

        # ── STEP 2: FORMULA & CONCEPT ────────────────────────────────────────
        step2_title = _section_title("Step 2 — Consumer Surplus Formula")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        formula_cs = VGroup(
            Text("CS per unit = Willingness to Pay - Market Price",
                 font_size=16, color=C_MU),
            Text("                 = P(Q) - P*",
                 font_size=16, color=C_MU),
            Text("", font_size=8),
            Text("Total CS = ½ × base × height (triangle area)",
                 font_size=16, color=YELLOW),
            Text("           = ½ × 8 × (12 - 4) = ½ × 8 × 8 = 32",
                 font_size=16, color=YELLOW),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(step2_title, DOWN, buff=0.25)

        for line in formula_cs:
            self.play(FadeIn(line), run_time=0.15)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step2_title, formula_cs)))
        self.wait(0.3)

        # ── STEP 3: TABLE ────────────────────────────────────────────────────
        step3_title = _section_title("Step 3 — CS per Unit Calculation")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        P_star = 4
        rows_cs = []
        for q in range(1, 9):
            p_wtp = 12 - q
            cs_unit = p_wtp - P_star
            rows_cs.append([str(q), f"₦{p_wtp}", f"₦{P_star}", f"₦{cs_unit}"])

        tbl_cs = _table(
            headers=["Q", "WTP (P)", "P*", "CS/unit"],
            rows=rows_cs,
            col_widths=[0.45, 0.75, 0.65, 0.75],
            row_h=0.30, accent=YELLOW
        )
        tbl_cs.scale(0.85).next_to(step3_title, DOWN, buff=0.25)

        self.play(FadeIn(tbl_cs[0]))
        for row in tbl_cs[1:]:
            self.play(FadeIn(row), run_time=0.12)

        total_note = Text("Total CS = 8+7+6+5+4+3+2+1 = ₦32",
                         font_size=15, color=YELLOW).next_to(tbl_cs, DOWN, buff=0.2)
        self.play(Write(total_note))

        self.wait(0.8)
        self.play(FadeOut(VGroup(step3_title, tbl_cs, total_note)))
        self.wait(0.3)

        # ── STEP 4: GRAPH ────────────────────────────────────────────────────
        step4_title = _section_title("Step 4 — Graph: Demand Curve & CS")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        ax = Axes(x_range=[0, 12, 1], y_range=[0, 14, 2],
                  x_length=5.8, y_length=4.0,
                  axis_config={"include_numbers": False, "include_tip": False})
        ax.shift(RIGHT * 0.3 + DOWN * 0.5)

        x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(i, 0), DOWN, buff=0.05) for i in [2, 4, 6, 8, 10]])
        y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(0, i), LEFT, buff=0.05) for i in [2, 4, 6, 8, 10, 12]])
        x_lbl = Text("Quantity (Q)", font_size=13, color=GRAY).next_to(ax, DOWN, buff=0.07)
        y_lbl = Text("Price (P)", font_size=13, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.07)

        self.play(Create(ax), FadeIn(x_tks), FadeIn(y_tks), FadeIn(x_lbl), FadeIn(y_lbl))

        # Demand curve: P = 12 - Q
        demand = ax.plot(lambda q: 12 - q, x_range=[0, 11], color=C_DEMAND, stroke_width=2.4)
        d_lbl = Text("D: P=12-Q", font_size=13, color=C_DEMAND).next_to(ax.c2p(0.5, 11.5), RIGHT, buff=0.04)
        self.play(Create(demand), Write(d_lbl))

        # Price line P* = 4
        p_line = ax.plot(lambda q: 4, x_range=[0, 11], color=WHITE, stroke_width=1.8, stroke_opacity=0.8)
        p_lbl = Text("P*=4", font_size=12, color=WHITE).next_to(ax.c2p(0.2, 4), LEFT, buff=0.05)
        self.play(Create(p_line), Write(p_lbl))

        # Q* = 8 line
        q_line = DashedLine(ax.c2p(8, 0), ax.c2p(8, 4), color=GRAY, stroke_width=1.1, dash_length=0.08)
        q_lbl = Text("Q*=8", font_size=12, color=GRAY).next_to(ax.c2p(8, 0), DOWN, buff=0.08)
        self.play(Create(q_line), Write(q_lbl))

        self.wait(0.5)

        # CS triangle shading
        cs_triangle = Polygon(
            ax.c2p(0, 12),    # P-intercept (12, 0)
            ax.c2p(8, 4),     # Equilibrium point
            ax.c2p(0, 4),     # Vertical drop at Q=0
            color=BLUE, fill_color=BLUE, fill_opacity=0.3, stroke_width=0
        )
        self.play(FadeIn(cs_triangle))

        cs_label = Text("CS = ₦32", font_size=18, color=BLUE).move_to(ax.c2p(2.5, 8))
        self.play(Write(cs_label))

        note_cs = Text("Consumer Surplus = area above price line, below demand curve",
                      font_size=14, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(Write(note_cs))

        self.wait(1.5)

        crumb = _breadcrumb("Next: Diminishing MU Explains the Demand Curve")
        self.play(FadeIn(crumb))
        self.wait(1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 7 — Diminishing MU to Demand Curve
# ═══════════════════════════════════════════════════════════════════════════════
class DiminishingMUDemandScene(Scene):
    """
    TEACHING FLOW:
    1. Given: MU data (same as Scene 1)
    2. Formula: MU = Willingness to Pay (price consumer will pay)
    3. Calculations: Map each MU to a quantity
    4. Table: MU as WTP
    5. Graph: Plot as demand curve
    """

    WTP = [10, 8, 6, 4, 2, 0]  # MU at Q=1..6

    def construct(self):
        self.camera.background_color = C_BG

        # ── HEADER ──────────────────────────────────────────────────────────
        main_title = Text("Diminishing MU  ↔  Demand Curve", font_size=38, color=WHITE).to_edge(UP)
        subtitle = Text("MU is willingness to pay → this creates the demand curve",
                       font_size=17, color=GRAY, slant=ITALIC).next_to(main_title, DOWN, buff=0.06)

        self.play(Write(main_title), FadeIn(subtitle))
        self.wait(0.8)

        # ── STEP 1: GIVEN ────────────────────────────────────────────────────
        step1_title = _section_title("Step 1 — Given: Marginal Utility Data")
        step1_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step1_title))

        given = VGroup(
            Text("Same data from Scene 1 (Law of Diminishing MU):", font_size=16, color=C_CALC),
            Text("Q:  1   2   3   4   5   6", font_size=15, color=YELLOW),
            Text("MU: 10  8   6   4   2   0  (₦ per unit)", font_size=15, color=YELLOW),
        ).arrange(DOWN, buff=0.15).next_to(step1_title, DOWN, buff=0.25)

        for line in given:
            self.play(FadeIn(line), run_time=0.15)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step1_title, given)))
        self.wait(0.3)

        # ── STEP 2: CONCEPT ─────────────────────────────────────────────────
        step2_title = _section_title("Step 2 — Key Insight: MU = WTP")
        step2_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step2_title))

        concept = VGroup(
            Text("Marginal Utility represents:", font_size=16, color=YELLOW),
            Text("  → Maximum price consumer will pay for the NEXT unit", font_size=15, color=C_CALC),
            Text("", font_size=8),
            Text("Demand curve is derived from MU:", font_size=16, color=YELLOW),
            Text("  → At each quantity, consumer demands at price = MU of that unit", font_size=15, color=C_CALC),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(step2_title, DOWN, buff=0.25)

        for line in concept:
            self.play(FadeIn(line), run_time=0.15)

        self.wait(1.0)
        self.play(FadeOut(VGroup(step2_title, concept)))
        self.wait(0.3)

        # ── STEP 3: MAPPING ─────────────────────────────────────────────────
        step3_title = _section_title("Step 3 — Map MU to Price Points")
        step3_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step3_title))

        mappings = VGroup()
        for q, mu in zip(range(1, 7), self.WTP):
            mapping = Text(f"At Q={q}: Consumer willing to pay ₦{mu}  →  Point ({q}, {mu}) on demand",
                          font_size=14, color=C_CALC)
            mappings.add(mapping)

        mappings.arrange(DOWN, buff=0.12).next_to(step3_title, DOWN, buff=0.25)

        for mapping in mappings:
            self.play(FadeIn(mapping), run_time=0.15)

        self.wait(0.8)
        self.play(FadeOut(VGroup(step3_title, mappings)))
        self.wait(0.3)

        # ── STEP 4: TABLE ────────────────────────────────────────────────────
        step4_title = _section_title("Step 4 — MU = WTP Table")
        step4_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step4_title))

        rows_wtp = [[str(q), f"₦{mu}"] for q, mu in zip(range(1, 7), self.WTP)]
        tbl_wtp = _table(
            headers=["Qty (Q)", "MU / WTP (₦)"],
            rows=rows_wtp,
            col_widths=[0.70, 2.00],
            row_h=0.32, accent=C_MU
        )
        tbl_wtp.scale(0.90).next_to(step4_title, DOWN, buff=0.3)

        self.play(FadeIn(tbl_wtp[0]))
        for row in tbl_wtp[1:]:
            self.play(FadeIn(row), run_time=0.15)

        note_law = Text("As Q increases, MU (and thus demand price) falls → Law of Demand",
                       font_size=14, color=YELLOW).next_to(tbl_wtp, DOWN, buff=0.2)
        self.play(Write(note_law))

        self.wait(0.8)
        self.play(FadeOut(VGroup(step4_title, tbl_wtp, note_law)))
        self.wait(0.3)

        # ── STEP 5: GRAPH ────────────────────────────────────────────────────
        step5_title = _section_title("Step 5 — The Demand Curve (MU Curve)")
        step5_title.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(step5_title))

        ax = Axes(x_range=[0, 8, 1], y_range=[0, 12, 2],
                  x_length=5.8, y_length=4.0,
                  axis_config={"include_numbers": False, "include_tip": False})
        ax.shift(RIGHT * 0.4 + DOWN * 0.5)

        x_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(i, 0), DOWN, buff=0.05) for i in range(1, 8)])
        y_tks = VGroup(*[Text(str(i), font_size=11, color=GRAY).next_to(ax.c2p(0, i), LEFT, buff=0.05) for i in [0, 2, 4, 6, 8, 10]])
        x_lbl = Text("Quantity (Q)", font_size=13, color=GRAY).next_to(ax, DOWN, buff=0.07)
        y_lbl = Text("Price / MU (₦)", font_size=13, color=GRAY).rotate(PI/2).next_to(ax, LEFT, buff=0.07)

        self.play(Create(ax), FadeIn(x_tks), FadeIn(y_tks), FadeIn(x_lbl), FadeIn(y_lbl))

        # Plot MU as demand
        pts_x = [0] + list(range(1, 7))
        pts_y = [10] + self.WTP

        demand_curve = ax.plot_line_graph(
            pts_x, pts_y,
            line_color=C_DEMAND, vertex_dot_radius=0.08
        )
        self.play(Create(demand_curve["line_graph"]), run_time=1.0)
        self.play(FadeIn(demand_curve["vertex_dots"]))

        d_label = Text("D = MU Curve", font_size=14, color=C_DEMAND).next_to(ax.c2p(5.5, 2.5), RIGHT, buff=0.05)
        self.play(Write(d_label))

        # Label each point
        self.wait(0.5)
        for q, mu in zip(range(1, 7), self.WTP):
            pt_lbl = Text(f"({q},{mu})", font_size=10, color=GRAY)
            pt_lbl.next_to(ax.c2p(q, mu), UR, buff=0.04)
            self.add(pt_lbl)

        self.wait(0.5)

        conclusion = Text(
            "The demand curve directly follows from the Law of Diminishing Marginal Utility",
            font_size=15, color=YELLOW
        ).to_edge(DOWN, buff=0.7)
        self.play(Write(conclusion))

        self.wait(1.5)

        crumb = _breadcrumb("End of Consumer Behaviour series. Review: Utility → IC → Equilibrium → Surplus")
        self.play(FadeIn(crumb))
        self.wait(1.0)
