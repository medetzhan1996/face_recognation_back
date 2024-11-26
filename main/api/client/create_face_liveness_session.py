from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.service import RekognitionAPI



class CreateFaceLivenessSessionView(APIView):

    def post(self, request):
        rekognition = RekognitionAPI()
        try:
            session_id = rekognition.create_face_liveness_session()
            return Response({"session_id": session_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)