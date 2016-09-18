from django.conf.urls import *
from ele.view import hello
from ele.testdb import testdb

urlpatterns = patterns("",
        ('^hello/$', hello),
        ('^testdb/$', testdb),
)