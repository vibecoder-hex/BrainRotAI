import boto3, base64


class ImageStorage:
    def __init__(self,
                 AWS_ENDPOINT_URL,
                 AWS_ACCESS_KEY_ID,
                 AWS_SECRET_ACCESS_KEY,
                 AWS_BUCKET_NAME,
                 IMAGE_EXT
                ):
        self.aws_endpoint_url = AWS_ENDPOINT_URL
        self.aws_access_key_id, self.aws_secret_access_key = AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        self.aws_bucket_name = AWS_BUCKET_NAME
        self.image_ext = IMAGE_EXT

        self.s3 = boto3.client(
            's3',
            endpoint_url = self.aws_endpoint_url,
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            config=boto3.session.Config(signature_version='s3v4')
        )
    
    def put_image_object(self, image_base64_code, image_filepath):
        image_binary = base64.b64decode(image_base64_code)
        self.s3.put_object(Bucket=self.aws_bucket_name,
                           Key=image_filepath,
                           Body=image_binary,
                           ContentType=f'image/png')
    
    def get_image_object(self, image_key):
        return self.s3.generate_presigned_url('get_object', Params={'Bucket': self.aws_bucket_name, "Key": image_key})
    
    def delete_image_object(self, image_key):
        self.s3.delete_object(Bucket=self.aws_bucket_name, Key=image_key)
