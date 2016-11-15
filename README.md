[![Documentation Status](https://readthedocs.org/projects/g-onramp/badge/?version=documentation)](http://g-onramp.readthedocs.io/en/documentation/?badge=documentation)

# Hub Archive Creator
This Galaxy tool permits to prepare your files to be ready for Assembly Hub visualization.

Into a publicly accessible Galaxy (Linux for maximum tools compatibility), you will be able to use UCSC Genome Browser fonctionality to see your tracks.

## Features
1. Create a structure for your tracks, and convert them to more efficient datatypes (e.g Bed => BigBed)
2. Benefits from Galaxy strong features as well as UCSC Genome Browser's ones without the hassle to move your data from one to another
3. Download and store, as a zip file, your tracks structured for UCSC TrackHub use
4. Create workflows within Galaxy to automatize pipeline analysis and get them ready to visualization inside UCSC Genome Browser...in a few clicks!

At the moment, Supported datatypes are:
- Bam
- Bed (Generic and Simple Repeats)
- BigWig
- Gff3
- Gtf
- Psl

## Installation:
1. You would need to add this tool into your Galaxy.
  1. (strongly preferred) **ToolShed Installation**: Tool is in [toolshed](https://toolshed.g2.bx.psu.edu/view/rmarenco/hubarchivecreator/fb5e60d4d18a)
  2. OR **Local Installation**: See https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial
2. The tool can be used with or without Conda (activate it in your galaxy.ini)
3. If installed without TS (by downloading on GitHub), you need to have all the binaries accessible within Galaxy.
   You can use the script [install_linux_binaries](util/install_linux_binaries) with a linux x86-64 (64bits)
4. Install the UCSC Track Hub datatype:
  1. **Easy** => Use Galaxy 16.07 or latest to directly have Track Hub Datatype (See [this Galaxy Pull Request](https://github.com/galaxyproject/galaxy/pull/2348) for more information)
  2. OR Look into [trackHub README](trackHub/README.md) for more information or if you want to use Galaxy < 16.07

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

## Contribute

- Issue Tracker: https://github.com/remimarenco/hub-archive-creator/issues
- Source Code: https://github.com/remimarenco/hub-archive-creator

## Support

If you are having issues, please let us know.

- For more information about how to use G-OnRamp:
    - [Wilson Leung](wleung@wustl.edu) - Product owner and developer
    - [Yating Liu](yliu41@wustl.edu) - Community manager and Developer
    - [Remi Marenco](remimarenco@gmail.com) - Main developer and Scrum Master

- For more information about the project vision, or for partneship:
    - [Elgin, Sarah](selgin@wustl.edu) - PI
    - [Jeremy Goecks](jgoecks@gwu.edu) - PI
    
## License

The project is licensed under the Academic Free License 3.0. See [LICENSE.txt](LICENSE.txt).
