#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import tempfile
import shutil
import zipfile

# Internal dependencies
from Datatype import Datatype
from util import subtools

from mako.lookup import TemplateLookup


class TrackHub(object):
    """docstring for TrackHub"""

    def __init__(self, inputFastaFile, user_email, outputFile, extra_files_path, tool_directory):
        super(TrackHub, self).__init__()

        self.rootAssemblyHub = None

        self.mySpecieFolderPath = None
        self.myTracksFolderPath = None
        self.tool_directory = tool_directory

        self.reference_genome = inputFastaFile
        # TODO: Add the specie name
        self.genome_name = None
        self.default_pos = None
        self.user_email = user_email

        # TODO: Modify according to the files passed in parameter
        mylookup = TemplateLookup(directories=[os.path.join(tool_directory, 'templates/trackDb')],
                                  output_encoding='utf-8', encoding_errors='replace')
        self.trackDbTemplate = mylookup.get_template("layout.txt")

        self.extra_files_path = extra_files_path
        self.outputFile = outputFile

        # Create the structure of the Assembly Hub
        # TODO: Merge the following processing into a function as it is also used in twoBitCreator
        self.twoBitName = None
        self.two_bit_final_path = None
        self.chromSizesFile = None

        self.default_pos = None

        # Set all the missing variables of this class, and create physically the folders/files
        self.rootAssemblyHub = self.__createAssemblyHub__(extra_files_path=extra_files_path)

        # Init the Datatype
        Datatype.pre_init(self.reference_genome, self.two_bit_final_path, self.chromSizesFile,
                          self.extra_files_path, self.tool_directory,
                          self.mySpecieFolderPath, self.myTracksFolderPath)

    def createZip(self):
        for root, dirs, files in os.walk(self.rootAssemblyHub):
            # Get all files and construct the dir at the same time
            for file in files:
                self.outputZip.write(os.path.join(root, file))

        self.outputZip.close()

    def addTrack(self, trackDbObject=None):
        # Create the trackDb.txt file in the specie folder, if not exists
        # Else append the new track
        trackDbTxtFilePath = os.path.join(self.mySpecieFolderPath, 'trackDb.txt')

        # Append to trackDbTxtFilePath the trackDbTemplate populate with the newTrack object
        with open(trackDbTxtFilePath, 'a+') as trackDbFile:
            trackDbs = [trackDbObject]
            htmlMakoRendered = self.trackDbTemplate.render(
                trackDbs=trackDbs
            )
            trackDbFile.write(htmlMakoRendered)

    def terminate(self):
        # Just a test to output a simple HTML
        # TODO: Create a class to handle the file object
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates')],
                                  output_encoding='utf-8', encoding_errors='replace')

        mytemplate = mylookup.get_template('display.txt')
        with open(self.outputFile, 'w') as htmlOutput:
            # TODO: We are basically looping two times: One time with os.walk, Second time
            # with the template. We could improve that if the number of files begins to be really important
            list_relative_file_path = [ ]
            for root, dirs, files in os.walk(self.extra_files_path):
                for file in files:
                    relative_directory = os.path.relpath(root, self.extra_files_path)
                    relative_file_path = os.path.join(relative_directory, file)
                    list_relative_file_path.append(relative_file_path)

            htmlMakoRendered = mytemplate.render(
                list_relative_file_path=list_relative_file_path
            )
            htmlOutput.write(htmlMakoRendered)

    def __createAssemblyHub__(self, extra_files_path):
        # Get all necessaries infos first
        # 2bit file creation from input fasta

        # baseNameFasta = os.path.basename(fasta_file_name)
        # suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
        # nameTwoBit = suffixTwoBit + '.2bit'
        twoBitFile = tempfile.NamedTemporaryFile(bufsize=0)
        subtools.faToTwoBit(self.reference_genome.false_path, twoBitFile.name)

        # Generate the twoBitInfo
        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        subtools.twoBitInfo(twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to generate the chromSizes
        self.chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")
        subtools.sortChromSizes(twoBitInfoFile.name, self.chromSizesFile.name)

        # We can get the biggest scaffold here, with chromSizesFile
        with open(self.chromSizesFile.name, 'r') as chrom_sizes:
            # TODO: Check if exists
            self.default_pos = chrom_sizes.readline().split()[0]

        # TODO: Manage to put every fill Function in a file dedicated for reading reasons
        # Create the root directory
        myHubPath = os.path.join(extra_files_path, "myHub")
        if not os.path.exists(myHubPath):
            os.makedirs(myHubPath)

        # Create the specie folder
        # TODO: Generate the name depending on the specie
        mySpecieFolderPath = os.path.join(myHubPath, "dbia3")
        if not os.path.exists(mySpecieFolderPath):
            os.makedirs(mySpecieFolderPath)
        self.mySpecieFolderPath = mySpecieFolderPath

        # We create the 2bit file while we just created the specie folder
        self.genome_name = "dbia3"
        self.twoBitName = self.genome_name + ".2bit"
        self.two_bit_final_path = os.path.join(self.mySpecieFolderPath, self.twoBitName)
        shutil.copyfile(twoBitFile.name, self.two_bit_final_path)

        # Add the genomes.txt file
        genomesTxtFilePath = os.path.join(myHubPath, 'genomes.txt')
        self.__fillGenomesTxt__(genomesTxtFilePath)

        # Add the hub.txt file
        hubTxtFilePath = os.path.join(myHubPath, 'hub.txt')
        self.__fillHubTxt__(hubTxtFilePath)

        # Add the hub.html file
        # TODO: Change the name and get it depending on the specie
        hubHtmlFilePath = os.path.join(myHubPath, 'dbia.html')
        self.__fillHubHtmlFile__(hubHtmlFilePath)


        # Create the description html file in the specie folder
        descriptionHtmlFilePath = os.path.join(mySpecieFolderPath, 'description.html')
        self.__fillDescriptionHtmlFile__(descriptionHtmlFilePath)

        # Create the file groups.txt
        # TODO: If not inputs for this, do no create the file
        groupsTxtFilePath = os.path.join(mySpecieFolderPath, 'groups.txt')
        self.__fillGroupsTxtFile__(groupsTxtFilePath)

        # Create the folder tracks into the specie folder
        tracksFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        if not os.path.exists(tracksFolderPath):
            os.makedirs(tracksFolderPath)
        self.myTracksFolderPath = tracksFolderPath

        return myHubPath

    def __fillGenomesTxt__(self, genomesTxtFilePath):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        # renderer = pystache.Renderer(search_dirs="templates/genomesAssembly")
        pathTemplate = os.path.join(self.tool_directory, 'templates/genomesAssembly')
        mylookup = TemplateLookup(directories=[pathTemplate], output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(genomesTxtFilePath, 'w') as genomesTxtFile:
            # Write the content of the file genomes.txt
            twoBitPath = os.path.join(self.genome_name, self.twoBitName)
            htmlMakoRendered = mytemplate.render(
                genomeName=self.genome_name,
                trackDbPath=os.path.join(self.genome_name, "trackDb.txt"),
                groupsPath=os.path.join(self.genome_name, "groups.txt"),
                genomeDescription="March 2013 Drosophilia biarmipes unplaced genomic scaffold",
                twoBitPath=twoBitPath,
                organismName=self.genome_name,
                defaultPosition=self.default_pos,
                orderKey="4500",
                scientificName=self.genome_name,
                pathAssemblyHtmlDescription=os.path.join(self.genome_name, "description.html")
            )
            genomesTxtFile.write(htmlMakoRendered)

    def __fillHubTxt__(self, hubTxtFilePath):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates/hubTxt')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template('layout.txt')
        with open(hubTxtFilePath, 'w') as genomesTxtFile:
            # Write the content of the file genomes.txt
            htmlMakoRendered = mytemplate.render(
                hubName='dbiaOnly',
                shortLabel='dbia',
                longLabel='This hub only contains dbia with the gene predictions',
                genomesFile='genomes.txt',
                email='rmarenco@gwu.edu',
                descriptionUrl='dbia.html'
            )
            genomesTxtFile.write(htmlMakoRendered)

    def __fillHubHtmlFile__(self, hubHtmlFilePath):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        # renderer = pystache.Renderer(search_dirs="templates/hubDescription")
        # t = Template(templates.hubDescription.layout.html)
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates/hubDescription')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(hubHtmlFilePath, 'w') as hubHtmlFile:
            htmlMakoRendered = mytemplate.render(
                specie='Dbia',
                toolUsed='Augustus',
                ncbiSpecieUrl='http://www.ncbi.nlm.nih.gov/genome/3499',
                genomeID='3499',
                specieFullName='Drosophila biarmipes'
            )
            hubHtmlFile.write(htmlMakoRendered)

    def __fillDescriptionHtmlFile__(self, descriptionHtmlFilePath):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates/specieDescription')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(descriptionHtmlFilePath, 'w') as descriptionHtmlFile:
            # Write the content of the file genomes.txt
            htmlMakoRendered = mytemplate.render(
                specieDescription='This is the description of the dbia',
            )
            descriptionHtmlFile.write(htmlMakoRendered)

    def __fillGroupsTxtFile__(self, groupsTxtFilePath):
        # TODO: Reenable this function at some point
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates/groupsTxt')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(groupsTxtFilePath, 'w') as groupsTxtFile:
            # Write the content of groups.txt
            # groupsTxtFile.write('name map')
            htmlMakoRendered = mytemplate.render(
                mapName='map',
                labelMapping='Mapping',
                prioriy='2',
                isClosed='0'
            )
            # groupsTxtFile.write(htmlMakoRendered)
