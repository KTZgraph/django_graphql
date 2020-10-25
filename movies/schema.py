import graphene
import movies.api.schema


class Query(movies.api.schema.Query, graphene.ObjectType): #dodawac jako arg z innych apek
    pass

schema = graphene.Schema(query=Query)