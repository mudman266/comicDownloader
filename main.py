import requests
from bs4 import BeautifulSoup
from img2pdf import convert


def save_images_as_pdf(url, output_pdf):
    # Fetch the HTML content of the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all images with the class "lazy"
        lazy_images = soup.find_all('img', class_='img-responsive')

        if lazy_images:
            # Create a list to store image URLs
            image_urls = []

            # Extract image URLs
            for img in lazy_images:
                src = img.get('data-src') or img.get('src')
                if src:
                    image_urls.append(src.strip())

            # Download images and save them to a list
            images = [requests.get(url).content for url in image_urls]

            # Convert images to PDF
            with open(output_pdf, 'wb') as pdf_file:
                pdf_file.write(convert(images))

            print(f"PDF saved successfully: {output_pdf}")
        else:
            print("No images with class 'img-responsive' found on the website.")
    else:
        print(f"Failed to fetch the website. Status Code: {response.status_code}")


# Example usage
website_url = 'https://readcomicsonline.ru/comic/blue-beetle-2023/6'
output_pdf_file = 'lazy_images.pdf'
save_images_as_pdf(website_url, output_pdf_file)
