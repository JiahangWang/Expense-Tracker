import tkinter as tk
from ui.dashboard_view import build_dashboard
from ui.transactions_view import build_transactions
from ui.analytics_view import build_analytics


class AppWindow(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title(f"Expense Tracker — {user.username}")
        self.geometry("900x560")
        self.minsize(800, 500)
        self._user = user
        self._views = {}
        self._active_btn = None
        self._build()
        self.register_view("Dashboard", build_dashboard(self._content, user))
        self.register_view("Transactions", build_transactions(self._content, user))
        self.register_view("Analytics", build_analytics(self._content, user))
        self._center()
        self.show_view("Dashboard")

    def _build(self):
        # Sidebar
        sidebar = tk.Frame(self, bg="#1e293b", width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="Expense\nTracker",
            bg="#1e293b", fg="white",
            font=("Helvetica", 13, "bold"), pady=24
        ).pack()

        tk.Frame(sidebar, bg="#334155", height=1).pack(fill="x", padx=16)

        self._nav_buttons = {}
        for name in ("Dashboard", "Transactions", "Analytics"):
            btn = tk.Button(
                sidebar, text=name, anchor="w", padx=16,
                bg="#1e293b", fg="#94a3b8",
                activebackground="#334155", activeforeground="white",
                relief="flat", font=("Helvetica", 10), cursor="hand2",
                command=lambda n=name: self.show_view(n),
            )
            btn.pack(fill="x", pady=2)
            self._nav_buttons[name] = btn

        # Content area
        self._content = tk.Frame(self, bg="#f1f5f9")
        self._content.pack(side="left", fill="both", expand=True)

        # Placeholder frames (replaced in later tasks)
        for name in ("Dashboard", "Transactions", "Analytics"):
            frame = tk.Frame(self._content, bg="#f1f5f9")
            tk.Label(
                frame, text=f"{name} — coming soon",
                bg="#f1f5f9", fg="#94a3b8", font=("Helvetica", 14)
            ).place(relx=0.5, rely=0.5, anchor="center")
            self._views[name] = frame

    def show_view(self, name):
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
        """Replace a placeholder with a real view frame."""
        self._views[name] = frame

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
