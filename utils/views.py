from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404

#create global transactional class mixin

class TransactionalViewMixin(object):
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(TransactionalViewMixin, self).dispatch(*args, **kwargs)