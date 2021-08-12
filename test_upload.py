import requests
import json
import random, string
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder


def send(videofile, id_stream, object_name):
    current_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(current_date)
    id_new = ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # test

    current_enterprise = '0KVmDvc9'
    # crée racine
    table_name = 'IA_RESULT'
    url_sync_put = 'http://api5.securemotion.fr/modules/gabarit/api/securemotion/sync_put.php?current_enterprise=0KVmDvc9&tbl_name=' + table_name
    print(url_sync_put)

    # créer data à envoyer
    send_data = [{"id": id_new, "created_on": current_date, "deleted_on": "", "updated_on": current_date,
                  "_id_stream": id_stream, "_id_object": object_name}]
    json_dump = json.dumps(send_data)

    send_me = {"tbl_name": table_name, "_id_login": "server", "db_data": json_dump}
    print(send_me)

    r = requests.post(url_sync_put, json=send_me)
    r.status_code

    print('envoi ok')
    filename = videofile
    id_file = ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # test

    # créer data à envoyer
    json_file = [
        {"id": id_file, "created_on": current_date, "deleted_on": "", "article_id": id_new, "updated_on": current_date}]
    json_dump = json.dumps(json_file)

    print('id_file => ' + id_file)

    ext_file = "avi"
    url_upload = 'http://api5.securemotion.fr/acces/api/sql/file/upload.php?current_enterprise=0KVmDvc9&db=' + table_name + "&table=" + table_name + "&id_file=" + id_file

    multipart_data = MultipartEncoder(
        fields={
            # a file upload field
            'file': (filename, open(filename, 'rb'), 'text/plain'),
            'id_file': id_file,
            'ext_file': ext_file,
            'cat': '0',
            'article_id': id_new,
            'json_file': json_dump,
            'db_name': table_name,
            'db_mode': 'mysql',
            'current_enterprise': current_enterprise,
            'url_client': '',
            'source_type': 'android'
        }
    )

    response = requests.post(url_upload, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
