# auth.py
import streamlit as st
from typing import Optional, Dict, Any

from db import init_db, create_user, authenticate


def ensure_db_initialised() -> None:
    # safe to call multiple times
    init_db()


def require_user() -> Dict[str, Any]:
    """
    Ensure a user is logged in.
    If not, show signup / login UI and stop the app until they do.
    Returns: {"id": int, "email": str}
    """
    ensure_db_initialised()

    # already logged in in this session
    if "user" in st.session_state and st.session_state["user"] is not None:
        return st.session_state["user"]

    st.markdown("### 🔒 Sign in to save your 30-day plan")

    mode = st.radio(
        "Account",
        ["Log in", "Sign up"],
        horizontal=True,
        key="auth_mode",
    )

    email = st.text_input("Email", key="auth_email")
    password = st.text_input("Password", type="password", key="auth_password")

    error_placeholder = st.empty()

    def _handle_signup():
        if not email or not password:
            error_placeholder.error("Please enter email and password.")
            return
        try:
            user = create_user(email, password)
            st.session_state["user"] = user
            st.success("Account created. You are now logged in.")
            st.rerun()
        except ValueError as e:
            error_placeholder.error(str(e))

    def _handle_login():
        if not email or not password:
            error_placeholder.error("Please enter email and password.")
            return
        user = authenticate(email, password)
        if not user:
            error_placeholder.error("Incorrect email or password.")
            return
        st.session_state["user"] = user
        st.success("Welcome back.")
        st.rerun()

    if mode == "Sign up":
        if st.button("Create account"):
            _handle_signup()
    else:
        if st.button("Log in"):
            _handle_login()

    # Stop rendering rest of the page until user is authenticated
    st.stop()


def get_current_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get("user")
