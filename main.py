import sys

sys.path.insert(0, './chart')
sys.path.insert(0, './util')

from chart import ChartAnalyzer
from config_reader import read_config
from image_uploader import upload_image_to_cloudinary

config = read_config('app.config')
api_key = config['api_key']
cloud_name = config['cloudinary_cloud_name']
cloudinary_api_key = config['cloudinary_api_key']
cloudinary_api_secret = config['cloudinary_api_secret']
image_path = 'resources/WELCORP_2025-02-07_23-49-30_62f5c.png'
image_url = upload_image_to_cloudinary(image_path, cloud_name, cloudinary_api_key, cloudinary_api_secret)

if image_url:
    print(f'Image URL: {image_url}')

    if __name__ == "__main__":
        analyzer = ChartAnalyzer(api_key)
        analyzer.analyze_image(image_url)
else:
    print("Failed to upload image to Imgur.")