from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Product, Order, User
from app.forms import ProductForm
from app import db
from werkzeug.utils import secure_filename
import os
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@admin.route('/products')
@admin_required
def products():
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=all_products)

@admin.route('/add-product', methods=['GET', 'POST'])
@admin_required
def add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data
        )
        
        # Handle image upload
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            
            # Add timestamp to filename to avoid conflicts
            import time
            filename = f"{int(time.time())}_{filename}"
            
            filepath = os.path.join('app/static/uploads', filename)
            image_file.save(filepath)
            product.image_filename = filename
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/add_product.html', form=form)

@admin.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        
        # Handle image upload
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            
            # Add timestamp to filename
            import time
            filename = f"{int(time.time())}_{filename}"
            
            filepath = os.path.join('app/static/uploads', filename)
            image_file.save(filepath)
            
            # Delete old image if it's not a placeholder
            if product.image_filename and product.image_filename != 'placeholder.jpg':
                old_filepath = os.path.join('app/static/uploads', product.image_filename)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
            
            product.image_filename = filename
        
        db.session.commit()
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/edit_product.html', form=form, product=product)

@admin.route('/delete-product/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Delete image file if it exists and is not a placeholder
    if product.image_filename and product.image_filename != 'placeholder.jpg':
        filepath = os.path.join('app/static/uploads', product.image_filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{product.name}" deleted successfully!', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/orders')
@admin_required
def orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)

@admin.route('/order/<int:order_id>')
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)
