#!/usr/bin/env python3
"""
teach_queue.py — Lesson Queue & Script Stack for the std-dev video series
==========================================================================
A structured lesson runner built around a proper queue/stack model:

  Queue  → scenes not yet reached (upcoming)
  Stack  → scenes already presented (history)
  Current → the scene being delivered right now

Each scene carries a three-part teacher script:
  [1] PRE-VIDEO   — what to say and ask BEFORE pressing play
  [2] CUES        — timed moment-by-moment prompts DURING the video
  [3] POST-VIDEO  — discussion questions and bridge AFTER the video

Usage:
  python3 teach_queue.py              # start from scene 1
  python3 teach_queue.py --from 3    # jump straight to scene 3
  python3 teach_queue.py --export    # save full script to lesson_script.txt
  python3 teach_queue.py --play      # auto-open video when entering each scene

Controls (inside the runner):
  n / Enter  next scene
  p          previous scene
  1          show Pre-video script panel
  2          show During-video cues panel
  3          show Post-video discussion panel
  v          play the current video
  r          restart queue from scene 1
  q          quit
"""

import argparse
import os
import subprocess
import textwrap
from collections import deque
from pathlib import Path

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

CONSOLE      = Console()
ROOT         = Path(__file__).parent
VIDEO_DIR    = ROOT / "media" / "videos" / "std_dev_viz" / "480p15"
CB_VIDEO_DIR = ROOT / "media" / "videos" / "consumer_behaviour" / "480p15"

# ── colour map (up to 7 scenes) ───────────────────────────────────────────────
SCENE_COLOURS = ["green", "yellow", "cyan", "magenta", "red", "blue", "white"]

