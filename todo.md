# HubArchiveCreator's TODO

*TODO file inspired from: http://lifehacker.com/why-a-github-gist-is-my-favorite-to-do-list-1493063613*

### TO COMPLETE

 
- [ ] Don't let the Tool Classes manage the archive (add or remove files / folders) => Everything should pass through TrackHub or another class dedicated to that
- [ ] Move the class and others program related files, into separated folders
- [ ] Take into account the name of the reference genome / the change:
  - [ ] Somebody could want to launch two visualisations of two different genomes. Repeats of Genome with extensions associated
- [ ] Add TDD => First add the test. It should not pass. Implement. It should now pass :)
- [ ] Replace Gff3 by an abstract class GeneralFormat, with two sub-classes GFF3Format and GTFFormat
- [ ] TrackHub should check if the 2bit already exists instead of recreating it (which is the case atm)
- [ ] Manage the error when a user is selecting Generic Bed instead of Bed Simple Repeats. Two options: a. Output a better error message ("Check with the other Bed options") b. Identify internally this is not a regular BED but a specific one
- [ ] Remove the non-explicit parameters for the communication between Galaxy Wrapper and the entry point
- [ ] Rename all occurences of `extension` which `datatype`
- [ ] Follow https://google.github.io/styleguide/pyguide.html
- [ ] Move to Python 3
- [ ] Remove the repetition of the extension if it already exists
- [ ] Better thinking about the tool_directory management / Classes path refactoring
- [ ] Add a debug mode to have more outputs
- [ ] Improve the standard output of HAC

### DONE


- [x] Each time a file is added => Print it in the output with the full path (or relative path to root)
- [x] Add a script for Linux.x86_64 to download and and chmod +x the dependencies for local testing => util/install_linux_binaries.py
- [x] Add sorting BED if not sorted (Use the output of bedToBigBed)
- [x] Add a script to install the huba datatype
- [x] Add the possibility to add a new item in TrackDb.txt through a public function from TrackHub.py => addTrack() in TrackHub.py
- [x] Fix the errors for the stdio regexp not properly processed in error case (always green) => Used `detect_errors` in  galaxy wrapper and raise Exception in Python
- [x] Add a class named ~~TrfBigProcess~~ BedSimpleRepeats
- [x] Add a class named TrackHub: Create the base TrackHub hierarchy
- [x] Change the Name of the classes
- [x] Add a class named AugustusProcess: Process the Augustus output to BigBed (and others needed in TrackHub) and (create folders + add the files into the right location => Process can be ported in a class responsible for that)
 - [x] Add a class named AugustusProcess
 - [x] Process the Augustus output to BigBed
 - [x] create folders + add the files into the right location
 - [x] Creation of folders to be ported into a separated class => In Datatype.py but should be into a dedicated to file manipulation class
 - [x] Refactoring of the AugustusProcess class to behave like a class and not like a procedural masked into a class
 - [x] Rename AugustusProcess into something more generic if the process is shared (gtf to BigBed) => Gff3.py
- [x] Use gffToBed for Gtf instead of GtfToGenePred => Cancelled
- [x] Clean the mess with the File handling (sometimes File, sometimes String, sometimes open File)
- [x] Find a way to avoid repetitions in TrackDb and Track (I repeat myself atm) => Track instance has a TrackDb instance as attribute
- [x] Refactor the creation of the structure to TrackHub: Access to paths via this Class, and creation of file through it
