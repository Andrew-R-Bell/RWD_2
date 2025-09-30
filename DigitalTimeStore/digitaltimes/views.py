from flask import Blueprint, render_template, request, session, redirect, flash
from .models import Watch, Order, orderdetails
from datetime import datetime, timedelta
from .forms import CheckoutForm
from . import db
from sqlalchemy import or_

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    watches = Watch.query.order_by(Watch.id).all()
    return render_template('index.html', watches = watches)

@bp.route('/watch/<int:watchId>')
def details(watchId):
    watch = Watch.query.filter(Watch.id== watchId).first()
    return render_template('details.html', watch=watch)
    
@bp.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@bp.route('/contactus')
def contactus():
    return render_template('contactus.html')

@bp.route('/message')
def message():
    flash('Thank you for contacting us, we value your thoughts.', 'alert')
    return redirect('/')

@bp.route('/watches')
def search():
    watches = []
    sections = []
    search = request.args.get('search')
    if search is None or search == '':
        return redirect('/')
    search = search.split(' ')
    for i in range(len(search)):
        if search[i].lower() == 'watch' or search[i].lower() == 'watches':
           
            if range(len(search) == 1):
                return redirect('/')
            # Otherwise, ignore the term
            continue

        # Structure the search term as a wildcard
        searchFormatted = '%{}%'.format(search[i])
        watchesQuery = Watch.query.filter(or_(Watch.colour.like(searchFormatted), Watch.style.like(searchFormatted))).all()
        for watch in watchesQuery:
            # To ensure watches is a unique list
            if watch not in watches:
                # To ensure sections is a unique list
                if watch.style not in sections:
                    sections.append(watch.style)
                # Have to handle personalised watches seperately
                elif watch.colour == 'personalised' and watch.colour not in sections:
                    sections.append(watch.colour)
                watches.append(watch)

    # if nothing was found, redirect
    if watches == []:
        return redirect('/watch/not-found')
    return render_template('index.html', sections=sections, watches=watches)

@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    action = request.form.get('action')
    newWatchId = request.form.get('watchId')
    newWatch = None
    if newWatchId is not None:
        newWatch = Watch.query.get(newWatchId)
    quantities = []
    orderDetails = None
    zippedOrder = []
    totalCost = 0

    # Confirming whether the user has an active cart and retrieving it if so
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None
    
    # If the user never had an active cart
    if order is None:
        order = Order()
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('New order creation failed')
            order = None



# *****************
    if order is not None:
        # Else if the user is adding the watch to their cart
        if request.method == 'POST' and not action:

            # Checking if the watch already exists in the cart and increasing quantity by 1
            if newWatch in order.watches:
                # Retrieving the specific watch's quantity for that order
                quantity = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).filter(orderdetails.c.watch_id==newWatch.id).one()[0]
                quantity += 1
                increase = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.watch_id==newWatch.id).values(quantity=quantity)
                db.session.execute(increase)
            else:
                order.watches.append(newWatch)
                
        # Else if the user is increasing/decreasing the watch quantity in the cart
        elif request.method == 'POST' and action:
            # Retrieving the specific watch's quantity for that order
            quantity = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).filter(orderdetails.c.watch_id==newWatch.id).one()[0]
            if action == 'increase':
                quantity += 1
                increase = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.watch_id==newWatch.id).values(quantity=quantity)
                db.session.execute(increase)
            elif action == 'decrease':
                quantity -= 1
                decrease = orderdetails.update().where(orderdetails.c.order_id==order.id).where(orderdetails.c.watch_id==newWatch.id).values(quantity=quantity)
                db.session.execute(decrease)
                if quantity < 1:
                    order.watches.remove(newWatch)

        db.session.commit()       
        # Retrieving a list of quantities for every watch in the order, or an empty list
        quantities = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==order.id).all() or []
        # Converting from tuple to list
        quantities = [value for (value,) in quantities]

        # With logic complete, zipping the order's watches and quantities lists for parallel iteration in the client
        zippedOrder = zip(order.watches, quantities)
# *******************




        # Calculating the total order's cost sever-sided for security purposes
        if order is not None:
            # Using a while loop to allow for parallel list searching
            i = 0
            for watch in order.watches:
                while i in range(len(order.watches)):
                    totalCost += order.watches[i].price * quantities[i]
                    i += 1
    return render_template('cart.html', order=zippedOrder, totalCostValue=totalCost)

@bp.route('/emptycart', methods=['POST'])
def emptyCart():
    if 'order_id' in session:
        deleteOrder = orderdetails.delete().where(orderdetails.c.order_id==session['order_id'])
        db.session.execute(deleteOrder)
        db.session.commit()
        del session['order_id']
        flash('Your cart has been emptied.', 'alert')
    return redirect('/')

@bp.route('/checkout', methods=['POST'])
def checkout():
    form = CheckoutForm()
    orderCheck = None
    if 'order_id' in session:
        orderCheck = Order.query.get(session['order_id'])
        
        if form.validate_on_submit():
            orderCheck.completed = True
            orderCheck.datetime = datetime.now()
            orderCheck.name_first = form.firstName.data
            orderCheck.name_last = form.surname.data
            orderCheck.address = form.address.data
            orderCheck.email = form.email.data
            orderCheck.phone = form.phone.data

            # Calculating total cost
            i = 0
            totalCost = 0
            # Retrieving a list of quantities for every watch in the order
            quantities = db.session.query(orderdetails.c.quantity).filter(orderdetails.c.order_id==orderCheck.id).all()
            # Converting from tuple to list
            quantities = [value for (value,) in quantities]
            for watch in orderCheck.watches:
                while i in range(len(orderCheck.watches)):
                    totalCost += orderCheck.watches[i].price * quantities[i]
                    i += 1
            orderCheck.total_cost = totalCost
            db.session.commit()

            # Clear the user's session/cart
            del session['order_id']

            # Confirmation and redirection for user
            flash('Thank you for your purchase, your invoice will be emailed to you.', 'success')
            return redirect('/')
    return render_template('checkout.html', form=form)