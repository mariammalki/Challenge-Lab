from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

BACK1_URL = os.environ.get("BACK1_URL", "http://back1-service:5001/users")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if name and email:
            try:
                requests.post(BACK1_URL.replace("/users", "/add_user"),
                              json={"name": name, "email": email}, timeout=5)
            except Exception as e:
                return f"Error contacting Back1: {str(e)}", 500
        return redirect("/")

    try:
        resp = requests.get(BACK1_URL, timeout=5)
        users = resp.json() if resp.status_code == 200 else []
    except Exception:
        users = []

    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
