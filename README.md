# JsCoverageQC
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

To try the software, you need to have a .gff3 and a .fa as input and set an output filename:
```hubArchiveCreator.py -g test_data/augustusDbia3.gff3 -f test_data/dbia3.fa -o output.zip```

You will get a .zip file, that you need to put on a server accessible from the outside. Then use UCSC track hubs fonctionality to see your track.

## Requirements:
You need to install [Mako](http://www.makotemplates.org/download.html)
