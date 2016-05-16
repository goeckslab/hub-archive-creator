# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

Into a publicly accessible Galaxy (Linux for maximum tools compatibility), you will be able to use UCSC track hubs fonctionality to see your tracks.

## Requirements:
1. You need to install [Mako](http://www.makotemplates.org/download.html)
2. HubArchiveCreator use tools from UCSC Kent Utils. This repository use the linux.x86_64/ ones, but you NEED to replace them accordingly to your architecture.
Here is the link to get these tools: http://hgdownload.soe.ucsc.edu/admin/exe/

### Install in Galaxy
1. Take the hubAssembly.py in the hubaDatatype folder, and add it into lib/galaxy/datatypes in your Galaxy instance
2. [Don't Use it this WIP because of changes for PR into Galaxy]Use `python ./util/add_datatype.py --galaxy_root path/to/myGalaxy` to add huba datatype to the galaxy your tool is into
3. Look into hubaDatatype/README.md for more informations / in case the script fails for some reasons
4. (Optional) If you want to test your tool locally, you need to install all the tool(shed) dependencies to your PATH.
See [tool_dependencies.xml](tool_dependencies.xml)

See [TODO.md](todo.md) for more informations
