"""Simple desktop IDE for Apophis programs.

This module provides a lightweight Tkinter based editor to create and
execute Apophis programs.  It allows opening and saving ``.apop`` files as
well as running the contents of the editor using :func:`apophis.run_apophis`.
Basic editing features such as undo/redo, cut/copy/paste and a status bar
that tracks the cursor position are provided to make the environment more
comfortable for day to day use.

The GUI is intentionally minimal but can serve as a foundation for a more
feature complete IDE.  The :class:`ApophisIDE` class exposes ``open_file``,
``save_file`` and ``run_code`` methods which are used by the graphical
interface and can also be invoked programmatically which facilitates
basic unit testing.
"""
from __future__ import annotations

from pathlib import Path
import contextlib
from tkinter import (
    Tk,
    Text,
    Menu,
    END,
    INSERT,
    Label,
    filedialog,
    messagebox,
)

import apophis


class ApophisIDE:
    """Tiny Tkinter based IDE for the Apophis language."""

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Apophis IDE")
        self.text = Text(self.root, wrap="none", undo=True)
        self.text.pack(fill="both", expand=True)
        self.status = Label(self.root, anchor="w")
        self.status.pack(fill="x", side="bottom")
        self.file_path: Path | None = None
        self._create_menu()
        self._bind_events()
        self.update_status_bar()

    # GUI setup ---------------------------------------------------------
    def _create_menu(self) -> None:
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut", command=lambda: self.text.event_generate("<<Cut>>")
        )
        edit_menu.add_command(
            label="Copy", command=lambda: self.text.event_generate("<<Copy>>")
        )
        edit_menu.add_command(
            label="Paste", command=lambda: self.text.event_generate("<<Paste>>")
        )
        edit_menu.add_command(
            label="Select All",
            command=lambda: self.text.event_generate("<<SelectAll>>"),
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        self.root.config(menu=menu_bar)

    # File operations ---------------------------------------------------
    def new_file(self) -> None:
        """Clear the editor and reset the current file."""
        self.text.delete("1.0", END)
        self.file_path = None
        self.update_status_bar()

    def open_file(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Apophis files", "*.apop *.apo"), ("All files", "*.*")]
        )
        if path:
            self.file_path = Path(path)
            self.text.delete("1.0", END)
            self.text.insert(END, self.file_path.read_text(encoding="utf-8"))
            self.update_status_bar()

    def save_file(self) -> None:
        if self.file_path is None:
            self.save_file_as()
            return
        self.file_path.write_text(self.text.get("1.0", END), encoding="utf-8")

    def save_file_as(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".apop",
            filetypes=[("Apophis files", "*.apop"), ("All files", "*.*")],
        )
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

    # Editing helpers --------------------------------------------------
    def undo(self) -> None:
        """Undo the last edit."""
        with contextlib.suppress(Exception):
            self.text.edit_undo()

    def redo(self) -> None:
        """Redo the last undone edit."""
        with contextlib.suppress(Exception):
            self.text.edit_redo()

    def update_status_bar(self, _event: object | None = None) -> None:
        """Update the status bar with the current cursor position."""
        line, col = self.text.index(INSERT).split(".")
        self.status.config(text=f"Ln {int(line)}, Col {int(col) + 1}")

    def _bind_events(self) -> None:
        self.text.bind("<KeyRelease>", self.update_status_bar)
        self.text.bind("<ButtonRelease>", self.update_status_bar)
        self.root.bind("<Control-n>", lambda _e: self.new_file())
        self.root.bind("<Control-o>", lambda _e: self.open_file())
        self.root.bind("<Control-s>", lambda _e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda _e: self.save_file_as())
        self.root.bind("<Control-r>", lambda _e: self.run_code())


def launch() -> None:
    """Launch the graphical Apophis IDE."""
    ide = ApophisIDE()
    ide.mainloop()


__all__ = ["ApophisIDE", "launch"]
