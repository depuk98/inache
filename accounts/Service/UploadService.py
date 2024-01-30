from django.conf import settings
from django.db import transaction
from django.utils import timezone
import pathlib
from uuid import uuid4
from django.urls import reverse
from django.conf import settings
from accounts.models import AwarenessProgram, BaseUserModel, Case, UploadedFile_S3, User_Profilepic, UserRoleFactory
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from rest_framework import  status

def s3_get_client():
    print(settings.AWS_S3_ACCESS_KEY_ID,settings.AWS_S3_SECRET_ACCESS_KEY,settings.AWS_S3_REGION_NAME)
    return boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        config= Config(signature_version='s3v4')
    )

def s3_generate_presigned_get(*, file_name: str):
    s3_client = s3_get_client()
    try:
        response = s3_client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': settings.AWS_S3_BUCKET_NAME, 'Key': file_name},
                                                     ExpiresIn=3600,
                                                     HttpMethod='GET')
    except ClientError as e:
        logging.error(e)
        return None
    return response


def s3_generate_presigned_post(*, file_path: str):
    s3_client = s3_get_client()
    try:
        response = s3_client.generate_presigned_url(ClientMethod='put_object',Params={'Bucket': settings.AWS_S3_BUCKET_NAME, 'Key': file_path},
                                                     ExpiresIn=3600,
                                                     HttpMethod='PUT')
    except ClientError as e:
        logging.error(e)
        return None
    return response

def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix
    return f"{uuid4().hex}{extension}"

class FileDirectUploadService:
    @transaction.atomic

    def start(self, *, file_name: str, file_type: str, model: str, id:str, company_fk:str): #file_name and file_type parameters should be passed as keyword arguments(* indicates that)
        extension = file_name.split(".")[-1]
        if extension!=file_type:
            return ({"errorMessage":"File type are not same"},status.HTTP_400_BAD_REQUEST)
        file = UploadedFile_S3(
            file_type=file_type,
            s3_file_path = f"{company_fk}/{model}/{id}/{file_generate_name(file_name)}"
        )
        file.full_clean() 
        
        print(file.s3_file_path)
        file.save()
        presigned_data = {}
        settings.FILE_UPLOAD_STORAGE = "s3"
        presigned_data = s3_generate_presigned_post(
            file_path=file.s3_file_path
        )
        settings.FILE_UPLOAD_STORAGE = "local"
        return {"id": file.id, "url": presigned_data}, status.HTTP_200_OK

    @transaction.atomic
    def finish(self, *, file: UploadedFile_S3, userRole: UserRoleFactory,model:str,model_id:int):
        
        assignFiletoModel(model, model_id, file)
        file.upload_finished_at = timezone.now()
        file.uploaded_by=userRole
        file.full_clean()
        file.save()
        return file

    def get(self, *, file: UploadedFile_S3) -> UploadedFile_S3:
        print(file.s3_file_path,"dasdas")
        get_path = s3_generate_presigned_get(file_name = str(file.s3_file_path))
        # print(file.id ,"SAdasdas")
        return get_path
    

def assignFiletoModel(model, id, file):
    if model == "case":
            case=Case.objects.get(id=id)
            case.File.add(file)
            case.save()
    if model =="awareness_program":
        awareness_program=AwarenessProgram.objects.get(id=id)
        awareness_program.Files.add(file)
        awareness_program.save()
    if model =="profile_picture":
        try:
            profile_pic=User_Profilepic.objects.get(user_id=id)
        except User_Profilepic.DoesNotExist:
            profile_pic=User_Profilepic.objects.create(user_id=id)
        profile_pic.profile_picture=file
        profile_pic.save()
    