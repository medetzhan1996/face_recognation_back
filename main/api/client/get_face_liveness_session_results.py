from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.service import RekognitionAPI
from main.models import Client


class GetFaceLivenessSessionResultsView(APIView):

    def get(self, request, session_id):
        rekognition = RekognitionAPI()
        id_document = request.GET.get("id_document")
        client = Client.objects.filter(id_document=id_document).first()

        results = rekognition.get_face_liveness_session_results(session_id)
        confidence = results.get("confidence")
        rec_status = results.get("status")
        source_file_byte = results["raw_response"]["ReferenceImage"]["Bytes"]

        compare_face_result = rekognition.compare_faces(
            source_file_byte=source_file_byte,
            target_file_path=client.photo.path
        )
        return Response(
            {
                "confidence": confidence,
                "status": rec_status,
                "compare_face_result": compare_face_result
            },
            status=status.HTTP_200_OK
        )