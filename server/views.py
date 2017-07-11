from rdflib import URIRef, Literal

from django.http.response import HttpResponse
from django.core.validators import URLValidator
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError


@require_http_methods(['GET'])
def tpf_server(request):
    page = int(request.GET.get('page', '1'))
    subject = URIRef(request.GET.get('subject')) if request.GET.get('subject') else None
    predicate = URIRef(request.GET.get('predicate')) if request.GET.get('predicate') else None
    obj = URIRef(request.GET.get('object')) if request.GET.get('object') else None
    if obj is not None:
        validator = URLValidator()
        try:
            validator(obj)
            obj = URIRef(obj)
        except ValidationError:
            obj = string_to_literal(obj, validator)

    response = HttpResponse(
        # returned_graph.serialize(format="trig", encoding="utf-8"),
        "page:%s subject:%s predicate:%s object:%s" % (page, subject, predicate, obj),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    return response


def string_to_literal(string, urlvalidator):
    splited_literal = string.split('"')
    value = splited_literal[1]
    datatype = splited_literal[2].split('^^')[1] if splited_literal[2] else None
    try:
        urlvalidator(datatype)
        datatype = URIRef(datatype)
    except ValidationError:
        datatype = None
    return Literal(value, datatype=datatype)
