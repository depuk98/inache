from accounts.Service.UploadService import FileDirectUploadService
from accounts.Utils.userRoleParser import parser
from accounts.models import AwarenessProgram, Case, UploadedFile_S3, User_Profilepic
from accounts.serializers import FinishInputSerializer, GetInputSerializer, StartInputSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request


class FileDirectUploadApi(APIView):
    
            
    def post(self, request:Request)->Response:
        serializer = StartInputSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        service = FileDirectUploadService()
        presigned_data,status = service.start(**serializer.validated_data)
        return Response(data=presigned_data,status=status)

    def patch(self, request:Request)->Response:
        
        serializer = FinishInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            file=UploadedFile_S3.objects.get(id=request.data.get("file_id"))
        except UploadedFile_S3.DoesNotExist:
            return Response({"errorMessage": "File not found"}, status=404)
        if UploadedFile_S3.objects.get(id=request.data.get("file_id")).upload_finished_at is not None:
            return Response({"errorMessage": "File already uploaded"}, status=400)
        service = FileDirectUploadService()
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        service.finish(file=file, userRole=userRole,model=request.data.get("model"),model_id=request.data.get("model_id"))
        return Response({"id": file.id},status=200)

    def get(self, request:Request)->Response:
        
        serializer = GetInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        file_ids_str = request.query_params.get('file_ids')
        file_ids = [int(file_id) for file_id in file_ids_str.split(',')]
        print(len(file_ids))
        if len(file_ids) > 10:
            return Response({"errorMessage": "Maximum 10 file ids can be provided"}, status=400)
        response = {}
        for file_id in file_ids:
            try:
                file = UploadedFile_S3.objects.get(id=file_id)
            except UploadedFile_S3.DoesNotExist:
                response[file_id] = {"errorMessage": "File not found for ID " + str(file_id)}
                continue
            # print(file.upload_finished_at)
            # if file.upload_finished_at is None:
            #         response[file_id] = {"errorMessage": "File not uploaded for ID " + str(file_id)}
            if file.uploaded_by is None:
                response[file_id] = {"errorMessage": "File is not uploaded for this ID " + str(file_id)}
                continue
            if file.uploaded_by.user_fk.company_fk.id != request.user.company_fk.id:
                response[file_id] = {"errorMessage": "User belongs to a different company"}
                continue
            service = FileDirectUploadService()
            presigned_url = service.get(file=file)
            filetype = file.file_type
            print(filetype)
            response[file_id] = {
            "presigned_url": presigned_url,
            "file_type": filetype
            }

        return Response(response)

    def delete(self, request:Request)->Response:
        try:
            file=UploadedFile_S3.objects.get(id=request.data.get("file_id"))
        except UploadedFile_S3.DoesNotExist:
            return Response({"errorMessage": "File not found"}, status=404)
        if request.data.get('model')=='case': 
            case=Case.objects.get(id=request.data.get('model_id'))
            case.File.remove(file)
            case.save()
        elif request.data.get('model')=='awareness_program':
            awarenesspgm=AwarenessProgram.objects.get(id=request.data.get('model_id'))
            awarenesspgm.Files.remove(file)
            awarenesspgm.save()
        elif request.data.get('model')=='profile_picture':
            profile_picture=User_Profilepic.objects.get(id=request.data.get('model_id'))
            profile_picture.user=None
            profile_picture.save()
    
        return Response({"message":"File was deleted"},status=200)
            