from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import ChallengeSerializer, ChallengeImageSerializer
from .models import Challenge


class ChallengeView(APIView):
    def get(self, request):
        '''
        챌린지 보기
        '''
        challenge = Challenge.objects.all()
        serializer = ChallengeSerializer(challenge, many=True)
        return Response(serializer.data)


class ChallengeWriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        '''
        챌린지 쓰기
        '''
        serializer = ChallengeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChallengeDatailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def put(self, request, challenge_id):
        '''
        챌린지 수정하기
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.user == challenge.user:
            serializer = ChallengeSerializer(challenge, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("챌린지 수정 권한은 챌린지를 만든 사람에게 있습니다.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, challenge_id):
        '''
        챌린지 삭제하기 : 챌린지를 시작한 사람이 없을 때
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.user == challenge.user:
            
            return Response({"message":"delete!"})
    

# class ChallengeBookmarkView(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def post(self, request, challenge_id):
#         challenge = get_object_or_404(Challenge, id=challenge_id)
#         if request.user in challenge.likes.all():
#             challenge.likes.remove(request.user)
#             return Response("북마크를 해제하였습니다.", status=status.HTTP_204_NO_CONTENT)
#         else:
#             challenge.likes.add(request.user)
#             return Response("챌린지를 북마크에 저장하였습니다.", status=status.HTTP_200_OK)


# class ChallengeMemberView(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get(self, request):
#         challenge = Challenge.objects.all()
#         serializer = ChallengeSerializer(challenge, many=True)
#         return Response(serializer.data)
#     challenge = get_object_or_404(Challenge, id=challenge_id)   

#     def post(self, request, challenge_id):
#         challenge = get_object_or_404(Challenge, id=challenge_id)
#         if request.user in challenge.likes.all():
#             challenge.likes.remove(request.user)
#             return Response("북마크를 해제하였습니다.", status=status.HTTP_204_NO_CONTENT)
#         else:
#             challenge.likes.add(request.user)
#             return Response("챌린지를 북마크에 저장하였습니다.", status=status.HTTP_200_OK)



class CommentView(APIView):
    def get(self, request):
        return Response({"message":"get!"})