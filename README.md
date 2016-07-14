# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

Into a publicly accessible Galaxy (Linux for maximum tools compatibility), you will be able to use UCSC track hubs fonctionality to see your tracks.

At the moment, Supported datatypes are:
- Bam
- Bed (Generic and Simple Repeats)
- BigWig
- Gff3
- Gtf

## Requirements:
1. You need to add this tool into your Galaxy.
  1. **Local Installation**: See https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial
  2. OR **ToolShed Installation**: Tool is in toolshed now
2. The tool can be used with or without Conda (activate it in your galaxy.ini)
3. If installed without TS (by downloading on GitHub), you need to have all the binaries accessible within Galaxy.
   You can use the script [install_linux_binaries](util/install_linux_binaries) with a linux x86-64 (64bits)
4. Install the UCSC Track Hub datatype:
  1. **Don't Use it this WIP because of changes for [PR into Galaxy](https://github.com/galaxyproject/galaxy/pull/2348)** ~~Use `python ./util/add_datatype.py --galaxy_root path/to/myGalaxy` to add huba datatype to the galaxy your tool is into~~
  2. Look into [trackHub README](trackHub/README.md) for more information / in case the script fails for some reasons

### Binaries used by HAC:
- twoBitInfo
- faToTwoBit
- gff3ToGenePred
- gtfToGenePred
- genePredToBed
- sort
- bedToBigBed
See [SubTools.py](util/SubTools.py) for up-to-date used binaries and [tool_dependencies.xml](tool_dependencies.xml)

## Future
See [TODO.md](todo.md) for more informations
