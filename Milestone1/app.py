import os
import sqlite3
import hashlib
import hmac
import secrets
import smtplib
import jwt
import streamlit as st
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone

DB_NAME = "users.db"
JWT_SECRET = os.environ.get("JWT_SECRET")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

st.set_page_config(
    page_title="Infosys Authentication System",
    page_icon="🔐",
    layout="centered"
)

if not JWT_SECRET:
    st.error("JWT_SECRET is missing. Restart the app using the Colab launcher.")
    st.stop()

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS password_otps (
                email TEXT PRIMARY KEY,
                otp_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0
            )
        """)

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(),
        bytes.fromhex(salt), 200000
    ).hex()

def create_token(username):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

def get_logged_in_user():
    token = st.session_state.get("jwt_token")
    if not token:
        return None
    try:
        return jwt.decode(
            token, JWT_SECRET, algorithms=["HS256"]
        )["username"]
    except jwt.InvalidTokenError:
        st.session_state.pop("jwt_token", None)
        return None

def send_otp(email, otp):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email secrets are missing.")

    message = EmailMessage()
    message["Subject"] = "Password Reset OTP"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email
    message.set_content(
        f"Your password reset OTP is {otp}.\n"
        "It expires in 5 minutes. Do not share this code."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)

create_table()

st.title("🔐 User Authentication System")
st.caption("Infosys Springboard Internship 7.0 | Batch 4 | Milestone 1")

logged_in_user = get_logged_in_user()

if logged_in_user:
    st.success(f"Welcome, {logged_in_user}!")
    st.subheader("User Dashboard")
    st.write("You have successfully logged in.")
    st.write("Your session uses a JWT token.")

    if st.button("Logout"):
        st.session_state.pop("jwt_token", None)
        st.rerun()

else:
    page = st.sidebar.selectbox(
        "Choose Page",
        ["Login", "Signup", "Forgot Password", "Admin Login"]
    )

    if page == "Admin Login":
        st.subheader("Admin Login")

        if st.session_state.get("admin_logged_in", False):
            st.success("Admin authenticated")
            st.subheader("Registered Users")

            with connect_db() as conn:
                users = conn.execute(
                    "SELECT username, email FROM users ORDER BY username"
                ).fetchall()

            if users:
                st.dataframe(
                    [{"Username": u, "Email": e} for u, e in users],
                    use_container_width=True
                )
            else:
                st.info("No registered users found.")

            if st.button("Admin Logout"):
                st.session_state.pop("admin_logged_in", None)
                st.rerun()

        else:
            admin_username = st.text_input("Admin Username")
            admin_password = st.text_input(
                "Admin Password", type="password"
            )

            if st.button("Admin Login"):
                expected_username = os.environ.get("ADMIN_USERNAME")
                expected_password = os.environ.get("ADMIN_PASSWORD")

                if (
                    admin_username == expected_username
                    and hmac.compare_digest(
                        admin_password, expected_password
                    )
                ):
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid admin credentials.")

    elif page == "Signup":
        st.subheader("Create an Account")
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            username = username.strip()
            email = email.strip().lower()

            if not username or not email or not password:
                st.error("Please fill in all fields.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Enter a valid email address.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                salt = os.urandom(16).hex()
                password_hash = hash_password(password, salt)
                try:
                    with connect_db() as conn:
                        conn.execute(
                            """INSERT INTO users
                            (username, email, password_hash, salt)
                            VALUES (?, ?, ?, ?)""",
                            (username, email, password_hash, salt)
                        )
                    st.success("Account created. Please log in.")
                except sqlite3.IntegrityError:
                    st.error("Username or email is already registered.")

    elif page == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            with connect_db() as conn:
                user = conn.execute(
                    """SELECT password_hash, salt FROM users
                    WHERE username = ?""",
                    (username.strip(),)
                ).fetchone()

            if user and hmac.compare_digest(
                hash_password(password, user[1]), user[0]
            ):
                st.session_state["jwt_token"] = create_token(username.strip())
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    elif page == "Forgot Password":
        st.subheader("Reset Password with Email OTP")
        email = st.text_input("Registered Email Address").strip().lower()

        if st.button("Send OTP"):
            if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
                st.error("Email settings are missing. Restart the app.")
            else:
                with connect_db() as conn:
                    user = conn.execute(
                        "SELECT id FROM users WHERE email = ?", (email,)
                    ).fetchone()

                if not user:
                    st.error("No account found for that email.")
                else:
                    otp = f"{secrets.randbelow(1000000):06d}"
                    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
                    expires = (
                        datetime.now(timezone.utc) + timedelta(minutes=5)
                    ).isoformat()

                    try:
                        send_otp(email, otp)
                        with connect_db() as conn:
                            conn.execute(
                                """INSERT OR REPLACE INTO password_otps
                                (email, otp_hash, expires_at, attempts)
                                VALUES (?, ?, ?, 0)""",
                                (email, otp_hash, expires)
                            )
                        st.session_state["reset_email"] = email
                        st.success("OTP sent to your registered email.")
                    except Exception:
                        st.error("Could not send OTP. Check Gmail settings.")

        reset_email = st.session_state.get("reset_email")

        if reset_email:
            st.info(f"Enter the OTP sent to: {reset_email}")
            entered_otp = st.text_input("6-digit OTP")
            new_password = st.text_input("New Password", type="password")
            confirm_new = st.text_input(
                "Confirm New Password", type="password"
            )

            if st.button("Reset Password"):
                with connect_db() as conn:
                    record = conn.execute(
                        """SELECT otp_hash, expires_at, attempts
                        FROM password_otps WHERE email = ?""",
                        (reset_email,)
                    ).fetchone()

                if not record:
                    st.error("Please request a new OTP.")
                elif record[2] >= 5:
                    st.error("Too many attempts. Request a new OTP.")
                elif datetime.now(timezone.utc) >= datetime.fromisoformat(
                    record[1]
                ):
                    st.error("OTP expired. Request a new one.")
                elif not hmac.compare_digest(
                    hashlib.sha256(entered_otp.encode()).hexdigest(),
                    record[0]
                ):
                    with connect_db() as conn:
                        conn.execute(
                            """UPDATE password_otps SET attempts = attempts + 1
                            WHERE email = ?""",
                            (reset_email,)
                        )
                    st.error("Incorrect OTP.")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters.")
                elif new_password != confirm_new:
                    st.error("Passwords do not match.")
                else:
                    new_salt = os.urandom(16).hex()
                    new_hash = hash_password(new_password, new_salt)

                    with connect_db() as conn:
                        conn.execute(
                            """UPDATE users SET password_hash = ?, salt = ?
                            WHERE email = ?""",
                            (new_hash, new_salt, reset_email)
                        )
                        conn.execute(
                            "DELETE FROM password_otps WHERE email = ?",
                            (reset_email,)
                        )

                    st.session_state.pop("reset_email", None)
                    st.success("Password reset successful. Please log in.")
