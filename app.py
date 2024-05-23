from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
import bcrypt
import random
from flask_mail import Mail, Message
import pandas as pd
import os
import subprocess
from flask import jsonify



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://broadash8:root123@erps.orr74gt.mongodb.net/ERP" # replace with your MongoDB URI
mongo = PyMongo(app)

mail = Mail(app)

app.config['SECRET_KEY'] = b'secretkey'

app.config['MAIL_SERVER'] = 'smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'servererp41@gmail.com'
app.config['MAIL_PASSWORD'] = '36B72D446DC3D4DB6BAB9E40E89367264ED6'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL']=False
#app.config['MAIL_DEFAULT_SENDER'] = 'shubham.tp05@gmail.com'  # Replace with your email


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_password = request.form['user_password']
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        
        mongo.db.users.insert_one({'name': name, 'email': email, 'password': hashed_password})
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            flash('Please enter email and password', 'error')
            return redirect(url_for('login'))
        
        user = mongo.db.users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = user['name']  
            flash('You have been successfully logged in.', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/run_dashboard')
def run_dashboard():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))
    subprocess.Popen(["streamlit", "run", "dashboard.py"])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        mobile = request.form['mobile']
        message = request.form['message']
        mongo.db.contact.insert_one({'first_name': first_name, 'last_name': last_name, 'email': email, 'mobile': mobile, 'message': message})
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact_us.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        plan = request.args.get('plan')
        name = request.form['name']
        email = request.form['email']
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        exp_date = request.form['exp_date']
        cvv = request.form['cvv']
        # Store payment details in the database
        mongo.db.payment.insert_one({'plan': plan, 'name': name, 'email': email, 'card_type': card_type, 'card_number': card_number, 'exp_date': exp_date, 'cvv': cvv})
        flash('Payment successful!', 'success')
        if 'email' in session:
            session['email']=email
            try:
                msg = Message('Thank You for Your Purchase', sender='servererp41@gmail.com', recipients=[email])
                msg.body = 'Thank You For Your Purchase!!!!'
                mail.send(msg)
                flash('Email sent successfully!', 'success')
            except Exception as e:
                flash(b'Error sending email: {str(e)}', 'error')
        else:
            flash('No email found in session.', 'error')
    
        return redirect(url_for('index'))
       
    return render_template('payment.html')
@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        try:
            # Save the uploaded file
            file.save(file.filename)
            # Read the Excel file
            df = pd.read_excel(file.filename)
            # Convert DataFrame to JSON for easy handling in JavaScript
            data = df.to_dict(orient='records')
            # Optionally, you can delete the uploaded file if not needed
            os.remove(file.filename)
            # Store data in session or database for later retrieval
            session['inventory_data'] = data
            return jsonify({'success': True, 'data': data})
        except Exception as e:
            return jsonify({'error': str(e)})

    # Modify your search route to use the uploaded Excel data for searching   
@app.route('/search', methods=['POST'])
def search():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
                # Read the Excel file
            df = pd.read_excel(file)
                # Convert DataFrame to JSON for easy handling in JavaScript
            data = df.to_dict(orient='records')
                # Store data in session or database for later retrieval
            session['inventory_data'] = data
            return jsonify({'success': True, 'data': data})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/add-item', methods=['POST'])
def additem():
    return render_template ('inventory.html')

@app.route('/remove-item', methods=['POST'])
def removeitem():
    return render_template ('inventory.html')

@app.route('/update_quantity', methods=['POST'])
def updatequantity():
    return render_template ('inventory.html')
# Modify your search route to use the uploaded Excel data for searching   

@app.route('/about')
def about():
    return render_template('about_us.html')

if __name__ == "__main__":    
    app.run(debug=True)


