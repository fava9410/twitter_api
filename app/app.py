import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# load credentials
with open('app/credentials.json') as f:
    credentials = json.load(f)

db_credentials = credentials['database']
twitter_credentials = credentials['twitter_api']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}/{db_credentials["db"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Portfolio(db.Model):
    idportfolio = db.Column(db.Integer, primary_key=True)
    twitter_user_name = db.Column(db.String(255))
    names = db.Column(db.String(255))
    last_names = db.Column(db.String(255))

    def __init__(self, twitter_user, names, last_names):
        self.twitter_user_name = twitter_user
        self.names = names
        self.last_names = last_names

class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('twitter_user_name', 'names', 'last_names', 'idportfolio')
    
portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)

@app.route('/users', methods=['GET'])
def get_users():
    all_portfolios = Portfolio.query.all()
    result = portfolios_schema.dump(all_portfolios)
    return jsonify(result)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    portfolio = Portfolio.query.get_or_404(id)
    return portfolio_schema.jsonify(portfolio)

@app.route('/create_user', methods=['POST'])
def create_user():
    names = request.form.get('names')
    last_names = request.form.get('last_names')
    twitter_user = request.form.get('twitter_user')

    new_portfolio = Portfolio(twitter_user, names, last_names)

    db.session.add(new_portfolio)
    db.session.commit()

    return portfolio_schema.jsonify(new_portfolio)

@app.route('/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    portfolio = Portfolio.query.get_or_404(id)
    db.session.delete(portfolio)
    db.session.commit()

    return portfolio_schema.jsonify(portfolio)

@app.route('/update_user/<id>', methods=['PUT'])
def update_user(id):
    portfolio = Portfolio.query.get_or_404(id)

    portfolio.names = request.form.get('names')
    portfolio.last_names = request.form.get('last_names')
    portfolio.twitter_user = request.form.get('twitter_user')

    db.session.commit()

    return portfolio_schema.jsonify(portfolio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)