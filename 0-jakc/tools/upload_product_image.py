import os
from os.path import basename
import csv
import xmlrpclib
import base64

username = 'admin'
password = 'P@ssw0rd'
dbname = '2017'
sock_common = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/common')
sock_object = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/object')
uid = sock_common.login(dbname, username, password)

rootdir = '/Users/wahhid/Google Drive/Project/0001 - BCP/Import Data/Gambar/WEB FIC BCP'

def find_product(default_code):
    args = [('default_code', '=', default_code)]
    ids = sock_object.execute(dbname, uid, password, 'product.template', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.template', 'read', ids[0])
    else:
        return False

def update_image(product_id, image):
    vals = {}
    vals.update({'image_medium': image})
    return sock_object.execute(dbname, uid, password, 'product.template', 'write', [product_id], vals)


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = os.path.join(subdir, file)
        print filepath
        filebase = os.path.splitext(basename(filepath))[0]
        print filebase
        filebase_rev = filebase.replace("-",".")
        product = find_product(filebase_rev)
        if product:
            with open(filepath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                update_image(product.get('id'), encoded_string)
                print "convert successfully"
        else:
            print "convert failed"