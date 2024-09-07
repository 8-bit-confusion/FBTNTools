# builtin imports
import subprocess
import warnings
import base64
import sys
import os

# package imports
try: import requests
except(ImportError): warnings.warn("'requests' module not installed. Try running 'install_drivers()'.")
try: import gallery_dl
except(ImportError): warnings.warn("'gallery_dl' module not installed. Try running 'install_drivers()'.")

def install_packages():
    subprocess.call("pip install requests")
    subprocess.call("pip install gallery_dl")

class Gallery:
    def __init__(self):
        self._gallery: dict[str, str] = {}
    
    def __getitem__(self, key: str) -> str:
        return self._gallery[key]
    
    def keys(self): return self._gallery.keys()
    def values(self): return self._gallery.values()

    @classmethod
    def _of(cls, gallery: dict[str, str]):
        of = cls()
        of._gallery = gallery
        return of

    @classmethod
    def from_url(cls, source_url: str):
        subprocess.call(f"gallery-dl {source_url} -G > tmp.gdlout", shell=True)

        gallery = {}
        with open("tmp.gdlout", 'r') as tmpfile:
            contents = tmpfile.readlines()
            for line in contents:
                url = line.strip()
                gallery[url] = cls.download_img(url)
        
        os.remove("tmp.gdlout")
        return cls._of(gallery)
    
    def add_from_url(self, source_url: str):
        subprocess.call(f"gallery-dl {source_url} -G > tmp.gdlout", shell=True)

        with open("tmp.gdlout", 'r') as tmpfile:
            contents = tmpfile.readlines()
            for line in contents:
                url = line.strip()
                self._gallery[url] = Gallery.download_img(url)
        
        os.remove("tmp.gdlout")

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
    out_file = "out.csv"
    source_url = ""

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg in ("-o", "--output", "-OutFile"):
            out_file = sys.argv[i + 1]
            i += 1
        elif arg in ("-SourceURL"):
            source_url = sys.argv[i + 1]
            i += 1
        else: source_url = arg
    
    if source_url == "":
        print("No source url provided. Exiting...")
        quit()
    
    tmp_gallery = Gallery.from_url(source_url)
    tmp_gallery.to_csv(out_file)