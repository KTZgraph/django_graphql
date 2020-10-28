from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    # url dla graphql
    # path('graphql/', GraphQLView.as_view(schema)) jak bez general schema w settings
    path('graphql/', jwt_cookie(GraphQLView.as_view(graphiql=True))) #opakowanie ciastkiem jwt wszystkie te urle
]
