from flask import Flask, render_template
from os import getenv
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import src.routes.authentication
import src.routes.dashboard
import src.routes.admin_dashboard
import src.routes.customer


@app.route('/')
def index():
    return render_template('customer/landing_page.html')


if __name__ == '__main__':
    app.run()
