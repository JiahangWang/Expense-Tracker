"""
Author: Perfect
Date: 2026-04-15
Description: Main authenticated application window and navigation container.
"""

import tkinter as tk
from tkinter import messagebox

from ui.analytics_view import build_analytics
from ui.dashboard_view import build_dashboard
from ui.transactions_view import build_transactions


class AppWindow(tk.Tk):
    """Render the application shell and switch between the registered feature views."""

    def __init__(self, user, on_logout=None):
        """Create the main window and register the dashboard, transactions, and analytics pages."""
        super().__init__()
        self.title(f"Expense Tracker - {user.username}")
        self.geometry("900x560")
        self.minsize(800, 500)

        # Store the logged-in user and the currently mounted view state.
        self._user = user
        self._on_logout = on_logout
        self._views = {}
        self._active_btn = None

        self._build()
        self.register_view("Dashboard", build_dashboard(self._content, user))
        self.register_view("Transactions", build_transactions(self._content, user))
        self.register_view("Analytics", build_analytics(self._content, user))
        self._center()
        self.show_view("Dashboard")

    def _build(self):
        """Build the persistent sidebar and content host shared by all pages."""
        # Sidebar navigation stays visible while the right-hand content changes.
        sidebar = tk.Frame(self, bg="#1e293b", width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Expense\nTracker",
            bg="#1e293b",
            fg="white",
            font=("Helvetica", 13, "bold"),
            pady=24,
        ).pack()

        tk.Frame(sidebar, bg="#334155", height=1).pack(fill="x", padx=16)

        self._nav_buttons = {}
        for name in ("Dashboard", "Transactions", "Analytics"):
            btn = tk.Button(
                sidebar,
                text=name,
                anchor="w",
                padx=16,
                bg="#1e293b",
                fg="#94a3b8",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                font=("Helvetica", 10),
                cursor="hand2",
                command=lambda n=name: self.show_view(n),
            )
            btn.pack(fill="x", pady=2)
            self._nav_buttons[name] = btn

        actions = tk.Frame(sidebar, bg="#1e293b")
        actions.pack(side="bottom", fill="x", pady=16)

        tk.Button(
            actions,
            text="Log out",
            anchor="w",
            padx=16,
            bg="#1e293b",
            fg="#fbbf24",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            font=("Helvetica", 10, "bold"),
            cursor="hand2",
            command=self._logout,
        ).pack(fill="x")

        tk.Button(
            actions,
            text="Quit",
            anchor="w",
            padx=16,
            bg="#1e293b",
            fg="#fca5a5",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            font=("Helvetica", 10, "bold"),
            cursor="hand2",
            command=self._quit_app,
        ).pack(fill="x", pady=(6, 0))

        # The content frame is reused while individual child pages are swapped in and out.
        self._content = tk.Frame(self, bg="#f1f5f9")
        self._content.pack(side="left", fill="both", expand=True)

        # Placeholder frames keep navigation safe until the real page builders register views.
        for name in ("Dashboard", "Transactions", "Analytics"):
            frame = tk.Frame(self._content, bg="#f1f5f9")
            tk.Label(
                frame,
                text=f"{name} - coming soon",
                bg="#f1f5f9",
                fg="#94a3b8",
                font=("Helvetica", 14),
            ).place(relx=0.5, rely=0.5, anchor="center")
            self._views[name] = frame

    def show_view(self, name):
        """Display one registered view and update the selected sidebar button state."""
        for frame in self._views.values():
            frame.place_forget()

        frame = self._views[name]
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        if hasattr(frame, "refresh"):
            frame.refresh()

        if self._active_btn:
            self._active_btn.config(bg="#1e293b", fg="#94a3b8")
        btn = self._nav_buttons[name]
        btn.config(bg="#334155", fg="white")
        self._active_btn = btn

    def register_view(self, name, frame):
        """Replace one placeholder frame with the actual view implementation."""
        self._views[name] = frame

    def _logout(self):
        """Close the authenticated window and return the user to the login screen."""
        if not messagebox.askyesno("Log out", "Sign out of the current account?", parent=self):
            return

        self.destroy()
        if self._on_logout:
            self._on_logout()

    def _quit_app(self):
        """Close the entire application window."""
        if not messagebox.askyesno("Quit", "Close Expense Tracker?", parent=self):
            return

        self.destroy()

    def _center(self):
        """Center the window on the current screen."""
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        x_pos = (self.winfo_screenwidth() - width) // 2
        y_pos = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
