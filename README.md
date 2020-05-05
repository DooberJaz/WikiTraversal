# WikiTraversal
An assortment of code and text files used in my dissertation

# Description of the files

WeightedWiki.zip - A zip file containing a plaintext file of the weighted wiki. This is the file that is used by the WikiTraversal.py code

BrokenLinks.txt - A list of all the links that were encountered in the wikipedia file that did not lead to any pages

WikiTraversal.py - Python code that can load in weightedwiki and run various methods to find a route from a wikipedia page to another wikipedia page. For Dijkstra's to run effectively, assign weights must be run first. It must be rerun for every new final page that is used

WikiTrimmer.java - Java code that takes in a raw data-dump of Wikipedia and compresses it to a smaller version that can be used by the python fie. The raw wikipedia data-dump cannot be provided as it is 750MB uncompressed, and 250MB compressed.
