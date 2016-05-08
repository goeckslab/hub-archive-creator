# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

To try the software, you need to have a .gff3 and a .fa as input and set an output filename:
```hubArchiveCreator.py -g test_data/augustusDbia3.gff3 -f test_data/dbia3.fa -o output.zip```

If you are not using Galaxy (on a public accessible server), you will get a .zip file, that you need to put on a server accessible from the outside. Then use UCSC track hubs fonctionality to see your track.

## Requirements:
1. You need to install [Mako](http://www.makotemplates.org/download.html)
2. HubArchiveCreator use tools from UCSC Kent Utils. This repository use the linux.x86_64/ ones, but you NEED to replace them accordingly to your architecture.
Here is the link to get these tools: http://hgdownload.soe.ucsc.edu/admin/exe/

### Install in Galaxy
1. Take the hubAssembly.py in the hubaDatatype folder, and add it into lib/galaxy/datatypes in your Galaxy instance
2. Use `python ./util/add_datatype.py --galaxy_root path/to/myGalaxy` to add huba datatype to the galaxy your tool is into
3. Look into hubaDatatype/README.md for more informations / in case the script fails for some reasons
4. (Optional) If you want to test your tool locally, you need to install all the tool(shed) dependencies to your PATH.
See [tool_dependencies.xml](tool_dependencies.xml)

See [TODO.md](todo.md) for more informations
