import xmlrpclib

username = 'admin'
password = 'password123'
dbname = 'erp_dev'
sock_common = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/common')
sock_object = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/object')
uid = sock_common.login(dbname, username, password)

values = {}
values.update({'name': 'Pricelist01'})
values.update({'type': 'sale'})
sock_object.execute(dbname, uid, password, 'product.pricelist', 'create', values)