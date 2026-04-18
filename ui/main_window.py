"""
Author: Jiahang
Date: 2026-04-12
Description: Top-level launcher that routes authentication success into the main app window.
"""

from ui.login_window import LoginWindow
from ui.app_window import AppWindow


def main():
    """Launch the login flow and open the authenticated application after success."""
    def on_login(user):
        """Create the main application window for the authenticated user."""
        AppWindow(user).mainloop()

    LoginWindow(on_login_success=on_login).mainloop()
