Wrangle OpenStreetMap Data
==========================

This repo contains files for my "P4 | Wrangle OpenStreetMap Data", done as a part of Data Analyst Nanodegree in Udacity.



Documents
---------

* **Datasets**: This folder contains the downloaded extract of Kolkata from Mapzen.
	* **custom_kolkata.osm.bz2**: My custom extract of Kolkata that I used throughout the project.
	*  **kolkata_india.osm.bz2**: The popular extract of Kolkata.
* **Documentation**: This folder contains actual report of this project.
	*  **Kolkata.ipynb**: This is the Jupyter Notebook containing the detailed report of my Data Wrangling project.
* **maps_uncompressed**: This folder contains the unzipped extracts and converted JSON for MongoDB import.
	* **custom_kolkata.osm** *(please refer to notes)*: The unzipped version of the custom extract of Kolkata.
	* **custom_kolkata.osm.json** *(please refer to notes)*: The JSON equivalent of the uncompressed .osm map.
	* **sample1.osm**: A partial equivalent of the uncompressed map mainly used for debugging purposes.
* **Screenshots**: This folder contains the necessary screenshots used as a suggestion for possible improvement of the OSM.
* **sampler.py**: This python script converts the large OSM file to a small sample mainly used for debugging.
* **map_parser.py**: This python script finds the statistics of various tags used in OSM XML.
* **unique_tag_key_finder.py**: This python script finds all the "tag"s unique key values.
* **unusual_tag_key_finder.py**: This python script finds all the "tag"s unique key values that do not have a proper wiki defined in [tagsingo](https://taginfo.openstreetmap.org/).
* **bad_regex_tag_key_finder.py**: The "tag"s unusual key values are grouped according to OSM standards, thus pointing which of them seek immediate attention.
* **unusual_key_value_gen.py**: This python scripts populates the unusual "tag"s keys with their values mainly for understanding the data well.
* **functions.py**: This python script contains the various arterial functions needed by the other python scripts and mappings needed for cleaning the messy data while forming the JSON.
* **json_maker.py**: This python scripts converts the OSM XML to JSON to be imported to MongoDB.
* **mongo_test_commands.txt**: This file contains various MongoDB shell commands that can be used for verification if the JSON is generated and fed as expected.
* **order_of_execution.txt**: This text file contains the order in which the python scripts should be executed.

> **Note**
> The .osm and .json cannot be included due to the large size (I am having some issues with git lfs). There are two ways to use them tough.
>
> * You can uncompress *"custom_kolkata.osm.bz2"* that is present inside the *"Datasets"* directory.
>
>* You can also download it via this [custom .osm extract link](https://mapzen.com/data/metro-extracts/your-extracts/320cb2360f25) which is accessible if you create a free Mapzen Account. 
>
>* Please ensure that the uncompressed custom extract is stored in the *"maps_uncompressed"* directory and be named *"custom_kolkata.osm."* (alternatively the OSM file location can be changed by modifying the variable *"OSM_file"* in *"functions.py"*. 
>
> * The .json can be created in the same location of the .osm by running the *"json_maker.py"*.
>
> I apologize for the inconvenience. Hopefully I'll get working soon.

---
