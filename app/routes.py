from flask import Flask, render_template


def register_routes(app: Flask) -> None:
	@app.route("/")
	def home():
		return render_template("home.html")
