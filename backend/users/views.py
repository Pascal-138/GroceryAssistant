# from django.shortcuts import get_object_or_404
# from djoser.views import UserViewSet

# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
# from rest_framework.response import Response

# from api.pagination import CustomPagination
# from api.serializers import FollowSerializer
# from users.models import Follow, User

# # from users.serializers import FollowSerializer
# # from rest_framework.pagination import PageNumberPagination


# class FollowViewSet(UserViewSet):
# # class FollowViewSet(viewsets.ModelViewSet):

#     permission_classes = (IsAuthenticated,)
#     # queryset = Follow.objects.all()
#     queryset = User.objects.all()
#     pagination_class = CustomPagination
#     serializer_class = FollowSerializer

#     @action(
#         methods=['GET'],
#         detail=False,
#         serializer_class = FollowSerializer
# )

#     def subscriptions(self, request):
#         user = request.user
#         # subscriptions = Follow.objects.filter(user=user)
#         # serializer = FollowSerializer(subscriptions,
#         #                               many=True,
#         #                               context={'request':request})
        
#         queryset = Follow.objects.filter(user=user)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)



#     @action(
#         detail=True,
#         methods=['POST', 'DELETE'],
#         #permission_classes=[IsAuthenticated],
#         )
#     def subscribe(self, request, id=None):
#         author = get_object_or_404(User, id=id)
#         user = request.user

#         if request.method == 'POST':
#             if Follow.objects.filter(user=user, author=author).exists():
#                 return Response(
#                     {'errors': 'Вы уже подписаны'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             if user == author:
#                 return Response(
#                     {'errors': 'Нельзя подписаться на самого себя'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             follow = Follow.objects.create(user=user, author=author)
#             serializer = FollowSerializer(follow, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         elif request.method == 'DELETE':
#             if not Follow.objects.filter(user=user, author=author).exists():
#                 return Response(
#                     {'errors': 'Вы не подписаны'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             follow = Follow.objects.get(user=user, author=author)
#             follow.delete()
#             return Response(
#                 {'message': 'Подписка удалена'},
#                 status=status.HTTP_204_NO_CONTENT
#             )





    




    