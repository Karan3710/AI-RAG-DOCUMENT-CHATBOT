import streamlit as st
import bcrypt
from db import users_collection


# ---------------------------
# Init Session
# ---------------------------
def init_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


# ---------------------------
# Hash Password
# ---------------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# ---------------------------
# Verify Password
# ---------------------------
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)


# ---------------------------
# Signup
# ---------------------------
def signup():
    st.sidebar.subheader("🆕 Signup")

    new_user = st.sidebar.text_input("Username", key="signup_user")
    new_pass = st.sidebar.text_input("Password", type="password", key="signup_pass")

    if st.sidebar.button("Create Account"):
        if users_collection.find_one({"username": new_user}):
            st.sidebar.error("User already exists ❌")
        else:
            hashed_pw = hash_password(new_pass)

            users_collection.insert_one({
                "username": new_user,
                "password": hashed_pw
            })

            st.sidebar.success("Account created ✅")


# ---------------------------
# Login
# ---------------------------
def login():
    st.sidebar.subheader("🔐 Login")

    username = st.sidebar.text_input("Username", key="login_user")
    password = st.sidebar.text_input("Password", type="password", key="login_pass")

    if st.sidebar.button("Login"):
        user = users_collection.find_one({"username": username})

        if user and verify_password(password, user["password"]):
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.sidebar.success(f"Welcome {username} 👋")
        else:
            st.sidebar.error("Invalid credentials ❌")


# ---------------------------
# Logout
# ---------------------------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.sidebar.success("Logged out ✅")