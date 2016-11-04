# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

Into a publicly accessible Galaxy (Linux for maximum tools compatibility), you will be able to use UCSC track hubs fonctionality to see your tracks.

At the moment, Supported datatypes are:
- Bam
- Bed (Generic and Simple Repeats)
- BigWig
- Gff3
- Gtf
- Psl

## Requirements:
1. You need to add this tool into your Galaxy.
  1. **Local Installation**: See https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial
  2. OR **ToolShed Installation**: Tool is in [toolshed](https://toolshed.g2.bx.psu.edu/view/rmarenco/hubarchivecreator/fb5e60d4d18a)
2. The tool can be used with or without Conda (activate it in your galaxy.ini)
3. If installed without TS (by downloading on GitHub), you need to have all the binaries accessible within Galaxy.
   You can use the script [install_linux_binaries](util/install_linux_binaries) with a linux x86-64 (64bits)
4. Install the UCSC Track Hub datatype:
  1. Use Galaxy 16.07 or latest to directly have Track Hub Datatype (See [this Galaxy Pull Request](https://github.com/galaxyproject/galaxy/pull/2348) for more information)
  2. Look into [trackHub README](trackHub/README.md) for more information or if you want to use Galaxy < 16.07

### Binaries used by HAC:
- bedToBigBed
- faToTwoBit
- genePredToBed
- genePredToBigGenePred
- gff3ToGenePred
- gtfToGenePred
- pslToBigPsl
- samtools
- sort
- twoBitInfo
See `<requirements` in [tool_dependencies.xml](tool_dependencies.xml) for an up-to-date used binaries list

## Future
See [TODO.md](todo.md) for more information
