from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")

Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

# default landing page, shows list of restaurants
@app.route('/', methods=['GET'])
@app.route('/list_restaurants', methods=['GET'])
def list_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('list_records.html', restaurants=restaurants)

# view the list of menu's available for each restaurant
@app.route('/view_menu', methods=['GET'])
def list_menu():
    r_id = request.args.get("r_id")
    items = session.query(MenuItem).filter_by(restaurant_id=r_id).all()
    return render_template('list_menus.html', items=items)

# redirect to restaurant update page
@app.route('/edit_res', methods=['GET'])
def edit_res():
    r_id = request.args.get("r_id")
    res = session.query(Restaurant).filter_by(id=r_id).first()
    res_details = {'r_id': r_id, 'res_name': res.name}
    return render_template('edit_res.html', res_details=res_details)

# update each restaurant details
@app.route('/update_res', methods=['POST'])
def update_res():
    r_id = request.form.get("res_id")
    r_name = request.form.get("res_name")
    res = session.query(Restaurant).filter_by(id=r_id).first()
    res.name = r_name
    session.add(res)
    session.commit()
    return redirect(url_for('list_restaurants'))

# delete each restaurant
@app.route('/delete_res', methods=['GET'])
def delete_res():
    r_id = request.args.get("r_id")
    res = session.query(Restaurant).filter_by(id=r_id).first()
    session.delete(res)
    session.commit()
    return redirect(url_for('list_restaurants'))

# redirect to menu item update page
@app.route('/edit_men', methods=['GET'])
def edit_men():
    m_id = request.args.get("m_id")
    r_id = request.args.get("r_id")
    men = session.query(MenuItem).filter_by(id=m_id).first()
    men_details = {'m_id': m_id, 'men_name': men.name, 'men_price': men.price, 'men_desc': men.description, 'men_course': men.course, 'r_id': r_id}
    return render_template('edit_men.html', men_details=men_details)

# update each menu item
@app.route('/update_men', methods=['POST'])
def update_men():
    m_id = request.form.get("men_id")
    r_id = request.form.get("res_id")
    m_name = request.form.get("men_name")
    m_price = request.form.get("men_price")
    m_desc = request.form.get("men_description")
    m_course = request.form.get("men_course")
    menu = session.query(MenuItem).filter_by(id=m_id).first()
    menu.price = m_price
    menu.name = m_name
    menu.desc = m_desc
    menu.course = m_course
    session.add(menu)
    session.commit()
    return redirect(url_for('list_menu', r_id=r_id))

# delete each menu item
@app.route('/delete_men', methods=['GET'])
def delete_men():
    m_id = request.args.get("m_id")
    r_id = request.args.get("r_id")
    menu = session.query(MenuItem).filter_by(id=m_id).first()
    session.delete(menu)
    session.commit()
    return redirect(url_for('list_menu', r_id=r_id))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)