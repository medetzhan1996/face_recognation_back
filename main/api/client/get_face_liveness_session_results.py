from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.recognation_liveness_service import RekognitionLivenessAPI
from main.models import Client
from main.recognaton_service import search_users_by_image


class GetFaceLivenessSessionResultsView(APIView):

    def get(self, request, session_id):
        rekognition = RekognitionLivenessAPI()
        results = rekognition.get_face_liveness_session_results(session_id)
        confidence = results.get("confidence")
        rec_status = results.get("status")
        source_file_byte = results["raw_response"]["ReferenceImage"]["Bytes"]
        result = {
            "confidence": confidence,
            "status": rec_status,
            "is_match": False,
            "name": None
        }
        data = search_users_by_image("kgdemo_collection", source_file_byte)
        if 'Matches' in data and len(data['Matches']) > 0:
            first_match = data['Matches'][0]
            user_id = first_match.get('UserId')
            similarity = first_match.get('Similarity')
            try:
                client = Client.objects.get(id=user_id)
                result['is_match'] = True
                result['similarity'] = similarity
                result["name"] = client.name
            except Client.DoesNotExist:
                pass
        return Response(
            {
                "confidence": confidence,
                "status": rec_status,
                "result": result
            },
            status=status.HTTP_200_OK
        )
