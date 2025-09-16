import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, RegularPolygon

class SleepCycle:
    def __init__(self, transition_matrix):
        """
        Initialize the SleepCycle Markov model.

        Argumentss:

        - transition_matrix (dict of dicts): A dictionary of transition probabilities between stages.
        """
        self.transition_matrix = transition_matrix
        self.stage = list(transition_matrix.keys())

        # Maps stage name -> numeric index (e.g. "Awake" -> 0)
        self.stage_to_id = {s: i for i, s in enumerate(self.stage)}

        # Maps numeric index -> stage name (e.g. 0 -> "Awake")
        self.id_to_stage = {i: s for s, i in self.stage_to_id.items()}

    def get_next_stage(self, current_stage):
        """
        Sample the next sleep stage from the transition probabilities.

        Arguments:
        
        - current_stage (str): The current stage ("Awake", "Light", "Deep", or "REM").

        Returns:
        
        - str: The next stage chosen at random using the transition matrix.
        """
        return np.random.choice(
            self.stage,
            p = [self.transition_matrix[current_stage][next_stage] for next_stage in self.stage]
        )

    def simulate(self, epoch_minutes=5, current_stage = "Awake", sleep_duration = 8):
        """
        Simulates a full night of sleep as a sequence of epochs.

        Arguments:

        - epoch_minutes (int): Length of each epoch in minutes.
        - current_stage (str): The starting stage is "Awake".
        - sleep_duration (int): Total sleep duration in hours.

        Returns:

        - list of str: Sequence of sleep stages, one per epoch.
        """
        # Number of epochs = (hours * 60) / epoch length
        steps = int((sleep_duration * 60) / epoch_minutes)

        sequence = [current_stage]
        current = current_stage

        # Sample the next stage for each epoch
        for _ in range(steps - 1):
            current = self.get_next_stage(current)
            sequence.append(current)
        return sequence

    def draw_abstract_art(self, stages, cols=12, cell=1.0, pad=0.12, jitter=0.10, bg="#0f0f10", save_path = "sleep_art.png"):
        """
        Render abstract art: one shape per epoch, colored by sleep stage.

        Arguments:

        - stages (list of str): Sequence of simulated sleep stages per epoch (ie. 96 items for 8h×5min).
        - cols (int): Number of epochs per row in the grid (default 12 = 1 hour of 5-min epochs).
        - cell (float): Size of each grid cell.
        - pad (float): Margin inside each cell so shapes don’t touch edges.
        - jitter (float): Random displacement applied to shapes (fraction of cell).
        - bg (str): Background color (hex code).
        - save_path (str): File path to save the abstract art PNG.

        """
        # Style mapping: stage -> color + shape
        STYLE = {
            "Awake": {"color": "#F6C90E", "shape": "circle"},
            "Light": {"color": "#5BC0EB", "shape": "square"},
            "Deep":  {"color": "#1B263B", "shape": "diamond"},
            "REM":   {"color": "#E83F6F", "shape": "triangle"},
        }
        # Ensures all stages have styles
        for s in self.stage:
            if s not in STYLE:
                raise ValueError(f"Unknown stage '{s}'. Expected one of {list(STYLE.keys())}")

        # number epochs to draw
        n = len(stages)
        rows = (n + cols - 1) // cols  # round up to fit all epochs
        width, height = cols * cell, rows * cell

        fig, ax = plt.subplots(figsize=(width * 0.55, height * 0.55), dpi=150)
        ax.set_facecolor(bg)

        # Shape size inside each cell
        r_shape = cell * (0.5 - pad)

        for i, st in enumerate(stages):
            r = i // cols
            c = i % cols
            y0 = (rows - 1 - r) * cell # row 0 is at the top
            x0 = c * cell

            # center of the cell with slight jitter
            cx = x0 + cell/2 + np.random.uniform(-jitter, jitter) * cell
            cy = y0 + cell/2 + np.random.uniform(-jitter, jitter) * cell

            spec = STYLE[st]
            color = spec["color"]
            shape = spec["shape"]

            # Pick the right shape based on stage
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

        # Save to file and close the figure
        fig.savefig(save_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)

    def graph_sleep(self, stage, epoch_minutes=5):
        """
        Plot a graph (timeline of stages) over the course of the night.

        Arguments:

        - stage (list of str): Sequence of simulated sleep stages.
        - epoch_minutes (int): Epoch length in minutes.
        """
        # x-axis = time in minutes
        times = np.arange(len(stage)) * epoch_minutes
        # y-axis = numeric encoding of sleep stages
        y_vals = [self.stage_to_id[s] for s in stage]

        plt.figure(figsize=(10, 4))
        plt.step(times, y_vals, where="post")

        # Label y-axis with stage names instead of numbers
        plt.yticks(range(len(self.stage)), self.stage)
        plt.xlabel("Time (minutes)")
        plt.ylabel("Stage")
        plt.title("Simulated Sleep Hypnogram")
        plt.tight_layout()
        plt.show()

def main():
    # Transition probabilities
    sleep_cycle = SleepCycle({
        "Awake": {"Awake": 0.7, "Light": 0.25, "Deep": 0.00, "REM": 0.05},
        "Light": {"Awake": 0.05, "Light": 0.70, "Deep": 0.15, "REM": 0.10},
        "Deep": {"Awake": 0.02, "Light": 0.20, "Deep": 0.70, "REM": 0.08},
        "REM": {"Awake": 0.05, "Light": 0.60, "Deep": 0.05, "REM": 0.30}
    })
    
    # Simulates 8 hours in 5-minute epochs (96 steps)
    stages = sleep_cycle.simulate(sleep_duration=8, epoch_minutes=5, current_stage="Awake")

    sleep_cycle.graph_sleep(stages, epoch_minutes=5)
    
    sleep_cycle.draw_abstract_art(stages, save_path="sleep_art.png")

if __name__ == "__main__":
    main()
