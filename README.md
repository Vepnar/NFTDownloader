# NFTDownloader
This is the script used to generate [this](https://www.kaggle.com/vepnar/nft-art-dataset) dataset on kaggle.

To use this dataset you need to have `python3` or higher.
The required dependencies are just `requests` which most of you already have.

## Execute
`python downloader.py`
Currently the data downloaded is around 33 gigabyte and it will take around 4 hours. I recommend to download it from kaggle.

## Configuration
Just edit the python file with `vim downloader.py`. Since I know you can code! :)

## Todo (If you like over optimisation)
- [ ] Improve my grammer mistakes
- [ ] Use an async protocol to do the downloads & requests
- [ ] Add argparse to parse arguments