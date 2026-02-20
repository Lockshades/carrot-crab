#!/usr/bin/env python3
"""
teach.py – Interactive teaching guide for the Standard Deviation video series.

Usage:
    python3 teach.py              # interactive walkthrough (default)
    python3 teach.py --scene 3   # jump straight to scene 3
    python3 teach.py --play      # try to open videos with system player
    python3 teach.py --list      # list all scenes and exit
    python3 teach.py --export    # save a printable PDF lesson plan (requires reportlab)
"""

import argparse
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

# ── rich is bundled with manim, use it for pretty terminal output ────────────
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
from rich.prompt import Prompt, Confirm
from rich import box

CONSOLE = Console()

# ── paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
VIDEO_DIR   = SCRIPT_DIR / "media" / "videos" / "std_dev_viz" / "480p15"
PREVIEW_DIR = SCRIPT_DIR / "media" / "previews"

# ── lesson plan data ─────────────────────────────────────────────────────────
SCENES = [
    {
        "number": 1,
        "title":  "Dataset Spread",
        "file":   "DatasetIntroScene.mp4",
        "duration": "~8 s",
        "concept": "Same mean, different spread",
        "summary": (
            "Three bar charts are shown side by side, all with the same mean "
            "but progressively wider spreads: Stable (σ≈0.5), Moderate (σ≈2.5), "
            "Chaotic (σ≈5.5). A dashed mean line runs through each."
        ),
        "talking_points": [
            "Ask students: 'Do these three datasets feel the same to you?'",
            "Point out: the mean (average) is identical in all three — yet they look completely different.",
            "Introduce vocabulary: 'spread', 'dispersion', 'variation'.",
            "Question: 'How would you measure how spread out the data is?'",
        ],
        "key_question": "If two factories report the same average output, can we trust them equally?",
        "follow_up": "Lead into Scene 2 — let's measure that spread mathematically.",
    },
    {
        "number": 2,
        "title":  "Dispersion from the Mean",
        "file":   "DispersionScene.mp4",
        "duration": "~13 s",
        "concept": "Deviation = distance from the mean",
        "summary": (
            "Dots start at the mean (x̄) then animate outward to their actual values. "
            "Arrows show the deviation of each point. Low σ dots barely move; "
            "high σ dots fly to the edges of the screen."
        ),
        "talking_points": [
            "Watch: every dot starts at the same place — the mean.",
            "Each dot travels a distance = (value − mean). That distance is the deviation.",
            "Low σ row: dots cluster tight. High σ row: dots scatter far.",
            "Key insight: we need ONE number that summarises all those distances.",
            "Why not just average the raw deviations? (They cancel out to 0!)",
        ],
        "key_question": "If deviations always sum to zero, how do we stop them cancelling?",
        "follow_up": "Answer: square them — leads directly into Scene 3.",
    },
    {
        "number": 3,
        "title":  "Building the Formula",
        "file":   "StdDevFormulaScene.mp4",
        "duration": "~15 s",
        "concept": "σ = √( Σ(xᵢ − x̄)² / n )",
        "summary": (
            "Four-step animated construction of the standard deviation formula: "
            "dataset → mean → squared deviations → final σ formula with a live "
            "numeric worked example (σ = 2.00)."
        ),
        "talking_points": [
            "Step 1: Start with raw data [2,4,4,4,5,5,7,9].",
            "Step 2: Calculate mean x̄ = 40/8 = 5.",
            "Step 3: Subtract mean from each value, then SQUARE — squaring makes all values positive and amplifies large deviations.",
            "Step 4: Average the squares → variance. Take the square root → back in original units → σ.",
            "Stress: the square root is what puts σ back in the same unit as the data (e.g. kg, €, °C).",
        ],
        "key_question": "Why do we square the deviations instead of taking absolute values?",
        "follow_up": (
            "Squaring has nice mathematical properties (differentiable everywhere) "
            "and punishes large deviations more. Now let's see what different σ values LOOK like."
        ),
    },
    {
        "number": 4,
        "title":  "σ and Data Instability",
        "file":   "StabilityCompareScene.mp4",
        "duration": "~13 s",
        "concept": "Higher σ = wider swings = less predictable",
        "summary": (
            "Side-by-side animated line graphs. Left: low σ=0.50 (flat, stable). "
            "Right: high σ=5.68 (jagged, chaotic). Both have the same mean. "
            "Curly braces mark the spread. Caption: Higher σ → Wider swings → Less predictable."
        ),
        "talking_points": [
            "This is the core visual — same mean, one line flat, one line wild.",
            "Low σ: you can predict the next value with confidence.",
            "High σ: the next value could be almost anywhere.",
            "Use analogy: a student with consistent 70% scores vs one swinging from 20% to 100%.",
            "Manufacturing: a machine with high σ produces many defective parts even if the average is 'on target'.",
        ],
        "key_question": "In which scenario would you feel more comfortable making a decision based on the data?",
        "follow_up": "Let's see a real-world domain where this matters enormously — finance.",
    },
    {
        "number": 5,
        "title":  "Real-World Impact",
        "file":   "RealWorldScene.mp4",
        "duration": "~11 s",
        "concept": "σ as a measure of risk / volatility",
        "summary": (
            "Two simulated assets tracked over 30 time steps. Asset A (green, σ≈0.9) "
            "trends steadily upward. Asset B (red, σ≈3.7) crashes and spikes wildly — "
            "same average return. A callout box: Low σ = predictable, low risk. "
            "High σ = unpredictable, high risk."
        ),
        "talking_points": [
            "Both assets have the same average return — so which would YOU invest in?",
            "Asset A: calm, predictable growth. Asset B: could double or crash to zero.",
            "In finance, σ IS the definition of volatility / risk.",
            "Other domains: weather forecasting, quality control, medical test reliability, sports performance.",
            "Summary: σ quantifies how much we can TRUST the mean as a representative value.",
        ],
        "key_question": "Name three fields outside finance where high standard deviation would be dangerous.",
        "follow_up": (
            "Discussion answers could include: medicine (drug dosage consistency), "
            "aviation (component tolerances), climate science (extreme weather events)."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name == "posix" else "cls")


def header():
    CONSOLE.print(Rule("[bold cyan]Standard Deviation — Teaching Guide[/bold cyan]"))


def scene_panel(scene: dict, show_full: bool = True) -> Panel:
    colour = ["green", "yellow", "cyan", "magenta", "red"][scene["number"] - 1]
    t = Text()
    t.append(f"  Scene {scene['number']}: {scene['title']}\n", style=f"bold {colour}")
    t.append(f"  Duration: {scene['duration']}   |   Concept: {scene['concept']}\n",
             style="dim")
    if show_full:
        t.append("\n")
        t.append("  WHAT HAPPENS\n", style="bold underline")
        for line in textwrap.wrap(scene["summary"], 72):
            t.append(f"  {line}\n", style="white")

        t.append("\n")
        t.append("  TALKING POINTS\n", style="bold underline")
        for i, pt in enumerate(scene["talking_points"], 1):
            t.append(f"  {i}. ", style=f"bold {colour}")
            for line in textwrap.wrap(pt, 68):
                t.append(f"{line}\n", style="white")
                t.append("     ")        # indent continuation lines
            # remove trailing indent for last line
            t.rstrip()
            t.append("\n")

        t.append("\n")
        t.append("  KEY QUESTION  ", style="bold yellow")
        t.append(f"{scene['key_question']}\n", style="italic yellow")

        t.append("\n")
        t.append("  BRIDGE TO NEXT  ", style="bold dim")
        t.append(f"{scene['follow_up']}\n", style="dim")

    video_path = VIDEO_DIR / scene["file"]
    exists = "✓ video found" if video_path.exists() else "✗ video missing"
    t.append(f"\n  {exists}: {video_path}\n", style="dim")

    return Panel(t, border_style=colour, padding=(0, 1))


def overview_table() -> Table:
    tbl = Table(box=box.ROUNDED, border_style="cyan", show_lines=True)
    tbl.add_column("#",       style="bold cyan",   width=3)
    tbl.add_column("Title",   style="bold white",  width=26)
    tbl.add_column("Concept", style="yellow",       width=32)
    tbl.add_column("Duration",style="dim",          width=8)
    tbl.add_column("Video",   style="dim green",    width=6)

    for s in SCENES:
        exists = "✓" if (VIDEO_DIR / s["file"]).exists() else "✗"
        tbl.add_row(
            str(s["number"]),
            s["title"],
            s["concept"],
            s["duration"],
            exists,
        )
    return tbl


def try_play(scene: dict):
    path = VIDEO_DIR / scene["file"]
    if not path.exists():
        CONSOLE.print(f"[red]Video not found: {path}[/red]")
        return

    players = ["mpv", "vlc", "ffplay", "xdg-open", "open"]
    for player in players:
        if subprocess.run(["which", player], capture_output=True).returncode == 0:
            CONSOLE.print(f"[dim]Opening with {player}…[/dim]")
            subprocess.Popen([player, str(path)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return

    # fallback: print path so the user can open manually
    CONSOLE.print(
        Panel(
            f"[yellow]No video player found.[/yellow]\n\n"
            f"Open this file manually:\n[bold]{path}[/bold]",
            title="Play video", border_style="yellow",
        )
    )


def export_lesson_plan():
    """Save a plain-text lesson plan to lesson_plan.txt."""
    out = SCRIPT_DIR / "lesson_plan.txt"
    lines = [
        "STANDARD DEVIATION — LESSON PLAN",
        "=" * 60,
        "",
        "A five-scene video study showing how higher σ means higher data instability.",
        "",
    ]
    for s in SCENES:
        lines += [
            f"SCENE {s['number']}: {s['title'].upper()}",
            "-" * 50,
            f"Duration : {s['duration']}",
            f"Concept  : {s['concept']}",
            f"Video    : {VIDEO_DIR / s['file']}",
            "",
            "SUMMARY",
            *textwrap.wrap(s["summary"], 70),
            "",
            "TALKING POINTS",
            *[f"  {i}. {pt}" for i, pt in enumerate(s["talking_points"], 1)],
            "",
            f"KEY QUESTION: {s['key_question']}",
            "",
            f"BRIDGE: {s['follow_up']}",
            "",
            "=" * 60,
            "",
        ]
    out.write_text("\n".join(lines))
    CONSOLE.print(f"[green]Lesson plan saved to:[/green] [bold]{out}[/bold]")


# ─────────────────────────────────────────────────────────────────────────────
# interactive walkthrough
# ─────────────────────────────────────────────────────────────────────────────

def run_interactive(start: int = 1, auto_play: bool = False):
    clear()
    header()
    CONSOLE.print()
    CONSOLE.print("[bold]Overview of all 5 scenes:[/bold]")
    CONSOLE.print(overview_table())
    CONSOLE.print()

    total = len(SCENES)
    idx   = start - 1          # 0-based index

    while 0 <= idx < total:
        scene = SCENES[idx]
        clear()
        header()
        CONSOLE.print(
            f"[dim]Scene {scene['number']} of {total}  "
            f"│  Press [bold]n[/bold]=next  [bold]p[/bold]=prev  "
            f"[bold]v[/bold]=play video  [bold]q[/bold]=quit[/dim]\n"
        )
        CONSOLE.print(scene_panel(scene))

        if auto_play:
            try_play(scene)

        choice = Prompt.ask(
            "\n[bold cyan]>[/bold cyan]",
            choices=["n", "p", "v", "q", ""],
            default="n",
            show_choices=False,
        ).strip().lower()

        if choice in ("n", ""):
            idx += 1
        elif choice == "p":
            idx = max(0, idx - 1)
        elif choice == "v":
            try_play(scene)
            CONSOLE.input("\n[dim]Press Enter to continue…[/dim]")
        elif choice == "q":
            break

    clear()
    header()
    if idx >= total:
        CONSOLE.print(Panel(
            "[bold green]You've reached the end of the lesson![/bold green]\n\n"
            "Run  [bold]python3 teach.py --export[/bold]  to save a printable lesson plan.",
            border_style="green",
        ))
    CONSOLE.print()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Interactive teaching guide for the std-dev Manim video series.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 teach.py                # start interactive walkthrough
              python3 teach.py --scene 3      # jump to scene 3
              python3 teach.py --play         # auto-open videos as you advance
              python3 teach.py --list         # print scene overview table
              python3 teach.py --export       # save lesson_plan.txt
        """),
    )
    parser.add_argument("--scene",  type=int, default=1, metavar="N",
                        help="Start at scene N (1-5)")
    parser.add_argument("--play",   action="store_true",
                        help="Auto-open each video as its slide appears")
    parser.add_argument("--list",   action="store_true",
                        help="Print scene overview and exit")
    parser.add_argument("--export", action="store_true",
                        help="Save lesson_plan.txt and exit")
    args = parser.parse_args()

    if args.list:
        header()
        CONSOLE.print(overview_table())
        return

    if args.export:
        export_lesson_plan()
        return

    scene_num = max(1, min(args.scene, len(SCENES)))
    run_interactive(start=scene_num, auto_play=args.play)


if __name__ == "__main__":
    main()
