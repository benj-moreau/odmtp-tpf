from jsonpath_rw import parse
from rdflib import URIRef, Literal

from odmtp.modules.mapper import Mapper


class MapperGithubXr2rml(Mapper):

    def result_set_2_rdf(self, result_set, reduced_mapping, fragment):
        for repo in result_set:
            for s, p, o in reduced_mapping.mapping:
                subject = s
                obj = o
                splited_subject = subject.split('{')
                subject_prefix = splited_subject[0]
                subject_jsonpath = parse(splited_subject[1].split('}')[0])
                subject_values = [match.value for match in subject_jsonpath.find(repo)]
                if '$.' in obj:
                    object_jsonpath = parse(obj.split('{')[0].split('}')[0])
                    object_values = [match.value for match in object_jsonpath.find(repo)]
                    for object_value in object_values:
                        fragment.add_data_triple(URIRef("%s%s" % (subject_prefix, subject_values[0])), p, Literal(object_value))
                else:
                    fragment.add_data_triple(URIRef("%s%s" % (subject_prefix, subject_values[0])), p, obj)
