Wrangle OpenStreetMap Data
===================

This repo contains files for my "P4 | Wrangle OpenStreetMap Data", completed as a part of Data Analyst Nanodegree in Udacity.

----------


Documents
--

* <i class="icon-folder-open"></i>**Datasets**: This folder contains the downloaded extract of Kolkata from Mapzen.
	* **custom_kolkata.osm.bz2**: My custom extract of Kolkata.
	*  **kolkata_india.osm.bz2**: The popular extract of Kolkata.
* <i class="icon-folder-open"></i>**Documentation**: This folder contains actual report of this project.
	*  **Kolkata.ipynb**: This is the Jupyter Notebook containing the detailed report of my Data Wrangling project.
* <i class="icon-folder-open"></i>**maps_uncompressed**: This folder contains the unzipped extracts and converted JSON for MongoDB import.
	* **custom_kolkata.osm**: The unzipped version of the custom extract of Kolkata.
	* **custom_kolkata.osm.json**: The JSON equivalent of the uncompressed .osm map.
	* **sample1.osm**: A partial equivalent of the uncompressed map mainly used for debugging purposes.
* <i class="icon-folder-open"></i>**Screenshots**: This folder contains the necessary screenshots used as a suggestion for possible improvement of the OSM.
* <i class="icon-file"></i>**sampler.py**: This python script converts the large OSM file to a small sample mainly used for debugging.
* <i class="icon-file"></i>**map_parser.py**: This python script finds the statistics of various tags used in OSM XML.
* <i class="icon-file"></i>**unique_tag_key_finder.py**: This python script finds all the "tag"s unique key values.
* <i class="icon-file"></i>**unusual_tag_key_finder.py**: This python script finds all the "tag"s unique key values that do not have a proper wiki defined in [tagsingo](https://taginfo.openstreetmap.org/).
* <i class="icon-file"></i>**bad_regex_tag_key_finder.py**: The "tag"s unusual key values are grouped according to OSM standards, thus pointing which of them seek immediate attention.

> *the python scripts are listed according to the execution order*

---