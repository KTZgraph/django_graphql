import graphene
from graphene_django.types import DjangoObjectType
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


class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String()) #aceptujemy parametr id typu Integer, tytul String

    all_directors = graphene.List(DirectorType)

    def resolve_all_movies(self, info, **kwargs): # dodatkowe argumenty na pozniej
        return Movie.objects.all()

    def resolve_all_directors(self, info, **kwargs): # dodatkowe argumenty na pozniej
        return Director.objects.all()

    def resolve_movie(self, info, **kwargs): # dodatkowe argumenty na pozniej można id, title zamiast **kwargs
        movie_id = kwargs.get('id')
        title = kwargs.get('title')

        if movie_id is not None:
            return Movie.objects.get(pk=movie_id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None


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
    create_movie = MovieCreateMutation.Field() #dla jednego pecyficznego rekordu
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()
