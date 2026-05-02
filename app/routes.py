from flask import Flask, render_template


def register_routes(app: Flask) -> None:
	@app.route("/")
	def home():
		return render_template("home.html")

	@app.route("/profile")
	@app.route("/profile.html")
	def profile():
		return render_template("profile.html")

	@app.route("/login")
	@app.route("/login.html")
	def login():
		return render_template("login.html")

	@app.route("/signup")
	@app.route("/signup.html")
	def signup():
		return render_template("signup.html")

	@app.route("/edit-profile")
	@app.route("/edit-profile.html")
	def edit_profile():
		return render_template("edit-profile.html")