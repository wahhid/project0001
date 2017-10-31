import csv
import xmlrpclib

username = 'admin'
password = 'P@ssw0rd'
dbname = '2017'
sock_common = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/common')
sock_object = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/object')
uid = sock_common.login(dbname, username, password)


args = []
product_ids = sock_object.execute(dbname, uid, password, 'product.product', 'search', args)
products = sock_object.execute(dbname, uid, password, 'product.product', 'read', product_ids, ['default_code'])
for product in products:
    if product.get('default_code'):
        default_code = product.get('default_code')
        values = {}
        values.update({'default_code':default_code.strip()})
        print values
        sock_object.execute(dbname, uid, password, 'product.product', 'write', [product.get('id')], values )
