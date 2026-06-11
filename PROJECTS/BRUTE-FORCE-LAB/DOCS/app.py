from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt
import time
from datetime import datetime

# =========================================
# Flask App Configuration
# =========================================

app = Flask(__name__)
app.secret_key = 'supersecretkey'


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

@app.errorhandler(RateLimitExceeded)
def rate_limit_handler(e):
    return """
    <h1>Too Many Requests</h1>
    <p>You have exceeded the login limit.</p>
    <p>Please wait one minute before trying again.</p>
    """, 429

# =========================================
# Security Settings
# =========================================

FAILED_ATTEMPTS = {}
SUSPICIOUS_IPS = {}
LOCKOUT_TIME = 30      # seconds
MAX_ATTEMPTS = 5

FAILED_IPS = {}
IP_MAX_ATTEMPTS = 10
IP_LOCKOUT_TIME = 60

# =========================================
# Logging System
# =========================================

ATTEMPT_COUNTER = 0

def log_attempt(username, success):

    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1

    ip = request.remote_addr

    if not success:

        if ip not in SUSPICIOUS_IPS:
            SUSPICIOUS_IPS[ip] = 1
        else:
            SUSPICIOUS_IPS[ip] += 1

    user_agent = request.headers.get('User-Agent')
    status = 'SUCCESS' if success else 'FAILED'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"""
====================================================
ATTEMPT #{ATTEMPT_COUNTER}
TIME: {timestamp}
USERNAME: {username}
STATUS: {status}
IP: {ip}
USER-AGENT: {user_agent}
====================================================
"""
    alert = ""

    if ip in SUSPICIOUS_IPS and SUSPICIOUS_IPS[ip] >= 10:

        alert = f"""
    ⚠ SUSPICIOUS IP DETECTED
    IP: {ip}
    FAILED ATTEMPTS: {SUSPICIOUS_IPS[ip]}
    """



    with open('logs/attempts.log', 'a') as f:
        f.write(log_entry)

        if alert:
            f.write(alert)

# =========================================
# Routes
# =========================================

@app.route('/')
def home():
    return redirect('/login')

# =========================================
# LOGIN
# =========================================

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        ip = request.remote_addr

        if ip in FAILED_IPS:

            attempts, first_time = FAILED_IPS[ip]

            if attempts >= IP_MAX_ATTEMPTS:

                elapsed = time.time() - first_time

                if elapsed < IP_LOCKOUT_TIME:

                    remaining = int(IP_LOCKOUT_TIME - elapsed)

                    return f"""
                    <h1>IP Blocked</h1>
                    <p>Too many failed attempts from this IP.</p>
                    <p>Try again in {remaining} seconds.</p>
                    """

                else:
                    FAILED_IPS[ip] = [0, time.time()]




        # -----------------------------
        # Lockout protection
        # -----------------------------

        if username in FAILED_ATTEMPTS:

            attempts, first_time = FAILED_ATTEMPTS[username]

            if attempts >= MAX_ATTEMPTS:

                elapsed = time.time() - first_time

                if elapsed < LOCKOUT_TIME:

                    remaining = int(LOCKOUT_TIME - elapsed)

                    return f"""
                    <h1>Account Locked</h1>
                    <p>Too many failed attempts.</p>
                    <p>Try again in {remaining} seconds.</p>
                    """

                else:
                    FAILED_ATTEMPTS[username] = [0, time.time()]

        # -----------------------------
        # Database check
        # -----------------------------

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        user = cur.fetchone()
        conn.close()

        # -----------------------------
        # Password check
        # -----------------------------

        if user:

            stored_password = user[0]

            if bcrypt.checkpw(password.encode(), stored_password):

                session['user'] = username
                log_attempt(username, True)

                if username in FAILED_ATTEMPTS:
                    FAILED_ATTEMPTS.pop(username)

                if ip in FAILED_IPS:
                    FAILED_IPS.pop(ip)



                return redirect('/admin')

        # -----------------------------
        # Failed login handling
        # -----------------------------

        if username not in FAILED_ATTEMPTS:
            FAILED_ATTEMPTS[username] = [1, time.time()]
        else:
            FAILED_ATTEMPTS[username][0] += 1


        if ip not in FAILED_IPS:
            FAILED_IPS[ip] = [1, time.time()]
        else:
            FAILED_IPS[ip][0] += 1

        log_attempt(username, False)

        error = "Invalid username or password"

    return render_template('login.html', error=error)

# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route('/admin')
def admin():

    if 'user' not in session:
        return redirect('/login')

    try:
        with open('logs/attempts.log', 'r') as f:
            logs = f.readlines()

        logs = logs[::-1]

    except:
        logs = ["No logs available"]

    return render_template(
        'admin.html',
        user=session['user'],
        logs=logs
    )

# =========================================
# LOGS API (LIVE FEED)
# =========================================

@app.route('/logs')
def get_logs():

    try:
        with open('logs/attempts.log', 'r') as f:
            logs = f.readlines()

        logs = logs[::-1]

    except:
        logs = ["No logs available"]

    return {"logs": logs}

# =========================================
# LOGOUT
# =========================================

@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect('/login')

# =========================================
# RUN APP
# =========================================

if __name__ == '__main__':
    app.run(debug=True)