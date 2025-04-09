from flask import Blueprint, render_template

main_routes = Blueprint("main", __name__)


@main_routes.route("/")
def index():
    return render_template("index.html", title="Home")


@main_routes.route("/about")
def about():
    return render_template("about.html", title="About Us")


@main_routes.route("/services")
def services():
    return render_template("services.html", title="Our Services")


@main_routes.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")
