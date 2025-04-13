from flask import Blueprint, render_template, make_response, redirect
from controllers.auth_controller import AuthController

# Cria o Blueprint "main_bp"
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=["GET", "POST"])
def home():
    return render_template('auth/login.html', methods=["GET", "POST"])

@main_bp.route('/register', methods=["GET", "POST"])
def register():
    return render_template('auth/register.html')

@main_bp.route('/chat')
def chat():
    if AuthController.is_authenticated: # retrona True ou False
        response = make_response(render_template('chat/index.html'))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return redirect("/")
