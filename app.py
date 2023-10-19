import logging
from flask import Flask , render_template, request, url_for, redirect, flash, session
from datetime import date, timedelta, datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session
from bson.objectid import ObjectId
from pymongo import MongoClient 

app=Flask(__name__) 
app.secret_key = "secret_key"
client = MongoClient("mongodb://localhost:27017")
db = client.library
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

@app.route("/", methods=('GET', 'POST'))
@app.route("/home", methods=('GET', 'POST'))
def home():
    app.logger.debug('/home')
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            password = generate_password_hash(password)
            email = request.form['email']
            db.users.insert_one({'username': username, 'password': password, 'email': email, 'loans' : []})
            flash('Registration Successful. Continue to login.')
            return redirect('/login')
        return render_template('home.html')
    except Exception as e:
        logger.exception(e)
        flash('Something went wrong. Please try again later.')
        return redirect('/home')

@app.route('/books/<string:genre>')
def books_by_genre(genre):
    try:
        books = db.books.find({'genre': genre})
        print(books)
        return render_template('book.html', genre=genre, books=books)
    except:
        return "There was an error finding books by genre."
    
@app.route("/commhome")
def commhome():
    try:
        books = db.books.find()
        genres = db.genre.find({'_id': '652d0308faaeeb31d214cec2'})
        result = db.genre.find_one()
        genres = result['genres']
        return render_template("comhome.html", books=books, genres=genres)
    except:
        return "There was an error displaying this page."

@app.route("/login", methods=["GET", "POST"])
def login():
    app.logger.debug('/login')
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = db.users.find_one({'username': username})
            admin = db.admin.find_one({'username': username, 'password': password})
            
            if admin:
                # logger.info(f'Admin {username} logged in.')
                session['username'] = username
                return redirect("/commhome")
            elif user and check_password_hash(user['password'], password):
                logger.info(f'User {username} logged in.')
                session['username'] = username
                flash(f'welcome {session.get("username")}')
                return redirect("/commhome")
            else:
                flash('Invalid credentials. Please enter correct details.')
                logger.warning(f'Invalid login attempt with username {username}.')
                return redirect('/login')
        return render_template("login.html")
    except Exception as e:
        logger.exception(e)
        flash('Something went wrong. Please try again later.')
        return redirect('/login')

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method=='POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publisher = request.form['publisher']
        release_date = request.form['release_date']
        isbn =  request.form['isbn']
        synopsis =  request.form['synopsis']
        avail_status =  request.form['avail_status']
        quantity = request.form['quantity']
        db.books.insert_one({'title': title, 'author': author, 'genre' : genre, 'publisher' : publisher,'release_date' : release_date, 'isbn' : isbn , 'synopsis' : synopsis,  'avail_status' : avail_status, 'quantity' : int(quantity)})
        db.genre.update_one({'_id':ObjectId('652d0308faaeeb31d214cec2')}, {'$addToSet': {'genres': genre}}, upsert=True)  # use $addToSet to prevent duplicates
        flash(f'{title} added successfully!!')
        return redirect("/add_book")
    return render_template("add_book.html")

@app.route('/book_details/<book_id>')
def book_details(book_id = ""):
    book = db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('book_details.html', book=book)

@app.route("/dashboard")
def dashboard():
    books = db.books
    num_books_available = books.count_documents({})
    users = db.users.find()
    c = 0
    for user in users:
        for loan in user['loans']:
            if loan['returned'] == False:
                c += 1
    # num_books_due = books.count_documents({'due_date': {'$lt': datetime.date.today()}})
    users = db.users
    num_users = users.count_documents({})
    total_quantity_available = 0
    for book in books.find():
        total_quantity_available += int(book['quantity'])
    return render_template('dashboard.html',num_users = num_users, num_books_available=num_books_available, total_quantity_available=total_quantity_available, c = c)

@app.route("/book")
def book():
    books = db.books.find()
    return render_template('book.html', books = books)

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.form['query']
    books = db.books.find({'title':query})
    if book:
        return render_template('book.html',books = books)
    else:
        flash('No books found')
        return redirect("/book")

@app.route('/del_books', methods=('GET', 'POST'))
def remove_book():
    if request.method=='POST':
        book_id = request.form['delv']
        book = db.books.find_one({'_id': ObjectId(book_id)})
        if not book:
            flash('Book not found.')
            return redirect('/book')

        if 'confirm_delete' in request.form:
            db.books.delete_one({'_id': ObjectId(book_id)})
            flash('Book  has been deleted.')
            return redirect('/book')
        else:
            flash('Please confirm deletion to remove the book.')
            return redirect('/book')

@app.route('/update_books', methods=('GET', 'POST'))
def update_book():
    if request.method=='POST':
        id = request.form['delv']
        res = db.books.find_one({'_id': ObjectId(id)})
        return (res['quantity'])

@app.route('/profile')
def profile():
    try:
        username = session.get('username')
        user = db.users.find_one({'username': username})
        # retrieve loans data from MongoDB
        loans = user['loans']
        return render_template('profile.html', user=user, loans=loans)
        
    except:
        return "Profile Updated Succussfully"

@app.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():
    # If the user submitted the form
    username = session.get('username')
    return render_template('manage_profile.html', user = username)

