import tkinter as tk
from tkinter import messagebox

from auth.auth_manager import AuthManager
class LoginWindow(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()
        self.title("Expense Tracker — Login")
        self.resizable(False, False)
        self._auth = AuthManager()
        self._on_login_success = on_login_success
        self._build()
        self._center()

    def _build(self):
        frame = tk.Frame(self, padx=30, pady=30)
        frame.pack()

        tk.Label(frame, text="Expense Tracker", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        tk.Label(frame, text="Username").grid(row=1, column=0, sticky="w")
        self._username = tk.Entry(frame, width=24)
        self._username.grid(row=1, column=1, pady=4)

        tk.Label(frame, text="Password").grid(row=2, column=0, sticky="w")
        self._password = tk.Entry(frame, show="*", width=24)
        self._password.grid(row=2, column=1, pady=4)
        self._password.bind("<Return>", lambda _: self._login())

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(16, 0))
        tk.Button(btn_frame, text="Login", width=10, command=self._login).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Register", width=10, command=self._do_register).pack(side="left", padx=6)

    def _login(self):
        try:
            ok, msg, user = self._auth.login(self._username.get(), self._password.get())
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc), parent=self)
            return

        if ok:
            self.destroy()
            self._on_login_success(user)
        else:
            messagebox.showerror("Login Failed", msg, parent=self)

    def _do_register(self):
        try:
            ok, msg = self._auth.register(self._username.get(), self._password.get())
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc), parent=self)
            return

        if ok:
            messagebox.showinfo("Registered", msg + " You can now log in.", parent=self)
        else:
            messagebox.showerror("Registration Failed", msg, parent=self)

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")
