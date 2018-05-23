from jsonpath_rw import parse
from rdflib import URIRef, Literal
from urllib import quote

from odmtp.modules.mapper import Mapper


class MapperlinkedinXr2rml(Mapper):

    def result_set_2_rdf(self, result_set, reduced_mapping, fragment):
        for s, p, o in reduced_mapping.mapping:
            subject = s
            obj = o
            # pour chaque sujet, URI ex "http/....../{variable}"
            splited_subject = subject.split('{')
            # le 0 me fait recupere le http ../
            subject_prefix = splited_subject[0]
            # le 1 est $.variable} donc on lui enleve l'accolade fermante afin de pourvoir l utiliser dans le fichier json il correspond a des positions
            subject_jsonpath = parse(splited_subject[1].split('}')[0])
            # regarde si a cette position on retrouve l element subject_path
            # on met dans subject_values tte les valurs qui corresponde a subject_jsonpath trouve dans le fichier json il y'aura qu un seule element
            # on en recupere plusisuers ? pourquoi les mettre dans une liste si on n'utilise que le premiers ?????
            subject_values = [match.value for match in subject_jsonpath.find(result_set)]
            # si l objet est une variable
            if '$.' in obj:
                object_jsonpath = parse(obj.split('{')[0].split('}')[0])
                print object_jsonpath
                object_values = [match.value for match in object_jsonpath.find(result_set)]
                print object_values
                for object_value in object_values:
                    # pour chaque valeur de object_values ajouter au fragment le sujet  predicat et l objet je cree une URI
                    # pourquoi on prend que le premier ?
                    fragment.add_data_triple(URIRef("%s%s" % (subject_prefix, quote(subject_values[0]))), p, Literal(object_value))
            else:
                # si j ai qu une seule valeur de objet je met que celle-ci
                fragment.add_data_triple(URIRef("%s%s" % (subject_prefix,  quote(subject_values[0]))), p, obj)