@app.route("/logout")
def logout():
    flash(f"{session.get("username")} logged out ")
    session["username"] = None
    return redirect("/login")

@app.route('/return_loan', methods=['POST'])
def return_loan():
    # retrieve user data from MongoDB
    username = session.get("username")
    user = db.users.find_one({'username': username})
    # update loans data in MongoDB
    loans = user['loans']
    loan_id = int(request.form['loan_id'])
    loans[loan_id]['returned'] = True
    db.list_collection_names.update_one({'_id': user['_id']}, {'$set': {'loans': loans}})
    # redirect to profile page
    flash(username)
    return redirect('/profile')

@app.route('/borrow', methods=['GET','POST'])
def borrow():
    if request.method == 'POST':
        username = session.get('username')
        title = request.form['title']
        id = request.form['id']
        today = date.today()
        loan_date = f"{today}"
        nextday = today + timedelta(days=14)
        due_date = f"{nextday}"
        if db.users.find_one({'username' : username}):
            db.users.find_one_and_update({'username' : username}, {"$push" : {"loans" : 
            {'title' : title, 
                'loan_date' : loan_date, 
                'due_date' : due_date, 
                'return_date' : "",
                'returned' : False}}}, upsert = True)
            book = db.books.find_one({'title' : title})
            book_quantity = book['quantity']
            book_quantity -= 1
            
            db.books.update_one({'title': title}, {'$set': {'quantity': book_quantity}})
        else:
            db.users.insert_one({'username' : username , 'loans' : {'title' : title, 'loan_date' : loan_date,'return_date' : "", 'due_date' : due_date,'returned' : False}})
        flash(f"borrowed Successfully, your due date is {due_date}")
        return redirect('/book')
    return render_template("/borrow")
   
@app.route('/reserve', methods=['GET','POST'])
def reserve():
    username = session.get('username')
    title = request.form['title']
    # Find the book with the given ID
    book = db.books.find_one({'title': title})
    quantity = book['quantity']
    quantity -= 1
    user = db.users.find_one({'username': username})
    today = date.today()
    reserve_date = f"{today}"
    # Update the book's quantity and reservation status
    db.books.update_one({'title': title}, {'$inc': {'quantity': quantity}, '$push': {'reservations': username}})
    
    # Update the user's reserved books list
    db.users.update_one({'username': username}, {'$push': {'reserved_books': {'title': title, 'reserved_date': reserve_date}}})
    
    flash(f"reserved Successfully")
    return redirect('/book')

@app.route('/book_return', methods=['GET', 'POST'])
@app.route('/book_return', methods=['GET', 'POST'])
def book_return():
    if request.method == 'POST':
        book_title = request.form['title']
        username = request.form['username']
        user = db.users.find_one({'username': username})
        print(username)
        fine_amount = 0
        if user:
            for loan in user['loans']:
                if loan['title'] == book_title:
                    due_date = datetime.strptime(loan['due_date'], '%Y-%m-%d').date()
                    return_date = date.today()
                    if return_date > due_date:
                        days_late = (return_date - due_date).days
                        fine_amount = days_late * 5 
        else:
            return "user not found"
        return_date = date.today()
        db.users.update_one(
            {
                'username': username,
                'loans.title': book_title
            },
            {
                '$set': {
                    'loans.$.returned': True,
                    'loans.$.returned_date': f'{return_date}',
                    'loans.$.fine_amount': fine_amount
                }
            }
        )
        flash(f'book having title : {book_title} returned successfully by {username} also collect fine amount : {fine_amount}')
        return redirect("/book_return")
    else:
        return render_template('book_return.html')

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        if action == 'delete':
            db.users.delete_one({'username': username})
            flash(f'User {username} has been deleted.')
            return redirect('/manage_users')
        elif action == 'view':
            user = db.users.find_one({'username': username})
            return render_template('profile.html', user=user)
        elif action == 'add':
            username = request.form['username']
            password = request.form['password']
            password = generate_password_hash(password)
            email = request.form['email']
            new_user = {
                'username': username,
                'password': password,
                'email': email,
                'loans': [],
                'reserved_books': []
            }
            db.users.insert_one(new_user)
            flash(f'User {username} has been added.')
            return redirect('/manage_users')
    else:
        users = db.users.find()
        return render_template('manage_users.html', users=users)


@app.route('/update_username', methods=['POST'])
def update_username():
    username_new = request.form['new_username']
    # update the username in the database
    username = session.get('username')
    db.users.update_one({'username': username}, {'$set': {'username': username_new}})
    return redirect(url_for('profile'))

# function to update the password
@app.route('/update_password', methods=['POST'])
def update_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    username = session.get('username')
    # check if the current password matches the password in the database
    user = db.users.find_one({'username': username})
    if user and  check_password_hash(user['password'], current_password):
        # check if the new password and confirm password match
        if new_password == confirm_password:
            # update the password in the database
            new_password = generate_password_hash(new_password)
            db.users.update_one({'username': username}, {'$set': {'password': new_password}})
            return "password updated successfully"
        else:
            flash('New password and confirm password do not match.')
    else:
        flash('Current password is incorrect.')
    return redirect(url_for('profile'))

# function to delete the account
@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    db.users.delete_one({'username': username})
    flash('Your account has been deleted.')
    return redirect(url_for('home'))
    

if __name__=='__main__':
    app.run(debug=True)