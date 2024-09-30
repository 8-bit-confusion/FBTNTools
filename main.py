from gallery_scrape import Gallery
from chat_utils import Prompts, ChatClient

if __name__ == "__main__":
    client = ChatClient()
    # https://in.pinterest.com/iunsct/coquette-outfits/
    #iunsct_gallery = Gallery.from_csv("data/iunsct.csv")   


    gallery = Gallery()

    urls = ["https://i.pinimg.com/originals/9e/62/61/9e626127c8161e999d6b03dd67090e85.jpg"]   

    for url in urls:
        gallery.add_from_image_link(url)

    for base64_image in gallery.values():
        response = client.response(
            Prompts.image_prompt(
                "Given the following image(s), provide objective descriptors, \
                each separated by commas, that describe solely the outfit. \
                Do not describe the person’s body type, skin color, or any other \
                attributes unrelated to the clothes. Include details on fabric types, \
                garment fit, cuts of the neckline, sleeves, and bottoms, as well as any accessories. \
                Additionally, based on the descriptors, suggest an aesthetic style label that best \
                fits the outfit’s overall look. Each descriptor can be no more than three words",
                base64_image
            )
        )

        print(response.choices[0].message.content)
