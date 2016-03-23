"""
HubAssembly datatype
"""
import logging
from galaxy.datatypes.text import Html
from galaxy.datatypes.metadata import MetadataElement

log = logging.getLogger(__name__)


class HubAssembly( Html ):
    """
    derived class for BioC data structures in Galaxy
    """

    # MetadataElement( name="columns", default=0, desc="Number of columns", visible=True )
    # MetadataElement( name="column_names", default=[], desc="Column names", visible=True )
    # MetadataElement(name="pheCols", default=[], desc="Select list for potentially interesting variables",
    # visible=True)
    # MetadataElement( name="base_name",
    # desc="base name for all transformed versions of this expression dataset", default='rexpression',
    # set_in_upload=True)
    # MetadataElement( name="pheno_path", desc="Path to phenotype data for this experiment",
    # default="rexpression.pheno", visible=True)

    file_ext = 'huba'
    composite_type = 'auto_primary_file'

    def __init__(self, **kwd):
        Html.__init__(self, **kwd)
        self.add_composite_file('hub.txt')
        self.add_composite_file('genomes.txt')
        # self.add_composite_file( 'trackDb.txt' )

    def generate_primary_file( self, dataset=None ):
        """
        This is called only at upload to write the html file
        cannot rename the datasets here - they come with the default unfortunately
        """
        rval = [
            '<html><head><title>Files for Composite Dataset (%s)</title></head><p/>\
            This composite dataset is composed of the following files:<p/><ul>' % (
                self.file_ext)]
        for composite_name, composite_file in self.get_composite_files( dataset=dataset ).iteritems():
            opt_text = ''
            if composite_file.optional:
                opt_text = ' (optional)'
            rval.append('<li><a href="%s">%s</a>%s' % ( composite_name, composite_name, opt_text) )
        rval.append('</ul></html>')
        return "\n".join(rval)

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek = "Track Hub structure: Visualization in UCSC Track Hub"
            dataset.blurb = "%s space" % ( dataset.metadata.sequence_space )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Track Hub structure: Visualization in UCSC Track Hub"

    def sniff( self, filename ):
        return False