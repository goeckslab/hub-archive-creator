#!/usr/bin/python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f test-data/dbia3.fa -d . -u ./tools -o output.html
"""

import sys
import tempfile
import getopt
import zipfile
import subprocess
import os
import argparse

from mako.template import Template
from mako.lookup import TemplateLookup

# Internal dependencies
from twoBitCreator import twoBitFileCreator

#TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort

def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    parser.add_argument('-g', '--gff3', help='Directory where to put the foo.txt')
    parser.add_argument('-f', '--fasta', help='Directory where to put the foo.txt')
    parser.add_argument('-d', '--directory', help='Directory where to put the foo.txt')
    parser.add_argument('-u', '--ucsc_tools_path', help='Directory where to put the foo.txt')
    parser.add_argument('-e', '--extra_files_path', help='Directory where to put the foo.txt')
    parser.add_argument('-o', '--output', help='Directory where to put the foo.txt')


    ucsc_tools_path = ''


    toolDirectory = '.'
    extra_files_path = '.'

    # Get the args passed in parameter
    args = parser.parse_args()

    inputGFF3File = open(args.gff3, 'r')
    inputFastaFile = open(args.fasta, 'r')

    if args.directory:
        toolDirectory = args.directory
    if args.extra_files_path:
        extra_files_path = args.extra_files_path
    if args.ucsc_tools_path:
        ucsc_tools_path = args.ucsc_tools_path

    outputZip = zipfile.ZipFile(os.path.join(extra_files_path, 'myHub.zip'), 'w')


    # Create the structure of the Assembly Hub
    # TODO: Merge the following processing into a function as it is also used in twoBitCreator
    baseNameFasta = os.path.basename(inputFastaFile.name)
    suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
    nameTwoBit = suffixTwoBit + '.2bit'

    rootAssemblyHub = createAssemblyHub(outputZip, twoBitName=nameTwoBit, toolDirectory=toolDirectory, extra_files_path=extra_files_path)

    # TODO: See if we need these temporary files as part of the generated files
    genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
    unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
    sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
    twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
    chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

    # gff3ToGenePred processing
    p = subprocess.Popen(
        [os.path.join(ucsc_tools_path, 'gff3ToGenePred'),
            inputGFF3File.name,
            genePredFile.name])
    # We need to wait the time gff3ToGenePred terminate so genePredToBed can begin
    # TODO: Check if we should use communicate instead of wait
    p.wait()

    # genePredToBed processing
    p = subprocess.Popen(
        [os.path.join(ucsc_tools_path, 'genePredToBed'),
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

    mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

    # 2bit file creation from input fasta
    twoBitFile = twoBitFileCreator(inputFastaFile, ucsc_tools_path, mySpecieFolderPath)

    # Generate the chrom.sizes
    # TODO: Isolate in a function
    # We first get the twoBit Infos
    p = subprocess.Popen(
        [os.path.join(ucsc_tools_path, 'twoBitInfo'),
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

    # bedToBigBed processing
    # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
    # TODO: Find the best to get this path without hardcoding it
    myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
    # TODO: Change the name of the bb, to tool + genome + .bb
    myBigBedFilePath = os.path.join(myTrackFolderPath, 'augustusDbia3.bb')
    with open(myBigBedFilePath, 'w') as bigBedFile:
        p = subprocess.Popen(
            [os.path.join(ucsc_tools_path, 'bedToBigBed'),
                sortedBedFile.name,
                chromSizesFile.name,
                bigBedFile.name])
        p.wait()

    # TODO: Add the .bb file in the zip, at the right place

    createZip(outputZip, rootAssemblyHub)

    # outputZip.write(sortedBedFile.name)
    # TODO: Find the best to get this path without hardcoding it

    # outputZip.write(bigBedFile.name)
    outputZip.close()

    # Just a test to output a simple HTML
    with open(args.output, 'w') as htmlOutput:
        htmlOutput.write('<html>')
        htmlOutput.write('<body>')
        htmlOutput.write('<p>')
        htmlOutput.write('The following generated by Hub Archive Creator:')
        htmlOutput.write('</p>')
        htmlOutput.write('<ul>')
        for root, dirs, files in os.walk(extra_files_path):
            # Get all files and get all relative links at the same time
            for file in files:
                relDir = os.path.relpath(root, extra_files_path)
                htmlOutput.write(str.format('<li><a href="{0}">{1}</a></li>', os.path.join(relDir, file), os.path.join(relDir, file)))
        htmlOutput.write('<ul>')
        htmlOutput.write('</body>')
        htmlOutput.write('</html>')

    sys.exit(0)

def createAssemblyHub(outputZip, twoBitName, toolDirectory, extra_files_path):
    # TODO: Manage to put every fill Function in a file dedicated for reading reasons
    # Create the root directory
    myHubPath = os.path.join(extra_files_path, "myHub")
    if not os.path.exists(myHubPath):
        os.makedirs(myHubPath)

    # Add the genomes.txt file
    genomesTxtFilePath = os.path.join(myHubPath, 'genomes.txt')
    fillGenomesTxt(genomesTxtFilePath, twoBitName, toolDirectory)

    # Add the hub.txt file
    hubTxtFilePath = os.path.join(myHubPath, 'hub.txt')
    fillHubTxt(hubTxtFilePath, toolDirectory)

    # Add the hub.html file
    # TODO: Change the name and get it depending on the specie
    hubHtmlFilePath = os.path.join(myHubPath, 'dbia.html')
    fillHubHtmlFile(hubHtmlFilePath, toolDirectory)

    # Create the specie folder
    # TODO: Generate the name depending on the specie
    mySpecieFolderPath = os.path.join(myHubPath, "dbia3")
    if not os.path.exists(mySpecieFolderPath):
        os.makedirs(mySpecieFolderPath)

    # Create the trackDb.txt file in the specie folder
    trackDbTxtFilePath = os.path.join(mySpecieFolderPath, 'trackDb.txt')
    fillTrackDbTxtFile(trackDbTxtFilePath, toolDirectory)

    # Create the description html file in the specie folder
    descriptionHtmlFilePath = os.path.join(mySpecieFolderPath, 'description.html')
    fillDescriptionHtmlFile(descriptionHtmlFilePath, toolDirectory)

    # Create the file groups.txt
    # TODO: If not inputs for this, do no create the file
    groupsTxtFilePath = os.path.join(mySpecieFolderPath, 'groups.txt')
    fillGroupsTxtFile(groupsTxtFilePath, toolDirectory)

    # Create the folder tracks into the specie folder
    tracksFolderPath = os.path.join(mySpecieFolderPath, "tracks")
    if not os.path.exists(tracksFolderPath):
        os.makedirs(tracksFolderPath)

    return myHubPath

def fillGenomesTxt(genomesTxtFilePath, twoBitName, toolDirectory):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    # renderer = pystache.Renderer(search_dirs="templates/genomesAssembly")
    pathTemplate = os.path.join(toolDirectory, 'templates/genomesAssembly')
    mylookup = TemplateLookup(directories=[pathTemplate], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(genomesTxtFilePath, 'w') as genomesTxtFile:
        # Write the content of the file genomes.txt
        twoBitPath = os.path.join('dbia3/', twoBitName)
        htmlMakoRendered = mytemplate.render(
            genomeName="dbia3",
            trackDbPath="dbia3/trackDb.txt",
            groupsPath="dbia3/groups.txt",
            genomeDescription="March 2013 Drosophilia biarmipes unplaced genomic scaffold",
            twoBitPath=twoBitPath,
            organismName="Drosophilia biarmipes",
            defaultPosition="contig1",
            orderKey="4500",
            scientificName="Drosophilia biarmipes",
            pathAssemblyHtmlDescription="dbia3/description.html"
        )
        genomesTxtFile.write(htmlMakoRendered)


def fillHubTxt(hubTxtFilePath, toolDirectory):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/hubTxt')], output_encoding='utf-8', encoding_errors='replace')
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


def fillHubHtmlFile(hubHtmlFilePath, toolDirectory):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    # renderer = pystache.Renderer(search_dirs="templates/hubDescription")
    # t = Template(templates.hubDescription.layout.html)
    mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/hubDescription')], output_encoding='utf-8', encoding_errors='replace')
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


def fillTrackDbTxtFile(trackDbTxtFilePath, toolDirectory):
    # TODO: Modify according to the files passed in parameter
    mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/trackDb')], output_encoding='utf-8', encoding_errors='replace')
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


def fillDescriptionHtmlFile(descriptionHtmlFilePath, toolDirectory):
    # TODO: Think about the inputs and outputs
    # TODO: Manage the template of this file
    mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/specieDescription')], output_encoding='utf-8', encoding_errors='replace')
    mytemplate = mylookup.get_template("layout.txt")
    with open(descriptionHtmlFilePath, 'w') as descriptionHtmlFile:
        # Write the content of the file genomes.txt
        htmlMakoRendered = mytemplate.render(
            specieDescription='This is the description of the dbia',
        )
        descriptionHtmlFile.write(htmlMakoRendered)


def fillGroupsTxtFile(groupsTxtFilePath, toolDirectory):
    mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/groupsTxt')], output_encoding='utf-8', encoding_errors='replace')
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


def createZip(myZip, folder):
    for root, dirs, files in os.walk(folder):
        # Get all files and construct the dir at the same time
        for file in files:
            myZip.write(os.path.join(root, file))

if __name__ == "__main__":
    main(sys.argv)
