import cloudinary
import cloudinary.uploader
import cloudinary.api

def upload_image_to_cloudinary(image_path, cloud_name, api_key, api_secret):
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    
    response = cloudinary.uploader.upload(image_path)
    if response:
        return response['secure_url']
    else:
        print("Error: Failed to upload image to Cloudinary.")
        return None