import boto3



class RekognitionLivenessAPI:

    def __init__(self):
        session = boto3.Session(profile_name='default')
        self.client = session.client(
            'rekognition',
            region_name="ap-south-1",
            aws_access_key_id="AKIA5CBDQ3LI7WLM6EEJ",
            aws_secret_access_key="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"
        )

    def create_face_liveness_session(self):
        response = self.client.create_face_liveness_session()
        return response.get("SessionId")

    def get_face_liveness_session_results(self, session_id):
        response = self.client.get_face_liveness_session_results(SessionId=session_id)
        return {
            "confidence": response.get("Confidence"),
            "status": response.get("Status"),
            "raw_response": response
        }

    def compare_faces(self, source_file_byte, target_file_path, threshold=85):
        try:    
            with open(target_file_path, 'rb') as target_file:
                response = self.client.compare_faces(
                    SimilarityThreshold=80,
                    SourceImage={'Bytes': target_file.read()},
                    TargetImage={'Bytes': source_file_byte}
                )
                face_matches = response.get('FaceMatches', [])
            if face_matches:
                similarities = [match.get('Similarity', 0) for match in face_matches]
                average_similarity = sum(similarities) / len(similarities)
                decision = average_similarity >= threshold
                return {
                    "decision": decision,
                    "average_similarity": round(average_similarity, 2),
                    "matches_count": len(face_matches),
                }
            else:
                return {
                    "decision": False,
                    "average_similarity": 0,
                    "matches_count": 0,
                }
        except FileNotFoundError as e:
            return {"error": f"File not found: {e.filename}"}
        except (BotoCoreError, ClientError) as e:
            return {"error": f"AWS Rekognition error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
            return len(response['FaceMatches'])