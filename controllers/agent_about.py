from fastapi import APIRouter,Body,File,UploadFile
from fastapi.exceptions import HTTPException
from fastapi.params import Query
from fastapi.responses import StreamingResponse
from minio import S3Error
from agents.agent_initializer import  cv_agent
from config.bucket import bucket_client
from io import BytesIO

router=APIRouter()


@router.post("/")
def about_user(question: str = Body(..., embed=True),filename: str = Body(..., embed=True)):
    messages={"messages":[{
        "role":"user",
        "content": f"give me information about this : {question}? and the cv is in the file named {filename}"
    }]}

    response = cv_agent.invoke(messages)

    result=response.get('structured_response',None)
    return result
    
@router.get("/cv")
async def get_file(file_name: str = Query(...)):
    try:
        BUCKET_NAME="s3-cv"
        client=bucket_client()

        # Get the object from MinIO
        response = client.get_object(BUCKET_NAME, file_name)

        # Stream the file content to the client
        return StreamingResponse(response, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename={file_name}"
        })

    except S3Error as err:
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    
@router.put("/cv")
async def update_file(file_name: str = Query(...), cv_file:UploadFile=File):
    try:
        BUCKET_NAME="s3-cv"
        client=bucket_client()
        contents =  await cv_file.read()  # read file content

        client.put_object(
            BUCKET_NAME,
            file_name,
            BytesIO(contents),
            length=len(contents),
            content_type=cv_file.content_type
            )
        
        
        return {"message": f"{file_name} updated in MinIO",
                }
        
    except S3Error as err:
        raise HTTPException(status_code=500, detail=f"Update File {err}")
    

@router.post("/cv")
async def upload_file(cv_file:UploadFile=File(...)):
    try:
        BUCKET_NAME="s3-cv"
        client=bucket_client()
        contents =  await cv_file.read()  # read file content

        client.put_object(
            BUCKET_NAME,
            cv_file.filename,
            BytesIO(contents),
            length=len(contents),
            content_type=cv_file.content_type
            )
        
        
        return {"message": f"{cv_file.filename} uploaded to MinIO",
                }
        
    except S3Error as err:
        raise HTTPException(status_code=500, detail=f"Uplaod File {err}")