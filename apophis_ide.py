"""Simple desktop IDE for Apophis programs.

This module provides a lightweight Tkinter based editor to create and
execute Apophis programs.  It allows opening and saving ``.apop`` files as
well as running the contents of the editor using :func:`apophis.run_apophis`.

The GUI is intentionally minimal but can serve as a foundation for a more
feature complete IDE.  The :class:`ApophisIDE` class exposes ``open_file``,
``save_file`` and ``run_code`` methods which are used by the graphical
interface and can also be invoked programmatically which facilitates
basic unit testing.
"""
from __future__ import annotations

from pathlib import Path
from tkinter import Tk, Text, Menu, END, filedialog, messagebox

import apophis


class ApophisIDE:
    """Tiny Tkinter based IDE for the Apophis language."""

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Apophis IDE")
        self.text = Text(self.root, wrap="none")
        self.text.pack(fill="both", expand=True)
        self.file_path: Path | None = None
        self._create_menu()

    # GUI setup ---------------------------------------------------------
    def _create_menu(self) -> None:
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        self.root.config(menu=menu_bar)

    # File operations ---------------------------------------------------
    def open_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Apophis files", "*.apop *.apo"), ("All files", "*.*")])
        if path:
            self.file_path = Path(path)
            self.text.delete("1.0", END)
            self.text.insert(END, self.file_path.read_text(encoding="utf-8"))

    def save_file(self) -> None:
        if self.file_path is None:
            self.save_file_as()
            return
        self.file_path.write_text(self.text.get("1.0", END), encoding="utf-8")

    def save_file_as(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".apop", filetypes=[("Apophis files", "*.apop"), ("All files", "*.*")])
        if path:
            self.file_path = Path(path)
            self.save_file()

    # Execution --------------------------------------------------------
    def run_code(self) -> None:
        code = self.text.get("1.0", END)
        try:
            output = apophis.run_apophis(code)
            messagebox.showinfo("Output", output)
        except Exception as exc:  # pragma: no cover - GUI only
            messagebox.showerror("Error", str(exc))

    # Convenience ------------------------------------------------------
    def mainloop(self) -> None:
        """Start the Tkinter main event loop."""
        self.root.mainloop()


def launch() -> None:
    """Launch the graphical Apophis IDE."""
    ide = ApophisIDE()
    ide.mainloop()


__all__ = ["ApophisIDE", "launch"]
