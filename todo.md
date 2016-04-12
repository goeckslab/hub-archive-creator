# HubArchiveCreator's TODO

*TODO file inspired from: http://lifehacker.com/why-a-github-gist-is-my-favorite-to-do-list-1493063613*

- [ ] Add a class named AugustusProcess: Process the Augustus output to BigBed (and others needed in TrackHub) and (create folders + add the files into the right location => Process can be ported in a class responsible for that)
 - [x] Add a class named AugustusProcess
 - [x] Process the Augustus output to BigBed
 - [x] create folders + add the files into the right location
 - [ ] Creation of folders to be ported into a separated class
 - [ ] Refactoring of the AugustusProcess class to behave like a class and not like a procedural masked into a class
 - [ ] Rename AugustusProcess into something more generic if the process is shared (gtf to BigBed)
- [ ] Add a class named TrfBigProcess
- [x] Add a class named TrackHub: Create the base TrackHub hierarchy
- [ ] Don't let the Tool Classes manage the archive (add or remove files / folders) => Everything should pass through TrackHub or another class dedicated to that
- [ ] Fix the errors for the stdio regexp not properly processed in error case (always green)
- [ ] Move the class and others program related files, into separated folders
