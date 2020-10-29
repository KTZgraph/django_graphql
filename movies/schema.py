import graphene
import movies.api.schema


class Query(movies.api.schema.Query, graphene.ObjectType): #dodawac jako arg z innych apek
    pass


class Mutation(movies.api.schema.Mutation, graphene.ObjectType): #dodawac jako arg z innych apek
    pass

#dla frontu
"""
python manage.py graphql_schema
Successfully dumped GraphQL schema to schema.json
robi się nowy plik ma np "name": "allMovies",
będize trzeb aciągle generowć nowe schema.json po zmianach w backendzie
Używać jak się nie ma default w settings.py
python manage.py graphql_schema --schema paramtrodomojejchemca

"""


schema = graphene.Schema(query=Query, mutation=Mutation)