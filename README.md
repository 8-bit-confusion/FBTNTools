# `GalleryScrape`
## Installing `GalleryScrape`
### Manual
- Download the `gallery_scrape.py` file from this github 
- Add it to your project directory

### Command line
Windows Powershell:
```
Invoke-WebRequest `
-Uri https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/gallery_scrape.py `
-OutFile gallery_scrape.py
```
macOS Terminal:
```
curl https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/gallery_scrape.py \
-o gallery_scrape.py
```
Unix/Linux Bash with `curl`:
```
curl https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/gallery_scrape.py \
-o gallery_scrape.py
```
Unix/Linux Bash with `wget`:
```
wget https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/gallery_scrape.py \
-O gallery_scrape.py
```

## Installing `GalleryScrape`'s required packages
### Installing PIP
PIP should come pre-installed with your Python installation, but to make sure you have it installed, you can run the following command:
```
python -m ensurepip --upgrade
```
For more information, see https://pip.pypa.io/en/stable/installation/.

### Code
Call the function `install_packages()` in any python file to automatically download required packagaes (this requires PIP). This function only needs to be called once for a given Python installation.

### Command line
requests:
```
pip install requests
```

gallery-dl:
```
pip install gallery_dl
```

## Using `GalleryScrape` in the command line
The `gallery_scrape.py` can be run in the command line for basic scraping and exporting operations. Command line arguments are available in both the Powershell and Unix styles. The command line utility will scrape the provided source URL and, for each image URL it finds, download and convert it to a base-64 encoding which can be used directly with ChatGPT. The image URLs are stored in the first column of the output `.csv`, and the base-64 encodings are stored in the second column. The output `.csv` file does not include column headers.

### Syntax
Powershell style:
```
python gallery_scrape.py
    [-SourceURL] <String>
    [-OutFile <String>]
```

Unix style:
```
Usage: python gallery_scrape.py <url> [options...]
 -o, --output <file>    Specify output file (defaults to 'out.csv')
```

## Using `GalleryScrape` in your code
The main component of `GalleryScrape` is the `Gallery` class. The `Gallery` class functions as a read-only wrapper for a `dict` which maps image URLs to their base-64 encodings. Encodings can be accessed by indexing the class directly or through the wrapped `.values()` function, and the keys can be accessed through the wrapped `.keys()` function (see examples below).

`Gallery` objects can be created from an online image gallery, such as a pinterest board, by using the static `Gallery.from_url()` constructor. This constructor takes a single argument, `source_url`, which provides the the URL to the image gallery.

`Gallery` objects can also be created with an empty internal `dict` by using the default constructor. The contents of an online image gallery can then be added to the object using the `.add_from_url()` function and supplying the source URL in the `source_url` argument. This method can be used to store multiple online galleries in the same `Gallery` object.

The `Gallery` class also contains a static `download_image()` method, which takes an image URL and returns the base-64 encoding. This is used internally in the `.from_url()` and `.add_from_url()` methods, but is also directly exposed as a utility function.

`Gallery` classes can also be saved to and loaded from `.csv` files (see 'Saving and loading `Gallery` objects' below).

### Encoding access example
```py
example_gallery # Gallery object
example_gallery["<image url>"] # -> base-64 image data associated with key URL
example_gallery.keys() # -> set-like view of all image URLs
example_gallery.values() # -> set-like view of all base-64 encodings
```

### Encoding access example (iterative)
```py
example_gallery # Gallery object
for key in example_gallery.keys(): # iterate through all image URLs
    encoding = example_gallery[key] # access associated image data
```

## Saving and loading `Gallery` objects
`Gallery` objects can be save to and loaded from `.csv` files, allowing you to store them between code runtimes and skip the work of repeating the web scraping and image downloading!

Calling the `.to_csv()` function from an instance of the `Gallery` class will save the object's data to the `.csv` file provided in the `filename` argument. The value of `filename` should be the relative path to the `.csv` file from your script.

Calling the static `Gallery.from_csv()` constructor will generate a new `Gallery` object from the data in the `.csv` file provided in the `filename` arguement. The value of `filename` should be the relative path to the `.csv` file from your script.

### Relative file path example
File structure:
```
project root [folder]
|-- data [folder]
|   |-- data1.csv [target file]
|
|-- main.py [script]
```

