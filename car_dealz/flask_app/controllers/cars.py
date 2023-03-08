from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car


@app.route('/dashboard')
def r_dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id']
        } 
    logged_in_user = User.get_by_id(data)
    cars = Car.get_all_cars()
    theUser = User.get_all()
    return render_template("dashboard.html", logged_in_user = logged_in_user, cars = cars, users = theUser)

@app.route('/show/<int:car_id>')
def r_one(car_id):
    wrapped_user= {
        "id": session["user_id"]
    }
    logged_in_user = User.get_by_id(wrapped_user)
    theCar = Car.get_by_id(car_id)
    theUser = User.get_all()
    return render_template("show.html", logged_in_user=logged_in_user, theCar = theCar, users = theUser)

@app.route('/new')
def r_new():
    user = User.get_by_id({'id': session['user_id']})
    return render_template("new.html", logged_in_user = user)

@app.route('/saveCar', methods=['POST'])
def saveCar():
    if not Car.validate_new_car(request.form):
        return redirect ('/new')
    data = {
        'model': request.form['model'],
        'make': request.form['make'],
        'description': request.form['description'],
        'year': request.form['year'],
        'price': request.form['price'],
        'user_id': session['user_id']
    }
    Car.save_car(data)
    return redirect('/dashboard')

@app.route("/edit/<int:car_id>")
def edit_car(car_id):
    vehicle = Car.get_by_id(car_id)
    wrapped_user = {
        "id": session['user_id']
    }
    logged_in_user = User.get_by_id(wrapped_user)
    return render_template('edit.html', logged_in_user = logged_in_user, car = vehicle)

@app.route("/editCar/<int:car_id>", methods=['POST'])
def carEdit(car_id):
    if not Car.validate_new_car(request.form):
        return redirect(f'/edit/{car_id}')
    data = {
        'id': car_id,
        'model': request.form['model'],
        'make': request.form['make'],
        'description': request.form['description'],
        'year': request.form['year'],
        'price': request.form['price'],
        'user_id': session['user_id']
    }
    Car.update_car(data)
    print("boop")
    return redirect("/dashboard")

@app.route("/purchaseCar/<int:car_id>")
def purchaseCar(car_id):
    Car.delete_car(car_id)
    return redirect("/dashboard")

@app.route("/deleteCar/<int:car_id>")
def delete_by_id(car_id):
    Car.delete_car(car_id)
    return redirect("/dashboard")

'''request.form, session['user_id']'''