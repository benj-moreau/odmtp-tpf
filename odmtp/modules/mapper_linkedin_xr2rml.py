from jsonpath_rw import parse
from rdflib import URIRef, Literal
from urllib import quote

from odmtp.modules.mapper import Mapper


class MapperlinkedinXr2rml(Mapper):

    def result_set_2_rdf(self, result_set, reduced_mapping, fragment):
        for s, p, o in reduced_mapping.mapping:
            subject = s
            obj = o
            splited_subject = subject.split('{')
            subject_prefix = splited_subject[0]
            subject_jsonpath = parse(splited_subject[1].split('}')[0])
            subject_values = [match.value for match in subject_jsonpath.find(result_set)]
            if '$.' in obj:
                if 'http' in obj:
                    splited_object = obj.split('{')
                    object_prefix = splited_object[0]
                    object_jsonpath = parse(splited_object[1].split('}')[0])
                    object_values = [match.value for match in object_jsonpath.find(result_set)]
                    for object_value in object_values:
                        fragment.add_data_triple(URIRef("%s%s" % (subject_prefix, quote(subject_values[0].encode('utf8')))), p, URIRef("%s%s" % (object_prefix, quote(object_values[0].encode('utf8')))))
                else:
                    object_jsonpath = parse(obj.split('{')[0].split('}')[0])
                    object_values = [match.value for match in object_jsonpath.find(result_set)]
                    for object_value in object_values:
                        fragment.add_data_triple(URIRef("%s%s" % (subject_prefix, quote(subject_values[0].encode('utf8')))), p, Literal(object_value))
            else:
                fragment.add_data_triple(URIRef("%s%s" % (subject_prefix,  quote(subject_values[0].encode('utf8')))), p, obj)
