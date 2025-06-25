from flask import Flask,request,render_template,redirect,url_for
app=Flask(__name__)

user_data={} #to store users data
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        print(request.form)
        username=request.form['username']
        email=request.form['email']
        password=request.form['pwd']
        pin=request.form['pin']
        print(user_data)
        if username not in user_data:
            user_data[username]={'password':password,'pin_no':pin,'email':email,'amount':0} #update user_data with new account
            print(user_data)
        else:
            return "Username already existed"
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username'] #user give login username
        password=request.form['pwd'] #user give login password
        #Now we need to verify the stored data that wheather the user give login details are correct or not
        if username in user_data:
            if password == user_data[username]['password']:
                return redirect(url_for('dashboard',passed_username=username))
            else:
                return 'Password is incorrect'
        else:
            return 'Username is incorrect'
       
    return render_template('login.html')

@app.route('/dashboard/<passed_username>')
def dashboard(passed_username):
    return render_template('dashboard.html',template_username=passed_username)

@app.route('/deposit/<username>',methods=['GET','POST'])
def deposit(username):
    if request.method=="POST":
        user_amount=int(request.form['amount'])
        if user_amount<=0 or user_amount>50000:
            return f'Amount invalid you need to specify between 1 and 50000'
        elif user_amount>=0 and user_amount<=50000:
            user_data[username]['amount']=user_data[username]['amount']+user_amount
            return redirect(url_for('balance',username=username))

    return render_template('deposit.html')

@app.route('/balance/<username>')
def balance(username):
    balance_amount=user_data[username]['amount']
    return render_template('balance.html',balance_amount=balance_amount)

@app.route('/withdraw/<username>',methods=['GET','POST'])
def withdraw(username):
    if request.method=="POST":
        user_amount=int(request.form['amount'])
        balance=user_data[username]['amount'] #stored balance
        if user_amount>balance:
            return f'Amount exceeded.Please check your balance'
        elif user_amount<=0:
            return 'Enter amount in positive values'
        elif user_amount>=0 and user_amount<balance:
            user_data[username]['amount']=user_data[username]['amount']-user_amount
            return redirect(url_for('balance',username=username))
        else:
            return 'Invalid data'
    return render_template('withdraw.html')

@app.route('/delete_acccount/<username>')
def delete_acc(username):
    user_data.pop(username)
    return redirect(url_for('home'))

@app.route('/logout/<username>')
def logout(username):
    return redirect(url_for('login'))
    
app.run(use_reloader=True)
