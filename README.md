# material-design-icons-uploader
Script for extracting metadata and uploading subsets of material design icons.

If you want to create your own icon picker using the material icon sets, this script is for you.

# Setup

First, we have to fetch the original [material-design-icons](https://github.com/google/material-design-icons) submodule.

```
git submodule init
git submodule update
```

# Generating a list of available icon names

Generate the list of available icon names with the following command:

```
python3 uploader.py
```

If you just want to grab the list of names as a JSON array, see `list.json` for a simple list of all the available material icon names, or `filenames.json` for a map of icon names to filenames.

# Uploading icons to an S3 bucket

If you'd like to upload a copy of the icons to an S3 bucket, run the following command.

```
python3 uploader.py --s3bucket s3://my-s3-bucket/folder/with/slash/
```

Note that this requires you have the `aws` command line utility installed and authenticated.

# TODO

- Support for extracting icons in formats other than SVG