Example code:
```py
example_gallery = Gallery.from_csv("data/data1.csv")
example_gallery.to_csv("data/data1.csv")
```

Calling `example_gallery = Gallery.from_csv("data/data1.csv")` correctly loads the desired `.csv` file from the data folder.

Calling `example_gallery.to_csv("data/data1.csv")` correctly saves the `Gallery` object to the desired location within the data folder.

# `ChatUtils`
## Installing `ChatUtils`
### Manual
- Download the `chat_utils.py` file from this github 
- Add it to your project directory

### Command line
Windows Powershell:
```
Invoke-WebRequest `
-Uri https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/chat_utils.py `
-OutFile gallery_scrape.py
```
macOS Terminal:
```
curl https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/chat_utils.py \
-o gallery_scrape.py
```
Unix/Linux Bash with `curl`:
```
curl https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/chat_utils.py \
-o gallery_scrape.py
```
Unix/Linux Bash with `wget`:
```
wget https://raw.githubusercontent.com/8-bit-confusion/FBTN-data/main/chat_utils.py \
-O gallery_scrape.py
```

## Installing `ChatUtils`'s required packages
### Installing PIP
PIP should come pre-installed with your Python installation, but to make sure you have it installed, you can run the following command:
```
python -m ensurepip --upgrade
```
For more information, see https://pip.pypa.io/en/stable/installation/.

### Code
Call the function `install_packages()` in any python file to automatically download required packagaes (this requires PIP). This function only needs to be called once for a given Python installation.

### Command line
dotenv:
```
pip install dotenv
```

openai:
```
pip install openai
```

## Using `dotenv` and `openai` API keys
The `ChatClient` component of `ChatUtils` expects your ChatGPT API key to be stored in the environment variable `OPENAI_API_KEY`. The `dotenv` package is used to load the environment variables. To create an environment variable, first create a file named `.env` in your project directory. _This file must be within the same directory as your main script._ To properly format your `.env` file, see the example below.

### Example setup
File structure:
```
project root [folder]
|-- .env [environment file]
|-- main.py [script]
```

`.env` contents:
```
OPENAI_API_KEY = [API key goes here]
```

Note that the API key is _not_ wrapped in quotation marks.

### Github considerations
If you are using Github as a version control manager and your repository is public, your `.env` file _SHOULD NOT BE TRACKED._ To ensure that it is never tracked, `ignore` the file by creating a file _within your project root directory_ named `.gitignore` and add the following line:

```
.env
```

Not tracking your `.env` file prevents your API keys from being exposed.

## Using `ChatUtils` in your code
`ChatUtils` has two main components: the `Prompts` class, which is used for easily generating properly formatted JSON prompts for ChatGPT, and the `ChatClient` class, which wraps part of the ChatGPT API for easily submitting prompts and saving responses.

### Using `Prompts`
The `Prompts` class has two static functions for generating formatted JSON prompts for use with the ChatGPT API: `.text_prompt()` and `.image_prompt()`. The `.text_prompt()` function takes a single argument, `prompt`, which expects a string containing the text of your prompt. The `.image_prompt()` function also has a `prompt` argument, but takes the additional argument `image`, which expects a string containing the base-64 encoded representation of the image you would like to submit. Base-64 encodings are used in image prompts to ensure that ChatGPT is using the correct image—when providing image URLs, Chat tends to hallucinate image contents. The JSON formatted prompts created by this class can be used with both a `ChatClient` object, or natively with the ChatGPT API.

For more information on aquiring the base-64 encodings for images, see the [`GalleryScrape`](#galleryscrape) tool.

### Using `ChatClient`
The `ChatClient` class wraps part of the ChatGPT API and the `OpenAI` client class. Direct access to the `OpenAI` object is provided through the `ChatClient._client` property, but if you plan on using the `OpenAI` class directly, consider either using the static `.load_client()` function, which will use the API key stored in your `.env` file and return an `OpenAI` object constructed with that key.

`ChatClient` objects have one major function, `.response()`, which wraps the ChatGPT API function `OpenAI.chat.completions.create()`. `.response()` takes any number of JSON formatted prompts as positional parameters, as well as named parameters `system_prompt` and `temperature`. `system_message` expects a string containing the system prompt text, and automatically includes a system prompt in your API call. It's default value is `None`. `temperature` wraps the `temperature` parameter of the `OpenAI.chat.completions.create()` function, and defaults to `0.7`.