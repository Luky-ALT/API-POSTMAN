from flask import Flask,jsonify, request

app = Flask(__name__)

customers = [
    {
        "email" : "jan.novak@example.cz",
        "username" : "johny",
        "name" : "Jan Novák",
        "newsletter_status" : True,
        "trips" : [
            {
                "destination" : "Oslo, Norway",
                "price" : 150.00
            },
            {
                "destination" : "Bangkok, Thailand",
                "price" : 965.00
            }
        ]
    },
    {
        "email" : "ivan.opletal@example.com",
        "username" : "ivan123",
        "name" : "Ivan Opletal",
        "newsletter_status" : False,
        "trips" : []
    }
]
# returnig of all customers
@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers),200


# returnig of customer
@app.route("/customers/<string:username>", methods=["GET"])
def get_customer(username):
    for customer in customers:
        if customer["username"] == username:
            return jsonify(customer),200
    return jsonify({"message":"customer not found"}),404

#creating of new customer

@app.route("/customer", methods=["POST"])
def create_customer():
    request_data = request.get_json()
    new_customer = {
        "email": request_data['email'],
        "username": request_data['username'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }
    for customer in customers:
        if customer["username"] == new_customer["username"]:
            return jsonify({"error":"username already exist"})
        customer.append(new_customer)
        return jsonify(new_customer)

#returning all trips of customers
@app.route("/customer/<string:username>/trips", methods=["GET"])
def get_trip_in_users(username):
    for customer in customers:
        if customer["username"] ==username:
            return jsonify({"trips": customer["trips"]})
    return jsonify({"message" :"username not found"})

#creating a new trip of customer
@app.route("/customer/<string:username>/trips", methods=["POST"])
def create_trip_in_user(username):
    for customer in customers:
        if customer["username"] == username:
            request_data = request.get_json()
            new_trip ={
                "destination": request_data['destination'],
                "price": request_data['price']
            }
            customer["trips"].append(new_trip)
            return new_trip
    return jsonify({"message":"username not found"})


# Úprava existujícího, popř, vytvoření neexistujícího zákazníka
@app.route('/customer/<string:username>', methods=['PUT'])
def update_customer(username):
    request_data = request.get_json()
    updated_customer = {
        "email": request_data['email'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }
    for customer in customers:
        if username == customer['username']:
            customer.update(request_data)
            return updated_customer, 201
    customers.append(updated_customer)
    return updated_customer
# Vymazání zákazníka
@app.route('/customer/<string:username>', methods=['DELETE'])
def delete_customer(username):
    for customer in customers:
        if username == customer['username']:
            customers.remove(customer)
            return jsonify({'message': 'customer was successfully removed'})
    return jsonify({'message': 'username not found'}), 404


app.run(port=80,debug = True)