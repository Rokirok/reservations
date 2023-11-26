from app import app
from src.services.locations import view_customer_locations


@app.route('/locations/')
def list_locations():
    return view_customer_locations()