# ─────────────────────────────────────────────────────────────────────────────
# Teaching scripts
# ─────────────────────────────────────────────────────────────────────────────
SCENES = [
    # ── 1 ────────────────────────────────────────────────────────────────────
    {
        "number":   1,
        "title":    "Dataset Spread",
        "file":     "DatasetIntroScene.mp4",
        "duration": "~18 s",
        "concept":  "Same mean — completely different spread",
        "pre": [
            "HOOK  Ask the class before touching anything:",
            "  'Two factories both report an average output of 10 units per hour.",
            "   Are they equally reliable?  Why or why not?'",
            "",
            "Allow 30–60 seconds of open debate — do not correct anyone yet.",
            "",
            "Then say:",
            "  'Let me show you three real datasets that share exactly the same",
            "   average.  Watch the tables carefully — especially the bottom row.'",
            "",
            "FOCUS POINT  Tell students to watch for the x̄ row at the bottom of",
            "each table and note that all three read 10.0.",
        ],
        "cues": [
            ("0:04", "Tables appear — ask: 'What does the xᵢ column represent?'"),
            ("0:10", "Mean row (x̄ = 10.0) is highlighted across all three — PAUSE here.",
                     "Say: 'Three completely different datasets. Identical averages.",
                     "      The mean alone is hiding something important.'"),
            ("0:15", "Bar charts appear — ask: 'Which dataset looks most reliable to",
                     "      you?  Could you predict the next value in each one?'"),
            ("0:18", "Breadcrumb text — read it aloud as a preview sentence."),
        ],
        "post": [
            "KEY TAKEAWAY  The mean is not enough on its own.",
            "",
            "Discussion:",
            "  Ask: 'What single number could tell us how spread out a dataset is?'",
            "  Accept any intuitive answer — range, gap, average distance, etc.",
            "  Write their suggestions on the board.",
            "",
            "Bridge to Scene 2:",
            "  'One of those suggestions is exactly right — average distance from the mean.",
            "   But we will see a problem with that idea in a moment.  Watch Scene 2.'",
        ],
        "key_q": "If two datasets share the same mean, what else must we compare?",
    },

    # ── 2 ────────────────────────────────────────────────────────────────────
    {
        "number":   2,
        "title":    "Dispersion from the Mean",
        "file":     "DispersionScene.mp4",
        "duration": "~22 s",
        "concept":  "Deviation = signed distance from x̄",
        "pre": [
            "RECAP  Say:",
            "  'In Scene 1 we saw three datasets with identical means — x̄ = 10.",
            "   Scene 2 will show you what we mean by each value being close to",
            "   or far from that mean.'",
            "",
            "VOCABULARY  Introduce these terms before playing:",
            "  • deviation  =  xᵢ − x̄   (positive if above mean, negative if below)",
            "  • The table at the start will PROVE both datasets have x̄ = 10.",
            "",
            "WATCH FOR  Tell students:",
            "  'Every dot starts on the mean marker (x̄ = 10) and flies to its",
            "   actual value.  The arrow label shows the signed distance: + or −.'",
        ],
        "cues": [
            ("0:05", "Comparison table — confirm Σ=100, n=10, x̄=10.0 for BOTH rows.",
                     "      Say: 'Proof on screen.  Same mean.  Different story.'"),
            ("0:10", "Dots animated outward — say: 'Each dot travels exactly (xᵢ − 10) units.'"),
            ("0:17", "Arrow labels (±N) appear — ask:",
                     "      'Which row has bigger arrows?  What does that tell us about σ?'"),
            ("0:21", "'Wider spread → Higher σ' footer — students copy this phrase."),
        ],
        "post": [
            "CRITICAL QUESTION  Ask the class:",
            "  'If I calculate the average of ALL the deviations (+1, −1, +2, −2 …),",
            "   what do I get?'",
            "",
            "Let them work it out (answer: always 0 — they cancel).",
            "",
            "Then ask:",
            "  'So how do we stop them cancelling?  How do we keep the distances positive?'",
            "  Expected answers: absolute value, squaring.",
            "",
            "Bridge to Scene 3:",
            "  'Scene 3 uses squaring.  We will see exactly why that choice leads us to σ.'",
        ],
        "key_q": "Why does averaging raw deviations always return zero?",
    },

    # ── 3 ────────────────────────────────────────────────────────────────────
    {
        "number":   3,
        "title":    "Building the Formula",
        "file":     "StdDevFormulaScene.mp4",
        "duration": "~16 s",
        "concept":  "σ = √( Σ(xᵢ − x̄)² / n )",
        "pre": [
            "RECAP  Say:",
            "  'Raw deviations always sum to zero.  Squaring every deviation fixes that",
            "   and also magnifies large outliers — making σ sensitive to extremes.'",
            "",
            "LAYOUT  Describe what students will see:",
            "  LEFT  — a computation table built row by row:",
            "          xᵢ  |  xᵢ − x̄  |  (xᵢ − x̄)²",
            "  RIGHT — the running derivation:",
            "          Σ → Variance → Formula → σ result",
            "",
            "DATASET  [2, 4, 4, 4, 5, 5, 7, 9]   x̄ = 5",
            "",
            "Tell students: keep a pencil ready — copy the formula when it appears.",
        ],
        "cues": [
            ("0:04", "Column headers appear — read them aloud: xᵢ, xᵢ−x̄, (xᵢ−x̄)²."),
            ("0:05", "Rows fill in one by one — students can verify each square mentally.",
                     "      E.g. row 1: xᵢ=2, deviation=2−5=−3, square=(−3)²=9."),
            ("0:13", "Σ row = 32 appears — ask: 'What do we do with this sum next?'"),
            ("0:14", "Variance = 32/8 = 4.00 — say: 'Dividing by n gives the AVERAGE squared deviation.'"),
            ("0:15", "σ = √4.00 ≈ 2.00 boxed in red — ask: 'Why take the square root at the end?'",
                     "      Answer: to return to the original unit (kg, °C, €, etc.)"),
            ("0:16", "Bottom note: 'every value is ~2.0 units from the mean on average'",
                     "      This is the plain-English meaning of σ.  Students copy it."),
        ],
        "post": [
            "FORMULA RECALL  Students write from memory:",
            "  σ = √( Σ(xᵢ − x̄)² / n )",
            "",
            "WORKED CHECK  Apply it together to the STABLE dataset from Scene 1:",
            "  Data: [9,10,10,11,10,9,10,11,10,10]   x̄ = 10",
            "  Σ(xᵢ−10)² = 1+0+0+1+0+1+0+1+0+0 = 4",
            "  Variance  = 4/10 = 0.40",
            "  σ         = √0.40 ≈ 0.63  ← matches Scene 1 label",
            "",
            "EXTENSION  Discuss population σ vs sample s (÷n vs ÷(n−1)).",
            "",
            "Bridge to Scene 4:",
            "  'Now we can compute σ.  But what does it LOOK like on a graph?",
            "   Scene 4 puts σ = 0.6 next to σ = 5.7 side by side.'",
        ],
        "key_q": "Why square the deviations instead of taking absolute values?",
    },

    # ── 4 ────────────────────────────────────────────────────────────────────
    {
        "number":   4,
        "title":    "σ and Data Instability",
        "file":     "StabilityCompareScene.mp4",
        "duration": "~16 s",
        "concept":  "Higher σ = wider swings = less predictable",
        "pre": [
            "PREDICTION  Write on the board before playing:",
            "  Low σ ≈ 0.6   →  graph looks like  ___",
            "  High σ ≈ 5.7  →  graph looks like  ___",
            "",
            "Ask students to predict the shape and take a show-of-hands vote.",
            "",
            "Say:",
            "  'Scene 4 will show a stats table first — confirm the means are equal.",
            "   Then the graphs appear with a numbered y-axis so you can read actual values.",
            "   The dashed line marks x̄ on each graph.'",
        ],
        "cues": [
            ("0:03", "Stats table — read σ values aloud.  Confirm x̄ ≈ 10 for both.",
                     "      Ask: 'Which dataset would you feel comfortable making decisions from?'"),
            ("0:08", "Both axes appear with y-ticks 0,5,10,15,20 — note the scale is identical."),
            ("0:09", "Dashed mean lines at y=10 — say: 'Same mean.  Watch what happens next.'"),
            ("0:12", "Lines drawn simultaneously — give students 3 seconds of silent observation."),
            ("0:15", "Dots appear, then 'Higher σ → Wider swings' message — students add to notes."),
        ],
        "post": [
            "ANALOGY SORT  Read each scenario; students call out 'low σ' or 'high σ':",
            "  • A rod-cutting machine produces 10 cm rods ± 0.05 mm    → low σ",
            "  • A student's test scores: 30, 95, 42, 88, 61            → high σ",
            "  • A river's flow rate during calm summer days             → low σ",
            "  • Daily number of emergency calls at a hospital           → high σ",
            "",
            "KEY INSIGHT  'A high mean with high σ can be more dangerous than a low mean with low σ.'",
            "  Example: average drug dose is correct but varies wildly → some patients underdose,",
            "           others overdose.",
            "",
            "Bridge to Scene 5:",
            "  'Scene 5 puts this in a financial context where σ has an official name: volatility.'",
        ],
        "key_q": "Can you name a real-world situation where high σ would be catastrophic?",
    },

    # ── 5 ────────────────────────────────────────────────────────────────────
    {
        "number":   5,
        "title":    "Real-World Impact",
        "file":     "RealWorldScene.mp4",
        "duration": "~17 s",
        "concept":  "σ = the mathematical definition of risk",
        "pre": [
            "CONTEXT  Set the scene:",
            "  'Imagine you have $1,000 to invest for one year.",
            "   You find two assets.  Both have the same average daily gain: +0.3.',",
            "  'Which do you choose?'",
            "",
            "Let students argue briefly — most will say 'they're the same'.",
            "",
            "Say:",
            "  'The stats table will appear first — look at the Daily σ column.",
            "   Then the 30-day price chart will draw itself, with a numbered y-axis",
            "   so you can read exact prices.'",
        ],
        "cues": [
            ("0:04", "Stats table — read Daily σ aloud.  Ask: 'Which is riskier before you see the graph?'"),
            ("0:09", "Chart axes appear — note y-axis range 80–120 and x-axis day 0–29."),
            ("0:12", "Both lines draw — green (A) climbs steadily, red (B) swings wildly.",
                     "      Give students 3 seconds of silent comparison."),
            ("0:15", "'Low σ → lower risk' callout box — students copy as the lesson summary statement."),
        ],
        "post": [
            "CLASS DISCUSSION  (choose 1–2 depending on time):",
            "",
            "  1. MEDICINE",
            "     'A drug must deliver 50 mg.  Batch A: σ = 0.2 mg.  Batch B: σ = 8 mg.",
            "      Which batch is safe to administer?  Why?'",
            "",
            "  2. AVIATION",
            "     'Engine thrust has σ = 1%.  Cabin temperature has σ = 5°C.",
            "      Which tolerance is acceptable?  Would you swap them?'",
            "",
            "  3. CLIMATE",
            "     'Two cities both average 20°C.  City A: σ = 2°C.  City B: σ = 10°C.",
            "      Where would you rather live?'",
            "",
            "WRAP-UP STATEMENT  Students write this in their own words:",
            "  'Standard deviation σ measures how much data deviates from its mean.",
            "   The higher σ is, the more unstable and unpredictable the data becomes.",
            "   In finance σ is called volatility; in engineering it is called tolerance.",
            "   Wherever decisions depend on data, σ measures how much you can trust",
            "   the mean as a representative value.'",
            "",
            "ASSESSMENT IDEA  Give two datasets with the same mean.",
            "  Ask students to compute σ for each and write one paragraph explaining",
            "  which dataset is more reliable and why.",
        ],
        "key_q": "Name three domains outside finance where high σ would be dangerous.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Consumer Behaviour teaching scripts  (7 scenes)
# ─────────────────────────────────────────────────────────────────────────────
CB_SCENES = [
    # ── 1 ─────────────────────────────────────────────────────────────────────
    {
        "number":   1,
        "title":    "Utility: TU, MU & AU",
        "file":     "UtilityScene.mp4",
        "duration": "~22 s",
        "concept":  "Law of Diminishing Marginal Utility",
        "pre": [
            "HOOK  Ask before pressing play:",
            "  'If you eat one slice of pizza you are very happy.",
            "   After six slices, are you still equally happy with each one?'",
            "",
            "Allow 30 seconds of discussion.",
            "",
            "Then say:",
            "  'We are going to measure that falling satisfaction using numbers.",
            "   Watch the table — pay close attention to the MU column.'",
            "",
            "FOCUS POINT  MU column colour: yellow = positive, red = negative.",
        ],
        "cues": [
            ("0:04", "Table builds row by row — call out MU values as they appear."),
            ("0:12", "MU = 0 row highlighted at Q=6.",
                     "Say: 'This is the saturation point — no extra satisfaction.'"),
            ("0:16", "Negative MU at Q=7 flagged.",
                     "Say: 'Beyond saturation, more becomes a burden — disutility.'"),
            ("0:20", "Dual-curve chart — TU and MU plotted together.",
                     "Point out: TU is maximum exactly where MU crosses zero."),
            ("0:22", "Breadcrumb appears — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Each additional unit gives less extra satisfaction.",
            "",
            "Discussion:",
            "  'Can you give a real-life example of diminishing MU?'",
            "  'At what point did your MU become zero or negative?'",
            "",
            "Assessment:",
            "  Give Q: 'If TU at Q=5 is 30 and TU at Q=6 is 30, what is MU₆?'",
            "  (Answer: 0 — confirm with the graph.)",
            "",
            "Bridge:",
            "  'We measured utility for one good. What if you must choose",
            "   between two goods with a limited budget?'",
        ],
        "key_q": "At what quantity does Total Utility reach its maximum, and why does MU = 0 at that point?",
    },
    # ── 2 ─────────────────────────────────────────────────────────────────────
    {
        "number":   2,
        "title":    "Indifference Curves & Equilibrium",
        "file":     "IndifferenceCurveScene.mp4",
        "duration": "~20 s",
        "concept":  "Highest reachable indifference curve = consumer equilibrium",
        "pre": [
            "SETUP  Write on the board: Px=₦2, Py=₦1, Income=₦12",
            "",
            "Ask:",
            "  'If you have ₦12 and Good X costs ₦2 while Good Y costs ₦1,",
            "   how many different combinations of X and Y could you buy?'",
            "",
            "Let two students suggest combinations — verify on budget equation.",
            "",
            "Then say:",
            "  'The curve that connects all combinations giving the SAME satisfaction",
            "   is called an indifference curve. Watch how the budget line touches one.'",
        ],
        "cues": [
            ("0:03", "Budget combination table — count the rows with students."),
            ("0:10", "Three IC curves drawn — note they never cross each other."),
            ("0:14", "Budget line appears — ask: 'Which IC does it touch?'"),
            ("0:17", "Equilibrium point E(3,6) highlighted.",
                     "Say: 'At this point MRS = Px/Py = 2 — the consumer is in balance.'"),
            ("0:20", "Breadcrumb — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Consumer equilibrium: tangency of budget line and IC.",
            "",
            "Discussion:",
            "  'Why can the consumer NOT reach U₃?' (Answer: budget constraint.)",
            "  'What happens to the equilibrium if income doubles?'",
            "",
            "Quick test:",
            "  'If the consumer is at U₁, are they maximising utility? Why not?'",
            "",
            "Bridge:",
            "  'We used ordinal utility (rankings). Now let us use cardinal utility",
            "   (actual MU numbers) to find the same equilibrium differently.'",
        ],
        "key_q": "Why must the slope of the budget line equal MRS at consumer equilibrium?",
    },
    # ── 3 ─────────────────────────────────────────────────────────────────────
    {
        "number":   3,
        "title":    "Cardinal Equilibrium (MU/P)",
        "file":     "CardinalEquilibriumScene.mp4",
        "duration": "~18 s",
        "concept":  "Equi-marginal principle: MUx/Px = MUy/Py = λ",
        "pre": [
            "RECAP  Ask: 'What did the indifference curve tell us about equilibrium?'",
            "",
            "Then say:",
            "  'Cardinal utility uses actual numbers — we can compute the exact",
            "   quantity of each good that maximises utility. Watch the λ column.'",
            "",
            "Write the formula on the board:",
            "  MUx / Px = MUy / Py = λ  (lambda = marginal utility of income)",
            "",
            "FOCUS POINT  Students should track when the λ values match across",
            "both goods — that is the equilibrium combination.",
        ],
        "cues": [
            ("0:04", "Formula banner displayed — read it with the class."),
            ("0:08", "Dual tables build: Good X (left) and Good Y (right)."),
            ("0:13", "Boxes highlight Qx=3 and Qy=4 simultaneously.",
                     "Say: 'MUx/Px = MUy/Py = 6 here — the ratios are equal.'"),
            ("0:16", "Budget check shown: 2×3 + 1×4 = 10 = income.  Say: 'Confirmed!'"),
            ("0:18", "Breadcrumb — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Spend income so the last ₦ spent on each good gives equal MU.",
            "",
            "Discussion:",
            "  'What does λ represent?' (MU from spending one more naira.)",
            "  'If MUx/Px > MUy/Py, what should the consumer do?'",
            "  (Answer: buy more X, less Y, until equality is restored.)",
            "",
            "Worked example:",
            "  'If MUx=20, Px=4, MUy=15, Py=3, is the consumer in equilibrium?'",
            "  (MUx/Px=5, MUy/Py=5 — Yes!)",
            "",
            "Bridge:",
            "  'What if the price of X changed? How would the budget line shift?'",
        ],
        "key_q": "If MUx/Px > MUy/Py, what adjustment must the consumer make to reach equilibrium?",
    },
    # ── 4 ─────────────────────────────────────────────────────────────────────
    {
        "number":   4,
        "title":    "Budget Line Shifts",
        "file":     "BudgetShiftsScene.mp4",
        "duration": "~20 s",
        "concept":  "Income → parallel shift; Price → pivot",
        "pre": [
            "HOOK  Ask: 'If your income doubles, can you buy twice as much of everything?'",
            "",
            "Discuss briefly, then add:",
            "  'What if the price of just one good falls — does the whole budget change?'",
            "",
            "Remind students of the budget equation: Px·x + Py·y = I",
            "  Intercepts: x-axis = I/Px,  y-axis = I/Py",
            "",
            "FOCUS POINT  Watch the x-intercept and y-intercept of each line.",
            "  — Income shift: BOTH intercepts change proportionally.",
            "  — Price pivot:  only the x-intercept moves.",
        ],
        "cues": [
            ("0:04", "Base budget table (I=12) shown — count intercept values."),
            ("0:09", "Base budget line drawn (white)."),
            ("0:12", "I=18 line (green) — parallel above.  Ask: 'Which intercept changed?'"),
            ("0:15", "I=8 line (red) — parallel below.  'And this one?'"),
            ("0:17", "Px=1 pivot line (yellow) — x-intercept doubles to 12.",
                     "Say: 'Y-intercept stays at 12 — Py and I are unchanged.'"),
            ("0:20", "Breadcrumb — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Two causes of budget change, two different geometric effects.",
            "",
            "Quick quiz (ask orally):",
            "  'If Px rises, which way does the budget line pivot?'",
            "  'If income falls by 20%, what happens to both intercepts?'",
            "",
            "Concept check:",
            "  'A tax on Good X is equivalent to a rise in Px — show on the diagram.'",
            "",
            "Bridge:",
            "  'When Px falls, the consumer buys more X for two different reasons.",
            "   Let us separate those two effects.'",
        ],
        "key_q": "A rise in income and a fall in Px both move the budget line — how do they differ geometrically?",
    },
    # ── 5 ─────────────────────────────────────────────────────────────────────
    {
        "number":   5,
        "title":    "Income & Substitution Effects",
        "file":     "IncomeSubstitutionScene.mp4",
        "duration": "~25 s",
        "concept":  "Hicks decomposition: TE = SE + IE",
        "pre": [
            "SETUP  Write on board: Px falls from ₦2 to ₦1  (Py=₦1, I=₦12)",
            "",
            "Ask: 'When petrol becomes cheaper, why do you buy more?'",
            "  Guide students to two reasons:",
            "  1. It is now cheaper relative to other things (substitution).",
            "  2. Your real purchasing power has effectively risen (income).",
            "",
            "Introduce Hicks method:",
            "  'We remove the income effect by imagining the government takes back",
            "   just enough income to keep you on the ORIGINAL satisfaction level.'",
            "",
            "FOCUS POINT  Watch points A, C and B.",
        ],
        "cues": [
            ("0:04", "Summary table: A(3,6), C(4.24,4.24), B(6,6) — read the columns."),
            ("0:10", "Effects table: SE=+1.24, IE=+1.76, TE=+3.00."),
            ("0:15", "Graph: two ICs drawn — U=18 and U=36."),
            ("0:18", "Three budget lines: original (red), compensated (grey), new (white)."),
            ("0:21", "Points A, C, B plotted.  Arrows show SE then IE along x-axis.",
                     "Say: 'Both effects point in the same direction — normal good.'"),
            ("0:25", "Breadcrumb — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Total Effect = Substitution Effect + Income Effect.",
            "",
            "Discussion:",
            "  'For an inferior good, IE is negative. What does that do to TE?'",
            "  'For a Giffen good, |IE| > |SE|, so TE is negative — demand curve slopes UP.'",
            "",
            "Diagram exercise:",
            "  'Sketch the Hicks decomposition for a price RISE.'",
            "",
            "Bridge:",
            "  'We know consumers gain when prices fall. But by how much?",
            "   That gain is called Consumer Surplus.'",
        ],
        "key_q": "A good has SE=+2 and IE=−3 when its price falls. Is it normal, inferior, or Giffen?",
    },
    # ── 6 ─────────────────────────────────────────────────────────────────────
    {
        "number":   6,
        "title":    "Consumer Surplus",
        "file":     "ConsumerSurplusScene.mp4",
        "duration": "~22 s",
        "concept":  "CS = area between demand curve and price line",
        "pre": [
            "HOOK  Ask: 'Have you ever paid ₦500 for something you would have",
            "  happily paid ₦800 for?  That ₦300 difference is your consumer surplus.'",
            "",
            "Write on board:  Demand → P = 12 − Q,  Market Price P* = ₦4",
            "",
            "Ask: 'How much would someone pay for the 1st unit?  The 2nd?  The 8th?'",
            "  (Answers: ₦11, ₦10, … ₦4 — from the demand equation.)",
            "",
            "FOCUS POINT  Watch the blue shaded triangle — that is the total CS.",
        ],
        "cues": [
            ("0:04", "Data table builds: willingness-to-pay vs market price per unit."),
            ("0:10", "Total CS = ½ × 8 × 8 = ₦32 announced."),
            ("0:13", "Axes and demand curve D: P=12−Q drawn."),
            ("0:16", "Horizontal price line P*=4 and vertical Q*=8 added."),
            ("0:18", "Blue CS triangle shaded.",
                     "Say: 'Every unit from Q=1 to Q=8 earns surplus. The triangle captures it all.'"),
            ("0:21", "Breadcrumb — read aloud."),
        ],
        "post": [
            "KEY TAKEAWAY  Consumer Surplus = what you would have paid minus what you actually paid.",
            "",
            "Calculation exercise:",
            "  'If P* rises to ₦8, recalculate CS.'",
            "  (New Q* = 4, CS = ½ × 4 × 4 = ₦8 — CS fell sharply.)",
            "",
            "Discussion:",
            "  'Why does a price ceiling (P < P*) increase CS for buyers who can get the good?'",
            "  'What is the connection between CS and the demand curve?'",
            "",
            "Bridge:",
            "  'The demand curve itself comes from the MU curve.",
            "   In our final scene, we connect these two ideas formally.'",
        ],
        "key_q": "If market price rises from ₦4 to ₦8 on demand P=12−Q, by how much does consumer surplus fall?",
    },
    # ── 7 ─────────────────────────────────────────────────────────────────────
    {
        "number":   7,
        "title":    "Diminishing MU → Demand Curve",
        "file":     "DiminishingMUDemandScene.mp4",
        "duration": "~22 s",
        "concept":  "The demand curve is the MU curve (willingness to pay)",
        "pre": [
            "RECAP HOOK  Ask: 'We said MU falls as you consume more.",
            "  If MU = the maximum price you are willing to pay, what does that imply?'",
            "",
            "Guide to: 'You pay less for extra units → buy more only at lower prices",
            "           → that is the Law of Demand!'",
            "",
            "Tell students:",
            "  'This scene is the grand finale — it ties Scenes 1 through 6 together.",
            "   Watch how the MU table becomes the demand curve point by point.'",
        ],
        "cues": [
            ("0:04", "MU-as-WTP table builds: each MU value is a willingness-to-pay price."),
            ("0:12", "Note: MU falls from ₦10 at Q=1 to ₦0 at Q=6 — downward sequence."),
            ("0:15", "Axes drawn — demand curve plotted through each (Q, MU) point.",
                     "Say: 'The demand curve IS the MU curve.'"),
            ("0:18", "Dot labels (1,10), (2,8) … (6,0) placed on each point."),
            ("0:20", "Final note: 'Law of Demand follows from Diminishing MU.'"),
            ("0:22", "End breadcrumb — recap the full journey."),
        ],
        "post": [
            "GRAND RECAP  Walk students through the full series linkage:",
            "  Scene 1: TU/MU/AU → Diminishing MU",
            "  Scene 2: IC map → consumer equilibrium (ordinal)",
            "  Scene 3: MU/P ratios → consumer equilibrium (cardinal)",
            "  Scene 4: Budget shifts → income & price effects on consumption",
            "  Scene 5: Hicks decomposition → SE + IE = TE",
            "  Scene 6: CS = area under demand above price line",
            "  Scene 7: MU curve = Demand curve — the unifying idea",
            "",
            "Final question (written assessment):",
            "  'Explain why the demand curve slopes downward using the concept",
            "   of diminishing marginal utility.'",
        ],
        "key_q": "How does the Law of Diminishing Marginal Utility directly explain the downward slope of the demand curve?",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Queue / Stack model
# ─────────────────────────────────────────────────────────────────────────────
class LessonQueue:
    """
    Manages the lesson state as a queue (upcoming) + stack (completed).

      advance()  → pop from queue front; push current to stack
      retreat()  → pop from stack top;  push current back to queue front
      restart()  → rebuild queue from scratch
    """

    def __init__(self, start_at: int = 1, scenes=None, video_dir=None):
        self._scenes  = scenes if scenes is not None else SCENES
        self.video_dir = video_dir if video_dir is not None else VIDEO_DIR
        self._all     = self._scenes
        self.done     = []                         # completed scenes (stack)
        self.queue    = deque(self._scenes)        # upcoming scenes
        self.current  = None

        # Fast-forward to the requested starting scene
        self._advance_internal()
        while self.current and self.current["number"] < start_at:
            self._advance_internal()

    def _advance_internal(self):
        if self.current:
            self.done.append(self.current)
        self.current = self.queue.popleft() if self.queue else None

    def advance(self) -> bool:
        if not self.queue:
            return False
        self._advance_internal()
        return True

    def retreat(self) -> bool:
        if not self.done:
            return False
        if self.current:
            self.queue.appendleft(self.current)
        self.current = self.done.pop()
        return True

    def restart(self):
        self.done    = []
        self.queue   = deque(self._scenes)
        self.current = None
        self._advance_internal()

    @property
    def total(self):
        return len(self._all)

    @property
    def position(self):
        return len(self.done) + (1 if self.current else 0)

    @property
    def is_last(self):
        return len(self.queue) == 0


# ─────────────────────────────────────────────────────────────────────────────
# Rendering helpers
# ─────────────────────────────────────────────────────────────────────────────

SECTION_LABELS = {
    "pre":   "[1] PRE-VIDEO  — What to say before pressing play",
    "cues":  "[2] CUES       — Moment-by-moment prompts during the video",
    "post":  "[3] POST-VIDEO — Discussion, assessment & bridge",
}

SECTION_COLOURS = {"pre": "cyan", "cues": "yellow", "post": "green"}


def _progress_bar(pos: int, total: int, width: int = 28) -> str:
    filled = round(width * pos / total)
    return "█" * filled + "░" * (width - filled)


def _queue_table(lq: LessonQueue) -> Table:
    tbl = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), expand=False)
    tbl.add_column("st",  width=2)
    tbl.add_column("num", width=2, style="dim")
    tbl.add_column("ttl", width=32)
    tbl.add_column("dur", width=7, style="dim")

    for s in lq.done:
        c = SCENE_COLOURS[s["number"] - 1]
        tbl.add_row("✓", str(s["number"]), s["title"], s["duration"], style=f"dim {c}")

    if lq.current:
        c = SCENE_COLOURS[lq.current["number"] - 1]
        tbl.add_row(
            "►", str(lq.current["number"]),
            f"[bold]{lq.current['title']}[/bold]",
            lq.current["duration"],
            style=f"bold {c}",
        )

    for s in lq.queue:
        tbl.add_row("  ", str(s["number"]), s["title"], s["duration"], style="dim")

    return tbl


def _script_panel(scene: dict, section: str) -> Panel:
    colour = SECTION_COLOURS[section]
    lines  = scene[section]   # list of strings (or tuples for cues)
    body   = Text()

    if section == "cues":
        for item in lines:
            # item is a tuple: (timestamp, line1, line2, ...)
            ts    = item[0]
            texts = item[1:]
            body.append(f"[{ts}]  ", style=f"bold {colour}")
            body.append(texts[0] + "\n", style="white")
            for extra in texts[1:]:
                body.append(f"        {extra}\n", style="dim white")
    else:
        for line in lines:
            if line.startswith("  "):
                body.append(line + "\n", style="dim white")
            elif line == "":
                body.append("\n")
            elif line.isupper() or line.endswith(":"):
                body.append(line + "\n", style=f"bold {colour}")
            else:
                body.append(line + "\n", style="white")

    return Panel(body, title=SECTION_LABELS[section], border_style=colour, padding=(0, 1))


def _key_q_panel(scene: dict) -> Panel:
    return Panel(
        Text(f"  {scene['key_q']}", style="bold yellow italic"),
        title="Key Question to pose to the class",
        border_style="yellow",
        padding=(0, 1),
    )


def _controls_text() -> str:
    return (
        "[dim]  [bold]n[/bold]/Enter  next  │  "
        "[bold]p[/bold]  prev  │  "
        "[bold]v[/bold]  play video  │  "
        "[bold]1[/bold]  pre  [bold]2[/bold]  cues  [bold]3[/bold]  post  │  "
        "[bold]r[/bold]  restart  │  "
        "[bold]q[/bold]  quit[/dim]"
    )


def render(lq: LessonQueue, section: str):
    os.system("clear")
    c = SCENE_COLOURS[(lq.current["number"] - 1)] if lq.current else "white"

    # ── header ────────────────────────────────────────────────────────────────
    CONSOLE.print(Rule(
        f"[bold {c}]Scene {lq.position} of {lq.total}  │  "
        f"{lq.current['title'] if lq.current else ''}  │  "
        f"{lq.current['concept'] if lq.current else ''}[/bold {c}]"
    ))

    # ── progress bar ──────────────────────────────────────────────────────────
    bar = _progress_bar(lq.position, lq.total)
    CONSOLE.print(f"  [{c}]{bar}[/{c}]  {lq.position}/{lq.total}", justify="left")
    CONSOLE.print()

    # ── queue list + video path ───────────────────────────────────────────────
    video_path = lq.video_dir / lq.current["file"]
    exists_txt = (
        f"[green]✓ {video_path}[/green]"
        if video_path.exists()
        else f"[red]✗ video not found: {video_path}[/red]"
    )
    CONSOLE.print(_queue_table(lq))
    CONSOLE.print(f"  {exists_txt}")
    CONSOLE.print()

    # ── script panel ──────────────────────────────────────────────────────────
    CONSOLE.print(_script_panel(lq.current, section))
    CONSOLE.print()

    # ── key question ──────────────────────────────────────────────────────────
    CONSOLE.print(_key_q_panel(lq.current))
    CONSOLE.print()

    # ── controls ──────────────────────────────────────────────────────────────
    CONSOLE.print(Rule())
    CONSOLE.print(_controls_text())


# ─────────────────────────────────────────────────────────────────────────────
# Video player
# ─────────────────────────────────────────────────────────────────────────────

def try_play(scene: dict, video_dir=None):
    path = (video_dir or VIDEO_DIR) / scene["file"]
    if not path.exists():
        CONSOLE.print(f"\n[red]Video not found:[/red] {path}")
        CONSOLE.input("[dim]Press Enter to continue…[/dim]")
        return

    players = ["mpv", "vlc", "ffplay", "xdg-open", "open"]
    for player in players:
        if subprocess.run(["which", player], capture_output=True).returncode == 0:
            CONSOLE.print(f"\n[dim]Launching {player}…[/dim]")
            subprocess.Popen([player, str(path)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return

    CONSOLE.print(Panel(
        f"[yellow]No video player found.[/yellow]\n\nOpen manually:\n[bold]{path}[/bold]",
        border_style="yellow",
    ))
    CONSOLE.input("[dim]Press Enter to continue…[/dim]")


# ─────────────────────────────────────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────────────────────────────────────

def export_script(scenes=None, video_dir=None, filename="lesson_script.txt"):
    scenes    = scenes    if scenes    is not None else SCENES
    video_dir = video_dir if video_dir is not None else VIDEO_DIR
    out = ROOT / filename
    lines = [
        "FULL TEACHING SCRIPT",
        "=" * 65,
        f"Video directory: {video_dir}",
        "",
    ]
    for s in scenes:
        sep = "=" * 65
        lines += [
            sep,
            f"SCENE {s['number']}: {s['title'].upper()}",
            f"Duration: {s['duration']}   |   Concept: {s['concept']}",
            f"Video:    {video_dir / s['file']}",
            sep,
            "",
            "── PRE-VIDEO (before pressing play) ──────────────────────",
            *s["pre"],
            "",
            "── DURING-VIDEO CUES ──────────────────────────────────────",
        ]
        for item in s["cues"]:
            ts    = item[0]
            texts = item[1:]
            lines.append(f"  [{ts}]  {texts[0]}")
            for t in texts[1:]:
                lines.append(f"          {t}")
        lines += [
            "",
            "── POST-VIDEO DISCUSSION ──────────────────────────────────",
            *s["post"],
            "",
            f"KEY QUESTION:  {s['key_q']}",
            "",
        ]

    out.write_text("\n".join(lines))
    CONSOLE.print(f"[green]Script saved to:[/green] [bold]{out}[/bold]")


# ─────────────────────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────────────────────

def run(lq: LessonQueue, auto_play: bool = False):
    section = "pre"

    if auto_play and lq.current:
        try_play(lq.current, lq.video_dir)

    while lq.current:
        render(lq, section)

        raw = Prompt.ask(
            "\n[bold cyan]>[/bold cyan]",
            choices=["n", "p", "v", "1", "2", "3", "r", "q", ""],
            default="n",
            show_choices=False,
        ).strip().lower()

        if raw in ("n", ""):
            if lq.is_last:
                # End of queue
                os.system("clear")
                CONSOLE.print(Panel(
                    "[bold green]Lesson complete![/bold green]\n\n"
                    "Run  [bold]python3 teach_queue.py --export[/bold]  "
                    "to save the full teaching script.",
                    border_style="green",
                ))
                break
            section = "pre"
            lq.advance()
            if auto_play:
                try_play(lq.current)

        elif raw == "p":
            lq.retreat()
            section = "pre"

        elif raw == "v":
            try_play(lq.current, lq.video_dir)
            CONSOLE.input("\n[dim]Press Enter to continue…[/dim]")

        elif raw == "1":
            section = "pre"

        elif raw == "2":
            section = "cues"

        elif raw == "3":
            section = "post"

        elif raw == "r":
            lq.restart()
            section = "pre"

        elif raw == "q":
            break

    CONSOLE.print()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Teaching queue & script stack for Manim lesson series.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Controls inside the runner:
              n / Enter  next scene        1  pre-video script
              p          previous scene    2  during-video cues
              v          play video        3  post-video discussion
              r          restart queue     q  quit
        """),
    )
    parser.add_argument(
        "--module", choices=["std-dev", "consumer-behaviour"],
        default="std-dev",
        help="Which lesson module to run (default: std-dev)",
    )
    parser.add_argument(
        "--from", dest="start", type=int, default=1, metavar="N",
        help="Start at scene N (default: 1)",
    )
    parser.add_argument(
        "--play", action="store_true",
        help="Auto-open the video when entering each scene",
    )
    parser.add_argument(
        "--export", action="store_true",
        help="Save full teaching script to a .txt file and exit",
    )
    args = parser.parse_args()

    if args.module == "consumer-behaviour":
        scenes    = CB_SCENES
        video_dir = CB_VIDEO_DIR
        fname     = "cb_lesson_script.txt"
    else:
        scenes    = SCENES
        video_dir = VIDEO_DIR
        fname     = "lesson_script.txt"

    if args.export:
        export_script(scenes=scenes, video_dir=video_dir, filename=fname)
        return

    lq = LessonQueue(start_at=args.start, scenes=scenes, video_dir=video_dir)
    run(lq, auto_play=args.play)


if __name__ == "__main__":
    main()
