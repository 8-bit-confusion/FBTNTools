# builtin imports
import subprocess
import warnings
import base64
import os

# package imports
try: import requests
except(ImportError): warnings.warn("'requests' module not installed. Try running 'install_drivers()'.")
try: import gallery_dl
except(ImportError): warnings.warn("'gallery_dl' module not installed. Try running 'install_drivers()'.")

def install_drivers():
    subprocess.call("pip install requests")
    subprocess.call("pip install gallery_dl")

class Gallery:
    def __init__(self):
        self.gallery: dict[str, str] = {}

    @classmethod
    def _of(cls, gallery: dict[str, str]):
        of = cls()
        of.gallery = gallery
        return of

    @classmethod
    def from_url(cls, gallery_url: str):
        subprocess.call(f"gallery-dl {gallery_url} -G > tmp.gdlout", shell=True)

        gallery = {}
        with open("tmp.gdlout", 'r') as tmpfile:
            contents = tmpfile.readlines()
            for line in contents:
                url = line.strip()
                gallery[url] = cls.download_img(url)
        
        os.remove("tmp.gdlout")
        return cls._of(gallery)

    @classmethod
    def download_img(cls, image_url: str) -> str:
        response = requests.get(image_url)
        return base64.b64encode(response.content).decode('utf-8')

    @classmethod
    def from_csv(cls, filepath: str):
        gallery = {}
        with open(filepath, 'r') as csv:
            contents = csv.read().split('\n')
            for pair in contents:
                url, img = pair.split(',')
                gallery[url] = img
        return cls._of(gallery)

    def to_csv(self, filename: str):
        if not filename.endswith(".csv"): filename += ".csv"
        with open(filename, 'w') as outfile:
            file_contents = ""
            for key in list(self.gallery.keys()):
                csv_line = key + "," + self.gallery[key]
                file_contents += csv_line + "\n"
            outfile.write(file_contents)

if __name__ == "__main__":
    print("Running 'gallery_scrape' demo. Output file: 'demo.csv'")
    test_gallery = Gallery.from_url("https://www.pinterest.com/iunsct/coquette-outfits/")
    test_gallery.to_csv("demo.csv")
