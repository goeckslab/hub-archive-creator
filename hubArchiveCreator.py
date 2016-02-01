#!/usr/bin/python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test_data/augustusDbia3.gff3 -f test_data/dbia3.fa -o output.zip
"""

import sys
import tempfile
import getopt
import zipfile
import subprocess
import os
import pystache

from mako.template import Template
from mako.lookup import TemplateLookup

# Internal dependencies
from twoBitCreator import twoBitFileCreator


def main(argv):
    inputGFF3File = ''
    inputFastaFile = ''

    try:
        opts, args = getopt.getopt(argv,
            "hg:f:o:",
            ['help',
            'gff3=',
            'fasta=',
            'output='])
    except getopt.GetoptError:
        # TODO: Modify
        print 'hubArchiveCreator.py -if <inputFastaFile> -ig <inputGFF3File> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', 'help'):
            # TODO: Modify
            print 'test.py -if <inputFastaFile> -ig <inputGFF3File> -o <outputfile>'
            sys.exit()
        elif opt in ("-g", 'gff3'):
            # We retrieve the input file
            inputGFF3File = open(arg, 'r')
        elif opt in ("-f", 'fasta'):
            # We retrieve the input file
            inputFastaFile = open(arg, 'r')
        elif opt in ("-o", 'output'):
            outputZip = zipfile.ZipFile(arg, 'w')

            # Create the structure of the Assembly Hub
            rootAssemblyHub = createAssemblyHub(outputZip)

            # TODO: See if we need these temporary files as part of the generated files
            genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
            unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
            sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
            twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
            chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

            # gff3ToGenePred processing
            p = subprocess.Popen(
                ['tools/gff3ToGenePred',
                    inputGFF3File.name,
                    genePredFile.name])
            # We need to wait the time gff3ToGenePred terminate so genePredToBed can begin
            # TODO: Check if we should use communicate instead of wait
            p.wait()

            # genePredToBed processing
            p = subprocess.Popen(
                ['tools/genePredToBed',
                    genePredFile.name,
                    unsortedBedFile.name])
            p.wait()

            # Sort processing
            p = subprocess.Popen(
                ['sort',
                    '-k'
                    '1,1',
                    '-k'
                    '2,2n',
                    unsortedBedFile.name,
                    '-o',
                    sortedBedFile.name])
            p.wait()

            # 2bit file creation from input fasta
            twoBitFile = twoBitFileCreator(inputFastaFile)

            # Generate the chrom.sizes
            # TODO: Isolate in a function
            # We first get the twoBit Infos
            p = subprocess.Popen(
                ['tools/twoBitInfo',
                    twoBitFile.name,
                    'stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            twoBitInfo_out, twoBitInfo_err = p.communicate()
            twoBitInfoFile.write(twoBitInfo_out)

            # Then we get the output to inject into the sort
            # TODO: Check if no errors
            p = subprocess.Popen(
                ['sort',
                    '-k2rn',
                    twoBitInfoFile.name,
                    '-o',
                    chromSizesFile.name])
            p.wait()

            createZip(outputZip, rootAssemblyHub)

            # outputZip.write(sortedBedFile.name)
            # TODO: Find the best to get this path without hardcoding it
            mySpecieFolderPath = os.path.join("myHub", "dbia3")
            twoBitFileFinalLocation = os.path.join(mySpecieFolderPath, os.path.basename(twoBitFile.name))
            outputZip.write(twoBitFile.name, twoBitFileFinalLocation)

            # bedToBigBed processing
            # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
            # TODO: Find the best to get this path without hardcoding it
            myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
            # TODO: Change the name of the bb, to tool + genome + .bb
            myBigBedFilePath = os.path.join(myTrackFolderPath, 'augustusDbia3.bb')
            with open(myBigBedFilePath, 'w') as bigBedFile:
                p = subprocess.Popen(
                    ['tools/bedToBigBed',
                        sortedBedFile.name,
                        chromSizesFile.name,
                        bigBedFile.name])
                p.wait()
            outputZip.write(bigBedFile.name)

            # TODO: Add the .bb file in the zip, at the right place
            # outputZip.write(bigBedFile.name)

            # outputZip.write(bigBedFile.name)
            outputZip.close()


def createAssemblyHub(outputZip):
    # TODO: Manage to put every fill Function in a file dedicated for reading reasons
    # Create the root directory
    myHubPath = "myHub"
    if not os.path.exists(myHubPath):
        os.makedirs(myHubPath)

    # Add the genomes.txt file
    genomesTxtFilePath = os.path.join(myHubPath, 'genomes.txt')
    fillGenomesTxt(genomesTxtFilePath)

    # Add the hub.txt file
    hubTxtFilePath = os.path.join(myHubPath, 'hub.txt')
    fillHubTxt(hubTxtFilePath)

    # Add the hub.html file
    # TODO: Change the name and get it depending on the specie
    hubHtmlFilePath = os.path.join(myHubPath, 'dbia.html')
    fillHubHtmlFile(hubHtmlFilePath)

    # Create the specie folder
    # TODO: Generate the name depending on the specie
    mySpecieFolderPath = os.path.join(myHubPath, "dbia3")
    if not os.path.exists(mySpecieFolderPath):
        os.makedirs(mySpecieFolderPath)

    # Create the trackDb.txt file in the specie folder
    trackDbTxtFilePath = os.path.join(mySpecieFolderPath, 'trackDb.txt')
    fillTrackDbTxtFile(trackDbTxtFilePath)

    # Create the description html file in the specie folder
    descriptionHtmlFilePath = os.path.join(mySpecieFolderPath, 'description.html')
    fillDescriptionHtmlFile(descriptionHtmlFilePath)

    # Create the file groups.txt
    # TODO: If not inputs for this, do no create the file
    groupsTxtFilePath = os.path.join(mySpecieFolderPath, 'groups.txt')
    fillGroupsTxtFile(groupsTxtFilePath)

    # Create the folder tracks into the specie folder
    tracksFolderPath = os.path.join(mySpecieFolderPath, "tracks")
    if not os.path.exists(tracksFolderPath):
        os.makedirs(tracksFolderPath)

    return myHubPath


def fillGenomesTxt(genomesTxtFilePath):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    # renderer = pystache.Renderer(search_dirs="templates/genomesAssembly")
    mylookup = TemplateLookup(directories=['templates/genomesAssembly'], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(genomesTxtFilePath, 'w') as genomesTxtFile:
        # Write the content of the file genomes.txt
        htmlMakoRendered = mytemplate.render(
            genomeName="dbia3",
            trackDbPath="dbia3/trackDb.txt",
            groupsPath="dbia3/groups.txt",
            genomeDescription="March 2013 Drosophilia biarmipes unplaced genomic scaffold",
            twoBitPath="dbia3/dbia3.2bit",
            organismName="Drosophilia biarmipes",
            defaultPosition="contig1",
            orderKey="4500",
            scientificName="Drosophilia biarmipes",
            pathAssemblyHtmlDescription="dbia3/description.html"
        )
        genomesTxtFile.write(htmlMakoRendered)


def fillHubTxt(hubTxtFilePath):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    mylookup = TemplateLookup(directories='templates/hubTxt', output_encoding='utf-8', encoding_errors='replace')
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


def fillHubHtmlFile(hubHtmlFilePath):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    # renderer = pystache.Renderer(search_dirs="templates/hubDescription")
    # t = Template(templates.hubDescription.layout.html)
    mylookup = TemplateLookup(directories=['templates/hubDescription'], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(hubHtmlFilePath, 'w') as hubHtmlFile:
        # Write the content of the file genomes.txt
        # htmlPystached = renderer.render_name(
        #     "layout",
        #     {'specie': 'Dbia',
        #     'toolUsed': 'Augustus',
        #     'ncbiSpecieUrl': 'http://www.ncbi.nlm.nih.gov/genome/3499',
        #     'genomeID': '3499',
        #     'SpecieFullName': 'Drosophila biarmipes'})
        htmlMakoRendered = mytemplate.render(
            specie='Dbia',
            toolUsed='Augustus',
            ncbiSpecieUrl='http://www.ncbi.nlm.nih.gov/genome/3499',
            genomeID='3499',
            specieFullName='Drosophila biarmipes'
        )
        # hubHtmlFile.write(htmlPystached)
        hubHtmlFile.write(htmlMakoRendered)


def fillTrackDbTxtFile(trackDbTxtFilePath):
    # TODO: Modify according to the files passed in parameter
    mylookup = TemplateLookup(directories=['templates/trackDb'], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(trackDbTxtFilePath, 'w') as trackDbFile:
        htmlMakoRendered = mytemplate.render(
            trackName='augustusTrack',
            trackDataURL='Augustus_dbia3',
            shortLabel='a_dbia',
            longLabel='tracks/augustusDbia3.bb',
            trackType='bigBed 12 +',
            visibility='dense'
        )
        trackDbFile.write(htmlMakoRendered)


def fillDescriptionHtmlFile(descriptionHtmlFilePath):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    mylookup = TemplateLookup(directories=['templates/specieDescription'], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(descriptionHtmlFilePath, 'w') as descriptionHtmlFile:
        # Write the content of the file genomes.txt
        htmlMakoRendered = mytemplate.render(
            specieDescription='This is the description of the dbia',
        )
        descriptionHtmlFile.write(htmlMakoRendered)


def fillGroupsTxtFile(groupsTxtFilePath):
    mylookup = TemplateLookup(directories=['templates/groupsTxt'], output_encoding='utf-8', encoding_errors='replace')
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
        groupsTxtFile.write(htmlMakoRendered)


def createZip(myZip, folder):
    for root, dirs, files in os.walk(folder):
        # Get all files and construct the dir at the same time
        for file in files:
            myZip.write(os.path.join(root, file))

if __name__ == "__main__":
    main(sys.argv[1:])
