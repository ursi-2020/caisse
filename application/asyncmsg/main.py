import sys
import os
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apipkg import queue_manager as queue

from application.djangoapp.models import *


def main():
    print("Liste des ventes:")
    for v in Vente.objects.all():
        print("ID: " + str(v.id) + "\tArticle: " + v.article.nom + "\tDate: " + str(v.date))

def callback(ch, method, properties, body):
    print(" [x] Received from queue %r" % body)

if __name__ == '__main__':
    main()
    queue.receive('AppB', callback)