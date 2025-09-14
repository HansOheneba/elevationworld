from flask import Blueprint, render_template, request, flash, redirect, url_for
from sheets import append_to_sheet, append_registration, check_email_exists
import random

main_routes = Blueprint("main", __name__)


SPIRITUAL_MESSAGES = [
    "Registration successful — welcome to God’s family!",
    "Form submitted — heaven rejoices with you today!",
    "Details saved — may God guide your journey.",
    "Registration complete — you are part of our family now.",
    "Success — your soul has found a home here.",
    "Submitted — blessings on your decision today!",
    "Saved — we’ll grow and worship together.",
    "Registration received — your journey with Elevation starts now!",
]

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
            email = request.form.get("email")
            form_data = {
                "email": email,
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

            # Check if email already exists
            if check_email_exists(email):
                flash(
                    "This email is already registered. If you need to update your information, please contact us for assistance.",
                    "info",
                )
                return render_template(
                    "attend.html", title="Attend", form_data=form_data
                )

            # Append to Google Sheet
            success = append_registration(form_data)

            if success:
                # Select a random spiritual message
                spiritual_message = random.choice(SPIRITUAL_MESSAGES)
                flash(f"Registration successful! {spiritual_message}", "success")
                return redirect(url_for("main.attend"))
            else:
                flash("Error submitting registration. Please try again.", "error")

        except Exception as e:
            print(f"Error in registration: {e}")
            flash("An error occurred. Please try again.", "error")

    return render_template("attend.html", title="Attend")
