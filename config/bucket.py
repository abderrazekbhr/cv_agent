from minio import Minio
from minio.error import S3Error

from dotenv import load_dotenv
import os

load_dotenv()




# --- CONFIGURATION --- #
MINIO_ENDPOINT = "localhost:9000"         # Adresse de ton MinIO
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")           # MINIO_ROOT_USER
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")           # MINIO_ROOT_PASSWORD
                # Nom du bucket à créer

def bucket_client(bucket_name :str= "s3-cv"):
    try:
        client_bucket = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False  # mettre True si tu utilises HTTPS
        )

        if not client_bucket.bucket_exists(bucket_name):
            client_bucket.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' créé.")
        else:
            print(f"Bucket '{bucket_name}' existe déjà.")

        return client_bucket
        
    except S3Error as err:
        raise err