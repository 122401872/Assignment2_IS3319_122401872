from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, json
from service.ProductService import ProductService
from Classes.ShoppingCart import ShoppingCart
from service.UserService import UserService
from init_db import get_db_connection
from werkzeug.utils import secure_filename
from Classes.User import User
import sqlite3
import requests
import os

# Initialize the Flask application
app = Flask(__name__)

# Generate a secret key for secure sessions
app.config['SECRET_KEY'] = os.urandom(24)
app.config['IMAGE_UPLOADS'] = os.path.join(app.root_path, 'static', 'images')

# Initialize services and shopping cart instance
ProductService = ProductService()
userService = UserService()
shopping_cart = ShoppingCart()

# Landing Page route
@app.route('/')
def LandingPage():
    return render_template('LandingPage.html')

@app.route('/api/jokes', methods=['GET'])
def getJokes():
    try:
        api_url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json() #directly parse JSON
            print("DUBUG: API RESPONSE", data)

            #returns resposne exactly as received
            return jsonify(data), 200
        else:
            print("DEBUG: API ERROR -- STATUS CODE {response.status_code}")
            return jsonify({"ERROR": "Failed to fetch quote"}), response.status_code
    except Exception as e:
        print("DEBUG: Exception occured", str(e))
        return jsonify({"ERROR": str(e)}), 500

# Display list of products
@app.route('/ProductSpread', methods=['GET', 'POST'])
def ProductSpread():
    console = request.args.get('console')  # Get the 'console' parameter from the query string
    print(f"Console filter received: {console}")  # Debugging

    if console:  # If a console filter is provided
        products = ProductService.get_products_by_console(console)  # Fetch filtered products
    else:
        products = ProductService.get_all_products()  # Fetch all products if no filter is applied

    # Fetch distinct console types for filtering options
    connection = sqlite3.connect("WorldGaming.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT console FROM products")
    consoles = [row[0] for row in cursor.fetchall()]
    connection.close()

    # Render the product spread page with products and filtering options
    return render_template('ProductSpread.html', Products=products, consoles=consoles, selected_console=console)



# Display details of a specific product
@app.route('/Product/<int:product_id>')
def show_product(product_id):
    Product = ProductService.get_product_details(product_id)
    Products = ProductService.get_all_products()
    return render_template('product_detail.html', Product=Product, Products=Products)

# Display the shopping cart
@app.route('/Cart')
def cart():
    cart = session.get('cart', [])  # Retrieve cart data from the session
    return render_template('Cart.html', cart=cart)

# Add an item to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user' not in session:
        flash('Please log in to add to your cart', 'error')
        return redirect(url_for('login'))

    product = ProductService.get_product_details(product_id)  # Fetch product details
    if product:
        # Retrieve the cart from the session or create a new one
        cart = session.get('cart', [])

        cart.append({
            'id': product.product_id,  # Ensure this is an integer
            'name': product.title,
            'description': product.description,
            'price': product.price,
            'quantity': 1,
        })

        session['cart'] = cart
        flash('Product added to cart!', 'success')
    else:
        flash('Product not found.', 'error')

    return redirect(url_for('cart'))

# Remove an item from the cart
@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'user' not in session:
        flash('Please log in to add to your cart', 'error')
        return redirect(url_for('login'))

    # Filter out the item to be removed
    cart = session.get('cart', [])
    cart = [product for product in cart if product['id'] != product_id]
    session['cart'] = cart  # Update the session cart
    flash('You have successfully removed the item', 'success')
    return redirect(url_for('cart'))  # Redirect to the cart page


@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    action = request.form.get('action')

    # Get the current quantity from the form (if provided)
    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    # Retrieve the current cart from the session
    cart = session.get('cart', [])

    # Loop through the cart items and update the one with the matching product ID
    for product in cart:
        if str(product['produtct_id']) == str(product_id):
            if action == 'increment':
                quantity += 1
            elif action == 'decrement' and quantity > 1:
                quantity -= 1
            # Update the item's quantity
            product['quantity'] = quantity
            break

    session['cart'] = cart  # Save the updated cart back into the session
    flash('Cart updated successfully!', 'success')
    return redirect(url_for('cart'))


# Admin dashboard route
@app.route('/Admin')
def admin():
    user = session.get('user')
    if not user or not user.get('isAdmin'):
        flash('Unauthorized')
        return redirect(url_for('ProductSpread'))
    return render_template('Admin.html')

# Log in functionality
@app.route('/LogIn', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login credentials from the form
        userEmail = request.form.get('emailField')
        userPassword = request.form.get('passwordField')

        # Validate the user using the UserService
        userToLogin = userService.get_user_by_email(userEmail)
        if userToLogin and userToLogin.userPassword == userPassword:  # Check password

            session['user'] = {
                'id': userToLogin.id,
                'first_name': userToLogin.first_name,
                'email': userToLogin.userEmail,
                'isAdmin': userToLogin.isAdmin
            }

            if userToLogin.isAdmin:
                return redirect(url_for('admin'))

            return redirect(url_for('ProductSpread'))

        flash('Invalid email or password', 'error')

    return render_template('LogIn.html')

# Log out functionality
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('LandingPage'))


# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':  # Handle form submission
        card_number = request.form.get('card-num')
        cardholder_name = request.form.get('name')
        expiration = request.form.get('exp')
        cvv = request.form.get('cvv')

        # Clear the cart after checkout
        session.pop('cart', None)
        flash('Thank you for your purchase! Your cart has been cleared.', 'success')
        return redirect(url_for('ProductSpread'))

    return render_template('Checkout.html')

@app.route('/Register')
def register():
    return render_template('Register.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    products = ProductService.get_all_products()
    return render_template('Products.html', Products=products)

@app.route('/EditProduct/<int:product_id>', methods=('GET', 'POST'))
@app.route('/add', methods=('GET', 'POST'), defaults={'product_id': None})
def EditProduct(product_id):
    conn = get_db_connection()

    # If editing, fetch the product
    product = None
    if product_id:
        product = conn.execute('SELECT * FROM products WHERE product_id = ?', (product_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        unique_attributes = request.form['unique_attributes']
        console = request.form['console']
        uploaded_image = request.files['image']

        image_filename = None  # This will store the filename to be saved in the database

        # Check if an image file was uploaded
        if uploaded_image and uploaded_image.filename != '':
            # Secure the filename
            filename = secure_filename(uploaded_image.filename)
            # Create the complete path to save the image
            image_path = os.path.join(app.config['IMAGE_UPLOADS'], filename)
            # Save the file to the directory
            uploaded_image.save(image_path)
            # Save just the filename (or a relative path) in the database
            image_filename = 'images/' + filename
        else:
            # If no new image is uploaded during edit, retain the existing image filename
            if product:
                image_filename = product['product_image_name']

        if product_id:  # Update existing product
            conn.execute(
                'UPDATE products SET title = ?, description = ?, product_image_name = ?, price = ?, unique_attributes = ?, console = ? WHERE product_id = ?',
                (title, description, image_filename, price, unique_attributes, console, product_id)
            )
        else:  # Insert new product
            conn.execute(
                'INSERT INTO products (title, description, product_image_name, price, unique_attributes, console) VALUES (?, ?, ?, ?, ?, ?)',
                (title, description, image_filename, price, unique_attributes, console)
            )

        conn.commit()
        conn.close()
        return redirect(url_for('products'))

    conn.close()
    return render_template('EditProduct.html', product=product)

@app.route('/delete/<int:product_id>')
def delete(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)
