from flask import Blueprint, request, jsonify
from db_utils import LocalSession, Orders, Products

orders_pages = Blueprint('orders', __name__, url_prefix='/orders')

session = LocalSession()

@orders_pages.route('/', methods=['GET'])
def list_orders():
    product_name = request.args.get("product")
    if product_name:
        product_query = session.query(Products).filter(Products.name==product_name).first()
        all_orders = session.query(Orders).filter(Orders.product_id==product_query.id)
    else: 
        all_orders = session.query(Orders).all()
        
    output_list = [] 
    for order in all_orders:
        output_list.append(dict(id=order.id,
                                actual_price=order.actual_price,
                                product_id=order.product_id))

    return jsonify(output_list)
    



@orders_pages.route('/<order_id>', methods=['GET'])
def get(order_id):
    get_order = session.query(Orders).filter(Orders.id==order_id).first()
    if get_order:
        order_dict = dict(id=get_order.id,
                        actual_price=get_order.actual_price,
                        product_id=get_order.product_id)
        return jsonify(order_dict)
    else:
        return jsonify({})

   


@orders_pages.route('/<order_id>', methods=['DELETE'])
def delete(order_id):
    order_to_delete = session.query(Orders).filter(Orders.id==order_id).first()
    if order_to_delete:
        session.delete(order_to_delete)
        session.commit()
        output_dict={"item_deleted_id": order_id}
        return jsonify(output_dict) 
    else:
        output_dict={"item_deleted_id": []}
        return jsonify(output_dict) 




@orders_pages.route('/<order_id>', methods=['PUT'])
def update(order_id):
    order_to_update = session.query(Orders).filter(Orders.id==order_id).first()
    if request.is_json and order_to_update :
        update_order = request.json
        update_order_price = update_order["actual_price"]
        order_to_update.actual_price = update_order_price
        order_dict = dict(id=order_to_update.id,
                     actual_price=order_to_update.actual_price,
                     product_id=order_to_update.product_id)
        session.commit()
        return  jsonify(order_dict)
    else:
        return  jsonify({})


    

@orders_pages.route('/', methods=['POST'])
def post():
    if request.is_json:
        new_order_details = request.json
        item_name = new_order_details["item"]
        get_product =  session.query(Products).filter(Products.name==item_name).first()

        if get_product:
            #make the order
            new_order = Orders(actual_price=new_order_details["actual_price"],
                            product_id= get_product.id)
            session.add(new_order)
            session.commit()
            return jsonify(new_order_details)
        else:
            return  jsonify({"message":"Check Product Options"})
    else:
        return jsonify({})

        

@orders_pages.route('/metrics', methods=['GET'])
def metrics():

    def get_total_actual_price(order_query):
        total_cost = 0
        for order_item in order_query:
            total_cost += order_item.actual_price
        return total_cost
    
    def calculate_dicount(total_actual_price,total_list_price):
        if total_list_price > 0:
            discount = (1 - (float(total_actual_price)/total_list_price)) * 100
            return round(discount)
        else:
            return 0

    all_products = session.query(Products).all()
    all_product_discount = []

    for product in all_products:
        product_id = product.id
        product_list_price = product.list_price
        all_product_orders =  session.query(Orders).filter(Orders.product_id==product_id)
        total_list_price = product_list_price * all_product_orders.count()
        total_actual_price = get_total_actual_price(all_product_orders)
        item_percentage = calculate_dicount(total_actual_price,total_list_price)
        all_product_discount.append(dict(product=product.name,total_discount=item_percentage))

    return jsonify(all_product_discount) 



