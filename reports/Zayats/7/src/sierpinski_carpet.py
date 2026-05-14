"""Task 2, variant 4: Sierpinski carpet fractal builder."""

# pylint: disable=too-few-public-methods,duplicate-code

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tkinter import Button, Canvas, Entry, Frame, Label, StringVar, Tk, messagebox

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
CONTROL_WIDTH = 270
CANVAS_WIDTH = WINDOW_WIDTH - CONTROL_WIDTH
CANVAS_HEIGHT = WINDOW_HEIGHT
SCREENSHOT_PREFIX = "sierpinski_carpet"

BACKGROUND_COLOR = "#202124"
CARPET_COLOR = "#40c4ff"
HOLE_COLOR = "#202124"
PANEL_COLOR = "#303136"
TEXT_COLOR = "#f2f2f2"


@dataclass(frozen=True)
class CarpetParameters:
    """Parameters that affect the fractal appearance."""

    depth: int
    size: int
    offset_x: int
    offset_y: int
    carpet_color: str
    hole_color: str


@dataclass(frozen=True)
class SquareArea:
    """Square area used during recursive fractal building."""

    left: float
    top: float
    size: float


class SierpinskiCarpet:
    """Recursive Sierpinski carpet model."""

    def __init__(self, parameters: CarpetParameters) -> None:
        self.parameters = parameters

    def update_parameters(self, parameters: CarpetParameters) -> None:
        """Apply new fractal parameters."""
        self.parameters = parameters

    def draw(self, canvas: Canvas) -> None:
        """Draw the fractal on the canvas."""
        parameters = self.parameters
        canvas.create_rectangle(
            parameters.offset_x,
            parameters.offset_y,
            parameters.offset_x + parameters.size,
            parameters.offset_y + parameters.size,
            fill=parameters.carpet_color,
            outline=parameters.carpet_color,
        )
        self._cut_center_squares(
            canvas,
            SquareArea(parameters.offset_x, parameters.offset_y, parameters.size),
            parameters.depth,
        )

    def _cut_center_squares(
        self,
        canvas: Canvas,
        area: SquareArea,
        depth: int,
    ) -> None:
        """Recursively remove center squares from the carpet."""
        if depth <= 0:
            return

        next_size = area.size / 3
        center_left = area.left + next_size
        center_top = area.top + next_size

        canvas.create_rectangle(
            center_left,
            center_top,
            center_left + next_size,
            center_top + next_size,
            fill=self.parameters.hole_color,
            outline=self.parameters.hole_color,
        )

        for row in range(3):
            for column in range(3):
                if row == 1 and column == 1:
                    continue

                self._cut_center_squares(
                    canvas,
                    SquareArea(
                        area.left + column * next_size,
                        area.top + row * next_size,
                        next_size,
                    ),
                    depth - 1,
                )


class FractalApplication:
    """Window application for building a Sierpinski carpet."""

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Task 2: Sierpinski carpet")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.entries: dict[str, Entry] = {}
        self.status_text = StringVar(value="Fractal is ready")
        self.carpet = SierpinskiCarpet(
            CarpetParameters(
                depth=4,
                size=540,
                offset_x=95,
                offset_y=80,
                carpet_color=CARPET_COLOR,
                hole_color=HOLE_COLOR,
            )
        )

        self.canvas = Canvas(
            self.root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(side="left", fill="both")

        control_panel = Frame(
            self.root,
            width=CONTROL_WIDTH,
            bg=PANEL_COLOR,
            padx=16,
            pady=16,
        )
        control_panel.pack(side="right", fill="y")
        control_panel.pack_propagate(False)

        self._create_controls(control_panel)
        self.draw()

    def _create_controls(self, control_panel: Frame) -> None:
        """Create input controls for fractal parameters."""
        Label(
            control_panel,
            text="Sierpinski carpet",
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 13, "bold"),
        ).pack(anchor="w", pady=(0, 14))

        default_values = {
            "Depth": "4",
            "Size": "540",
            "Offset X": "95",
            "Offset Y": "80",
            "Carpet color": CARPET_COLOR,
            "Hole color": HOLE_COLOR,
        }

        for label_text, value in default_values.items():
            self._add_entry(control_panel, label_text, value)

        Button(
            control_panel,
            text="Build fractal",
            command=self.apply_parameters,
        ).pack(fill="x", pady=(12, 4))
        Button(
            control_panel,
            text="Save screenshot",
            command=self.save_screenshot,
        ).pack(fill="x", pady=4)

        Label(
            control_panel,
            textvariable=self.status_text,
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            wraplength=225,
            justify="left",
        ).pack(anchor="w", pady=(18, 0))

    def _add_entry(self, control_panel: Frame, label_text: str, value: str) -> None:
        """Add a labeled entry to the control panel."""
        Label(control_panel, text=label_text, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        entry = Entry(control_panel)
        entry.insert(0, value)
        entry.pack(fill="x", pady=(0, 6))
        self.entries[label_text] = entry

    def apply_parameters(self) -> None:
        """Read screen input and rebuild the fractal."""
        try:
            parameters = self._read_parameters()
            self.carpet.update_parameters(parameters)
            self.draw()
            self.status_text.set("Fractal rebuilt")
        except ValueError as error:
            messagebox.showerror("Input error", str(error))

    def draw(self) -> None:
        """Draw the current fractal."""
        parameters = self.carpet.parameters
        self.canvas.delete("all")
        self.canvas.configure(bg=parameters.hole_color)
        self.carpet.draw(self.canvas)

    def save_screenshot(self) -> None:
        """Save the current canvas image to the active directory."""
        filename = self._next_screenshot_name()
        self.canvas.postscript(file=filename, colormode="color")
        self.status_text.set(f"Screenshot saved: {filename}")

    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()

    def _read_parameters(self) -> CarpetParameters:
        """Read and validate fractal parameters from entries."""
        depth = int(self.entries["Depth"].get())
        size = int(self.entries["Size"].get())
        offset_x = int(self.entries["Offset X"].get())
        offset_y = int(self.entries["Offset Y"].get())
        carpet_color = self.entries["Carpet color"].get().strip()
        hole_color = self.entries["Hole color"].get().strip()

        if not 0 <= depth <= 6:
            raise ValueError("Depth must be from 0 to 6")

        if size <= 0:
            raise ValueError("Size must be positive")

        if offset_x < 0 or offset_y < 0:
            raise ValueError("Offsets must not be negative")

        if offset_x + size > CANVAS_WIDTH or offset_y + size > CANVAS_HEIGHT:
            raise ValueError("The carpet must fit inside the drawing area")

        if not carpet_color or not hole_color:
            raise ValueError("Colors must not be empty")

        return CarpetParameters(
            depth=depth,
            size=size,
            offset_x=offset_x,
            offset_y=offset_y,
            carpet_color=carpet_color,
            hole_color=hole_color,
        )

    @staticmethod
    def _next_screenshot_name() -> str:
        """Return an available screenshot filename in the active directory."""
        screenshot_number = 1

        while True:
            filename = f"{SCREENSHOT_PREFIX}_{screenshot_number}.ps"
            if not Path(filename).exists():
                return filename

            screenshot_number += 1


def main() -> None:
    """Application entry point."""
    FractalApplication().run()


if __name__ == "__main__":
    main()
