# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

Into a publicly accessible Galaxy (Linux for maximum tools compatibility), you will be able to use UCSC track hubs fonctionality to see your tracks.

## Requirements:
1. You need to add this tool into your Galaxy. See https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial
2. You need to enable Conda in you Galaxy (galaxy.ini)
3. If installed without TS (by downloading on GitHub), you need to have all the binaries accessible within Galaxy
4. Install the UCSC Track Hub datatype:
  1. Take the hubAssembly.py in the hubaDatatype folder, and add it into lib/galaxy/datatypes in your Galaxy instance
  2. **Don't Use it this WIP because of changes for PR into Galaxy** ~~Use `python ./util/add_datatype.py --galaxy_root path/to/myGalaxy` to add huba datatype to the galaxy your tool is into~~
  3. Look into [hubaDatatype README(hubaDatatype/README.md) for more informations / in case the script fails for some reasons

### Binaries used by HAC:
- twoBitInfo
- faToTwoBit
- gff3ToGenePred
- genePredToBed
- sort
- bedToBigBed
See [SubTools.py](util/SubTools.py) for up-to-date used binaries and [tool_dependencies.xml](tool_dependencies.xml)

## Future
See [TODO.md](todo.md) for more informations
