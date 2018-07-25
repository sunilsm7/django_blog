from django.conf import settings
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import (
    analyzer,
    Boolean,
    Date,
    DocType,
    Integer,
    Keyword,
    Search,
    Text,
)

from elasticsearch_dsl import analyzer, tokenizer
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from . import models
# Create a connection to ElasticSearch
# connections.create_connection()

ELASTIC_HOSTS = getattr(settings, "ELASTIC_HOSTS",)
ELASTIC_AUTH_USERNAME = getattr(settings, "ELASTIC_AUTH_USERNAME")
ELASTIC_AUTH_PASSWORD = getattr(settings, "ELASTIC_AUTH_PASSWORD")
ELASTIC_PORT = getattr(settings, "ELASTIC_PORT")


connections.create_connection(
    hosts=[ELASTIC_HOSTS],
    http_auth=(ELASTIC_AUTH_USERNAME, ELASTIC_AUTH_PASSWORD),
    scheme="https",
    port=9243
)


my_analyzer = analyzer(
    'my_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
    filter=['lowercase']
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


# ElasticSearch "model" mapping out what fields to index
class PostIndex(DocType):
    user = Text()
    title = Text(analyzer=my_analyzer, fields={'raw': Keyword()})
    slug = Text()
    content = Text(analyzer=html_strip)
    draft = Boolean()
    height_field = Integer()
    width_field = Integer()
    approved = Boolean()
    publish = Boolean()
    read_time = Integer()
    views = Integer()
    updated = Date()
    timestamp = Date()

    class Index:
        name = 'posts'


# Bulk indexing function, run in shell
def bulk_indexing(index="posts"):
    PostIndex.init()
    es = Elasticsearch()
    try:
        bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))
    except Exception:
        pass


def search(q):
    s = Search(index="posts").query("multi_match", query=q, fields=['title', 'content'])
    response = s.execute()
    return response


def search_all():
    s = Search(index="posts").query('match_all')
    response = s.execute()
    return response
