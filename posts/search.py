from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Document, Date, Integer, Boolean, Text, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

# Create a connection to ElasticSearch
connections.create_connection()


# ElasticSearch "model" mapping out what fields to index
class PostIndex(DocType):
    user = Text()
    title = Text()
    slug = Text()
    content = Text()
    draft = Boolean()
    image = Text()
    height_field = Integer()
    width_field = Integer()
    approved = Boolean()
    publish = Boolean()
    read_time = Integer()
    views = Integer()
    updated = Date()
    timestamp = Date()

    class Meta:
        index = 'post-index'


# Bulk indexing function, run in shell
def bulk_indexing():
    PostIndex.init()
    es = ElasticSearch()
    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))


def search(title):
    s = Search().filter('term', tilte=tilte)
    response = s.execute()
    return response
