from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, current_app
from app.models import Product, Order, OrderItem
from app import db
from flask_login import current_user, login_required
import razorpay
import hashlib
import hmac

main = Blueprint('main', __name__)

@main.route('/')
def home():
    featured_products = Product.query.limit(6).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    return render_template('home.html', featured_products=featured_products, categories=categories)

@main.route('/products')
def products():
    # Get search and filter parameters
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    # Base query
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%') | 
                           Product.description.ilike(f'%{search_query}%'))
    
    # Apply category filter
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    all_products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('products.html', 
                         products=all_products, 
                         categories=categories,
                         search_query=search_query,
                         category_filter=category_filter)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add or update product in cart
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': product.price,
            'image': product.image_filename,
            'quantity': 1
        }
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({
        'success': True, 
        'message': f'{product.name} added to cart!',
        'cart_count': sum(item['quantity'] for item in cart.values())
    })

@main.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, total=total)

@main.route('/update-cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' in session:
        cart = session['cart']
        product_id_str = str(product_id)
        
        if quantity > 0:
            if product_id_str in cart:
                cart[product_id_str]['quantity'] = quantity
        else:
            if product_id_str in cart:
                del cart[product_id_str]
        
        session['cart'] = cart
        session.modified = True
    
    return redirect(url_for('main.cart'))

@main.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            del cart[product_id_str]
            session['cart'] = cart
            session.modified = True
            flash(f'Item removed from cart.', 'success')
    
    return redirect(url_for('main.cart'))

@main.route('/checkout')
@login_required
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.products'))
    
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('checkout.html', cart_items=cart_items, total=total)

@main.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        return jsonify({'success': False, 'message': 'Your cart is empty!'}), 400
    
    # Calculate total in paise (Razorpay requires amount in paise)
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    amount_in_paise = int(total * 100)
    
    # Create Razorpay order
    client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], 
                                   current_app.config['RAZORPAY_KEY_SECRET']))
    
    try:
        razorpay_order = client.order.create(dict(
            amount=amount_in_paise,
            currency='INR',
            receipt='receipt_' + str(current_user.id)
        ))
        
        # Create order in database with pending status
        order = Order(
            user_id=current_user.id, 
            total_price=total, 
            status='Pending',
            payment_id=razorpay_order['id']
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for product_id, item in cart_items.items():
            order_item = OrderItem(
                order_id=order.id,
                product_id=int(product_id),
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Return Razorpay order details
        return jsonify({
            'success': True,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': current_app.config['RAZORPAY_KEY_ID'],
            'amount': amount_in_paise,
            'order_id': order.id,
            'email': current_user.email,
            'contact': request.form.get('phone', ''),
            'name': current_user.username
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/verify-payment', methods=['POST'])
@login_required
def verify_payment():
    data = request.get_json()
    
    try:
        client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], 
                                       current_app.config['RAZORPAY_KEY_SECRET']))
        
        # Verify the payment signature
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })
        
        # Update order status to Completed
        order = Order.query.filter_by(
            payment_id=data['razorpay_order_id'],
            user_id=current_user.id
        ).first()
        
        if order:
            order.status = 'Completed'
            db.session.commit()
            
            # Clear cart
            session.pop('cart', None)
            session.modified = True
            
            return jsonify({
                'success': True, 
                'message': 'Payment verified successfully!',
                'order_id': order.id
            })
        else:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
            
    except razorpay.BadRequestsError as e:
        return jsonify({'success': False, 'message': 'Payment verification failed'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Ensure user can only view their own orders
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.home'))
    
    return render_template('order_success.html', order=order)

@main.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)
