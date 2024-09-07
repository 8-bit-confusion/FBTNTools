from gallery_scrape import Gallery
from chat_utils import Prompts, ChatClient

if __name__ == "__main__":
    client = ChatClient()
    iunsct_gallery = Gallery.from_csv("data/iunsct.csv")

    for base64_image in iunsct_gallery.values():
        response = client.response(
            Prompts.image_prompt(
                "please list the clothing items in this image. \
                be detailed in your description of garment styles, fabrics, textures, accessories, etc.",
                base64_image
            )
        )

        print(response.choices[0].message.content)
