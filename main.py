import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from img2pdf import convert
from statistics import mode


def get_image_dimensions(url):
    # Fetch image content and get dimensions
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img.size  # Returns (width, height)
    return None


def save_images_as_pdf(url, output_pdf):
    # Fetch the HTML content of the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all images
        all_images = soup.find_all('img')

        if all_images:
            # Create lists to store image URLs and dimensions
            image_urls = []
            image_dimensions = []

            # Extract image URLs and dimensions
            for img in all_images:
                src = img.get('data-src') or img.get('src')
                if src:
                    dimensions = get_image_dimensions(src.strip())
                    if dimensions:
                        image_urls.append(src.strip())
                        image_dimensions.append(dimensions)
                        # print(f'Adding dimensions: {dimensions}')

            if not image_urls:
                print("No images found on the website.")
                return

            # Calculate the mode dimensions of all images
            mode_width = mode(dim[0] for dim in image_dimensions)
            mode_height = mode(dim[1] for dim in image_dimensions)

            print(f"Mode image dimensions: {mode_width} x {mode_height}")

            # Make a list of image urls that match the mode dimensions
            filtered_images = []
            for i in range(0, len(image_dimensions)):
                # width
                width_diff = image_dimensions[i][0] - mode_width
                if width_diff < 5 and width_diff > -5:
                    # height
                    height_diff = image_dimensions[i][1] - mode_height
                    if height_diff < 5 and height_diff > -5:
                        filtered_images.append(image_urls[i])

            # Download images and save them to a list
            print(f'Converting images from the following urls:')
            for report_url in filtered_images:
                print(report_url)
            images = [requests.get(url).content for url in filtered_images]

            # Convert images to PDF
            try:
                with open(output_pdf, 'wb') as pdf_file:
                    pdf_file.write(convert(images))
            except:
                print(f'Error occurred trying to convert images to pdf: {output_pdf}.')

            print(f"PDF saved successfully: {output_pdf}")
        else:
            print("No images found on the website.")
    else:
        print(f"Failed to fetch the website. Status Code: {response.status_code}")


# Example usage
website_url = 'https://readcomicsonline.ru/comic/birds-of-prey-2023/7'
output_pdf_file = 'mode_dimensions_images.pdf'
save_images_as_pdf(website_url, output_pdf_file)