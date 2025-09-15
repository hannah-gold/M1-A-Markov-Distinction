import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, RegularPolygon

class SleepCycle:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix
        self.stage = list(transition_matrix.keys())
        # map stage -> index and back (useful for plotting)
        self.stage_to_id = {s: i for i, s in enumerate(self.stage)}
        self.id_to_stage = {i: s for s, i in self.stage_to_id.items()}

    def get_next_stage(self, current_stage):
        return np.random.choice(
            self.stage,
            p = [self.transition_matrix[current_stage][next_stage] for next_stage in self.stage]
        )

    def simulate(self, epoch_minutes=5, current_stage = "Awake", sleep_duration = 8, seed=None):
        steps = int((sleep_duration * 60) / epoch_minutes)
        rng = np.random.default_rng(seed)
        sequence = [current_stage]
        current = current_stage
        for _ in range(steps - 1):
            current = self.get_next_stage(current)
            sequence.append(current)
        return sequence

    def draw_abstract_art(self, stages, cols=12, cell=1.0, pad=0.12, jitter=0.10, bg="#0f0f10", save_path="sleep_art.png",
                      title="Sleep Stages — Abstract Art"):
        """
        Render an abstract grid: one colored shape per epoch.

        stages: list of stage names per epoch (e.g., output of simulate)
        cols:   how many epochs per row (12 => one hour per row for 5-min epochs)
        cell:   size of each grid cell (arbitrary units)
        pad:    how much margin inside a cell (fraction of cell)
        jitter: random offset (fraction of cell) to make the art less rigid
        bg:     background color
        """
        # Style mapping (customize as you like)
        STYLE = {
            "Awake": {"color": "#F6C90E", "shape": "circle"},
            "Light": {"color": "#5BC0EB", "shape": "square"},
            "Deep":  {"color": "#1B263B", "shape": "diamond"},
            "REM":   {"color": "#E83F6F", "shape": "triangle"},
        }
        # Ensure all stages have styles
        for s in self.stage:
            if s not in STYLE:
                raise ValueError(f"Unknown stage '{s}'. Expected one of {list(STYLE.keys())}")

        n = len(stages)
        rows = (n + cols - 1) // cols
        width, height = cols * cell, rows * cell

        fig, ax = plt.subplots(figsize=(width * 0.55, height * 0.55), dpi=150)
        ax.set_facecolor(bg)

        r_shape = cell * (0.5 - pad)

        for i, st in enumerate(stages):
            r = i // cols
            c = i % cols
            # y from top to bottom (row 0 at top)
            y0 = (rows - 1 - r) * cell
            x0 = c * cell

            # center of the cell with slight jitter
            cx = x0 + cell/2 + np.random.uniform(-jitter, jitter) * cell
            cy = y0 + cell/2 + np.random.uniform(-jitter, jitter) * cell

            spec = STYLE[st]
            color = spec["color"]
            shape = spec["shape"]

            if shape == "circle":
                patch = Circle((cx, cy), radius=r_shape, facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.95)
            elif shape == "square":
                patch = Rectangle((cx - r_shape, cy - r_shape), 2*r_shape, 2*r_shape, facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.95)
            elif shape == "diamond":
                patch = RegularPolygon((cx, cy), numVertices=4, radius=r_shape, orientation=np.pi/4, facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.95)
            elif shape == "triangle":
                patch = RegularPolygon((cx, cy), numVertices=3, radius=r_shape, orientation=np.pi/2, facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.95)
            else:
                patch = Rectangle((cx - r_shape, cy - r_shape), 2*r_shape, 2*r_shape, facecolor=color, edgecolor="white", linewidth=0.6, alpha=0.95)

            ax.add_patch(patch)

        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        ax.set_title(title, color="white", pad=8)

        # Save to file and close the figure (no blocking GUI window)
        fig.savefig(save_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)
        print(f"Saved abstract art to: {save_path}")

    def graph_sleep(self, stage, epoch_minutes=5,):
        times = np.arange(len(stage)) * epoch_minutes
        y_vals = [self.stage_to_id[s] for s in stage]

        plt.figure(figsize=(10, 4))
        plt.step(times, y_vals, where="post")
        plt.yticks(range(len(self.stage)), self.stage)
        plt.xlabel("Time (minutes)")
        plt.ylabel("Stage")
        plt.title("Simulated Sleep Hypnogram")
        plt.tight_layout()
        plt.show()

def main():
    sleep_cycle = SleepCycle({
        "Awake": {"Awake": 0.7, "Light": 0.25, "Deep": 0.00, "REM": 0.05},
        "Light": {"Awake": 0.05, "Light": 0.70, "Deep": 0.15, "REM": 0.10},
        "Deep": {"Awake": 0.02, "Light": 0.20, "Deep": 0.70, "REM": 0.08},
        "REM": {"Awake": 0.05, "Light": 0.60, "Deep": 0.05, "REM": 0.30}
    })

    # --- Simulate 8 hours in 5-minute epochs (96 steps) ---
    stages = sleep_cycle.simulate(sleep_duration=8, epoch_minutes=5, current_stage="Awake")

    # sleep_cycle.graph_sleep(stages, epoch_minutes=5)

    sleep_cycle.draw_abstract_art(
        stages,
        cols = 12,           # 12 epochs/hour
        cell = 1.0,          # size of each cell (scales figure size)
        pad = 0.14,          # margin inside cell
        jitter = 0.10,       # slight randomness so it looks organic
        bg = "#0b0b0c",
        save_path = "sleep_art.png",
        title = "Sleep Stages — Abstract Art"
    )
if __name__ == "__main__":
    main()