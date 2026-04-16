# Description:
# This file implements the main Tkinter window for the Expense Tracker.

from ui.login_window import LoginWindow


def _on_login(user):
    # Placeholder — main app window will be built in Task 2
    print(f"Logged in as: {user.username}")


def main():
    app = LoginWindow(on_login_success=_on_login)
    app.mainloop()
