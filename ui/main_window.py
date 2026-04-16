# Description:
# This file implements the main Tkinter window for the Expense Tracker.

from ui.login_window import LoginWindow
from ui.app_window import AppWindow


def main():
    def on_login(user):
        AppWindow(user).mainloop()

    LoginWindow(on_login_success=on_login).mainloop()
