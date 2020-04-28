import os
import sys


def get_database_config():
    return {
        'db_host': os.environ['FANTASY_PI_DB_HOST'],
        'db_name': os.environ['FANTASY_PI_DB_NAME'],
        'db_user': os.environ['FANTASY_PI_DB_USER'],
        'db_pass': os.environ['FANTASY_PI_DB_PORT'],
        'db_port': os.environ['FANTASY_PI_DB_PASS']
    }

class flask_config_template(object):

    DEBUG = False
    TESTING = False
    DB_CONFIG = get_database_config()
    DB_SERVER='localhost'

class development_config(flask_config_template):

    DEBUG = True
    TESTING = True
    DB_SERVER='localhost'

    # EDGE_DBCONFIG = get_parameters('edge')
    # DEV_DBCONFIG = get_parameters('dev')
