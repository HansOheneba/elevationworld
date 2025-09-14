from flask import Blueprint, render_template, request, flash, redirect, url_for
from sheets import append_to_sheet, append_registration
from datetime import datetime

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


@main_routes.route("/attend", methods=["GET", "POST"])
def attend():
    if request.method == "POST":
        try:
            # Check if consent was given
            if not request.form.get("consent"):
                flash("You must agree to the consent terms to register.", "error")
                return render_template("attend.html", title="Attend")

            # Get all form data
            form_data = {
                "email": request.form.get("email"),
                "firstname": request.form.get("firstname"),
                "lastname": request.form.get("lastname"),
                "phonenumber": request.form.get("phonenumber"),
                "gender": request.form.get("gender"),
                "age_bracket": request.form.get("age_bracket"),
                "occupation": request.form.get("occupation"),
            }

            # Validate required fields
            required_fields = [
                "email",
                "firstname",
                "lastname",
                "phonenumber",
                "gender",
                "age_bracket",
                "occupation",
            ]
            for field in required_fields:
                if not form_data.get(field):
                    flash(f"Please fill in the {field} field.", "error")
                    return render_template(
                        "attend.html", title="Attend", form_data=form_data
                    )

            # Append to Google Sheet using the new function
            success = append_registration(form_data)

            if success:
                flash(
                    "Registration successful! Welcome to the Elevation World family!",
                    "success",
                )
                return redirect(url_for("main.attend"))
            else:
                flash("Error submitting registration. Please try again.", "error")

        except Exception as e:
            print(f"Error in registration: {e}")
            flash("An error occurred. Please try again.", "error")

    return render_template("attend.html", title="Attend")
