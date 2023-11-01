import pandas as pd
import numpy as np

def transformar_columnas_datetime(orders, columnas):
    for columna in columnas:
        orders[columna] = pd.to_datetime(orders[columna], yearfirst = True)
    return orders

def tiempo_de_espera(orders, is_delivered=True):
    # filtrar por entregados y crea la varialbe tiempo de espera
    if is_delivered:
        orders = orders.query("order_status=='delivered'").copy()
    # compute wait time
    orders.loc[:, 'tiempo_de_espera'] = \
        (orders['order_delivered_customer_date'] -
         orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')
    orders.loc[:,'tiempo_de_espera_previsto'] = \
        (orders['order_estimated_delivery_date'] - 
         orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')
    return orders
    
def real_vs_esperado(orders,is_delivered=True):
    if is_delivered:
        orders = orders.query("order_status=='delivered'").copy()
    orders['real_vs_esperado'] = orders.apply(lambda x: max(0, x['tiempo_de_espera'] - x['tiempo_de_espera_previsto']), axis=1)
    return orders

def puntaje_de_compra(reviews):
    reviews['es_cinco_estrellas'] = reviews['review_score'].apply(lambda x: 1 if x == 5 else 0)
    reviews['es_una_estrella'] = reviews['review_score'].apply(lambda x: 1 if x == 1 else 0)
    return reviews[['order_id', 'es_cinco_estrellas', 'es_una_estrella', 'review_score']]

def calcular_numero_productos(data):
    items = data['order_items'].copy()
    return items.groupby('order_id').agg(number_of_product = ('product_id', 'count')).reset_index()

def vendedores_unicos(data):
    items = data['order_items'].copy()
    return items.groupby('order_id').agg(vendedores_unicos = ('seller_id', 'nunique')).reset_index()

def calcular_precio_y_transporte(data):
    items = data['order_items'].copy()
    return items.groupby('order_id').agg(precio = ('price', 'mean'), transporte = ('freight_value', 'mean')).reset_index()

from math import radians, sin, cos, asin, sqrt

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Computa distancia entre dos pares (lat, lng)
    Ver - (https://en.wikipedia.org/wiki/Haversine_formula)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))