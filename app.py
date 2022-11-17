import configparser

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session
from helpers import apology, login_required
from player import Game
from save import db_get_users, db_write_user

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

config = configparser.ConfigParser()
config.read('.env')
API_KEY = config["section"]["API_KEY"]

if not API_KEY:
    raise RuntimeError("API_KEY not set")


db = "database.db"
gme = None

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """landing page for starting a game"""
    if request.method == "GET":
        return render_template("index.html")
    else:
        # Start Game: Generate Game
        global gme
        gme = Game()
        print("Game Created")
        # Go to select Category 
        return redirect("select")


@app.route("/select", methods=["GET", "POST"])
@login_required
def select():
    """selection page for difficulty and category"""
    if request.method == "GET":
        categories = gme.categories
        diff = ["easy", "medium", "hard"]
        return render_template("select.html", categories=categories, diff=diff)
    else:
        cat = int(request.form.get("category"))
        gme.setCategory(cat)
        diff = request.form.get("diff")
        gme.setDifficulty(diff)
        return redirect("quest")

@app.route("/quest", methods=["GET", "POST"])
@login_required
def quest():
    if request.method == "GET":
        if request.args.get("translate") == "t":
            gme.question.translateQ()
        else:
            gme.getNewQuestion()
        return render_template("quest.html", question=gme.question, correct_index=gme.question.correct_index)
    else:
        if request.form.get("correct") == "true":
            flash("Correct")
            return redirect("select")
        else:
            flash("Incorrect")
            return render_template("quest.html", question=gme.question, correct_index=gme.question.correct_index)

        
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        rows = db_get_users(conn=db, user=(username,))
        print(type(rows), rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # GET
    if request.method == "GET":
        return render_template("register.html")
    # POST
    else:
        username = request.form.get("username")
        pw = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Validate user input
        if username is None or username == "":
            return apology("Please provide a username")
        #Check that username does not exist already
        usernames = db_get_users(conn=db, user=(username,))
        if not len(usernames) == 0:
            return apology("Username already exists")
        if pw is None or pw == "":
            return apology("Please provide a password")
        if not pw == confirmation:
            return apology("Passwords no not match")
        db_write_user(conn=db, user=(username,generate_password_hash(pw)))
        return redirect("/")
