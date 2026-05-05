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
	
	@app.route("/read")
	@app.route("/read.html")
	def read():
		return render_template("read.html")
	
	@app.route("/currently-reading")
	@app.route("/currently-reading.html")
	def currently_reading():
		return render_template("currently-reading.html")
	
	@app.route("/to-be-read")
	@app.route("/to-be-read.html")
	def to_be_read():
		return render_template("to-be-read.html")
	
	@app.route("/did-not-finish")
	@app.route("/did-not-finish.html")
	def did_not_finish():
		return render_template("did-not-finish.html")
	
	@app.route("/my-reviews")
	@app.route("/my-reviews.html")
	def my_reviews():
		return render_template("my-reviews.html")