from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api , Checkout

api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)
data = {
    "currency": "USD",
    "amount": 10000
}
url = checkout.url(data).get('checkout_url')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Item(db.Model):
   id= db.Column(db.Integer,primary_key=True)
   title= db.Column(db.String(100), nullable= False)
   price= db.Column(db.Integer, nullable= False)
   isActive= db.Column(db.Boolean, default= True)
   # image = db.Column(db.FileField,upload_to='img/')
   #text=  db.Column(db.Text, nullable= False)

   def __str__(self):
       return self.title



@app.route('/')
def index():
    item=Item.query.order_by(Item.price).all()
    return render_template('index.html',data=item)

@app.route('/product/<int:id>')
def index_details(id):
    item=Item.query.get(id)
    return render_template('product.html',data=item)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create',methods=['POST','GET'])
def create():
    if request.method=='POST':
        title = request.form['title']
        price=request.form['price']
        it = Item(title=title,price=price)
        try:
            db.session.add(it)
            db.session.commit()
            return redirect('/')
        except:
            print('erorr')
    else:
        return render_template('create.html')

@app.route('/product/<int:id>/delete')
def Delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True,port=2000)


