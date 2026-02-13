import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    
    # User credentials loaded from Streamlit secrets
    try:
        USERS = st.secrets["credentials"]
    except Exception:
        st.error("⚠️ Credentials not configured. Please set up secrets in Streamlit.")
        return False
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state["username"].lower().strip()
        password = st.session_state["password"]
        
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = username.capitalize()
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["authenticated"] = False
    
    # Return True if already authenticated
    if st.session_state.get("authenticated", False):
        return True
    
    # Show login form
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Task Manager Login")
        st.markdown("---")
        
        st.text_input("Username", key="username", placeholder="Enter your username")
        st.text_input("Password", type="password", key="password", placeholder="Enter your password")
        
        if st.button("Login", use_container_width=True):
            password_entered()
        
        if st.session_state.get("authenticated") == False:
            st.error("😕 Username or password incorrect")
        
        st.markdown("---")
        st.caption("💡 Hint: Contact admin if you forgot your credentials")
    
    return False
