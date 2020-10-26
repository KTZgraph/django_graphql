from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    # url dla graphql
    # path('graphql/', GraphQLView.as_view(schema)) jak bez general schema w settings
    path('graphql/', GraphQLView.as_view(graphiql=True))
]
