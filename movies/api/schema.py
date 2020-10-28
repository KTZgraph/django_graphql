import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id #do mutacji relay
from .models import Director, Movie


class MovieType(DjangoObjectType): # podobnie do serializer
    class Meta:
        model = Movie

    #synamicznie dodane do modelu niekoniecznei z bazy
    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New movie"


class DirectorType(DjangoObjectType): # podobnie do serializer
    class Meta:
        model = Director


# just for relay implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        #dodanie filtró dla pól, custom way to get datd
        #Filtr icontains - incase sensitive
        filter_fields = {
            'title': ["exact", "icontains", "istartswith"],
            'year': ["exact",]
        }
        interfaces = (relay.Node, ) #this django object witl be relay



class Query(graphene.ObjectType):
    # all_movies = graphene.List(MovieType)
    all_movies =DjangoFilterConnectionField(MovieNode)
    #movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String()) #aceptujemy parametr id typu Integer, tytul String
    movie = relay.Node.Field(MovieNode)

    all_directors = graphene.List(DirectorType)

    """
    @login_required
    def resolve_all_movies(self, info, **kwargs): # dodatkowe argumenty na pozniej
        # 1. roziwazanie info.context
        # user = info.context.user
        # if not user.is_authenticated:
        #     raise Exception("Auth credentials were not provided")
        return Movie.objects.all()
    """

    def resolve_all_directors(self, info, **kwargs): # dodatkowe argumenty na pozniej
        return Director.objects.all()

    """
        # zastapoione przez movie = relay.Node.Field(MovieNode)
    def resolve_movie(self, info, **kwargs): # dodatkowe argumenty na pozniej można id, title zamiast **kwargs
        movie_id = kwargs.get('id')
        title = kwargs.get('title')

        if movie_id is not None:
            return Movie.objects.get(pk=movie_id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None
    """

class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year): #zamiast **kwargs
        #nasza logika
        movie = Movie.objects.create(title=title, year=year)
        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year
        movie.save()

        return MovieUpdateMutation(movie=movie)


class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title, year):
        #try catch dopisać
        movie = Movie.objects.get(pk=id)

        return MovieCreateMutation(movie=movie)


#relay implementation
class MovieUpdateMutationRelay(relay.ClientIDMutation):
    """
    :example:
    mutation MutateRelay {
          updateMovieRelay(input: {id: "TW92aWVOb2RlOjE=", title:"Test relay mutation"})
          {
            movie{
              id
              title
              year
            }
          }
        }
    """
    class Input:
        title = graphene.String()
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    @classmethod #relay - trzbea nadpisac roznice
    def mutate_and_get_payload(cls, root,  info, id, title):
        #try catch dopisać
        #id dla relay jest inne - jest to long string characters
        movie = Movie.objects.get(pk=from_global_id(id)[1]) #jedyna różnica w wcyiagnaiu id z nodów relay

        if title is not None:
            movie.title = title
        movie.save()

        return MovieUpdateMutationRelay(movie=movie)


class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()

        return MovieUpdateMutation(movie=None)#już nie ma movie bo usunięte


class Mutation:
    #głowna klasa mutacji
    token_auth = graphql_jwt.ObtainJSONWebToken.Field() #token z loginu i hasła użytkownika
    verify_token = graphql_jwt.Verify.Field()

    create_movie = MovieCreateMutation.Field() #dla jednego pecyficznego rekordu
    update_movie = MovieUpdateMutation.Field()
    update_movie_relay = MovieUpdateMutationRelay.Field() #dal relay
    delete_movie = MovieDeleteMutation.Field()
