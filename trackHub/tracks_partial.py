"""
HubAssembly datatype
"""
import logging

from galaxy.datatypes.text import Html

log = logging.getLogger( __name__ )

# !!! README !!! The content of this file should be added in tracks.py, but do it carefully!
# Don't erase the existing content


class UCSCTrackHub( Html ):
    """
    derived class for BioC data structures in Galaxy
    """

    file_ext = 'trackhub'
    composite_type = 'auto_primary_file'

    def __init__( self, **kwd ):
        Html.__init__( self, **kwd )

    def generate_primary_file( self, dataset=None ):
        """
        This is called only at upload to write the html file
        cannot rename the datasets here - they come with the default unfortunately
        """
        rval = [
            '<html><head><title>Files for Composite Dataset (%s)</title></head><p/>\
            This composite dataset is composed of the following files:<p/><ul>' % (
                self.file_ext)]

        def create_tree(path, tree):
            if path[0] in tree:
                create_tree(path[1:], tree[path[0]])
            else:
                tree[path[0]] = {}
                if len(path) == 1:
                    return
                else:
                    create_tree(path[1:], tree[path[0]])

        def print_tree(tree, level):
            if len(tree) == 0:
                return

            for vertex in tree:
                    composite_name = vertex
                    bullet_point = '<li><a href="{0}>{0}</a></li>'.format(composite_name)
                    rval.append(bullet_point)
                    # Parent, so need to create a sub <ul>
                    if len(tree[vertex]) > 0:
                        rval.append('<ul>')
                        print_tree(tree[vertex], level+1)
                        rval.append('</ul>')

        walkable_tree = {}

        for composite_name_full_path, composite_file in self.get_composite_files(dataset=dataset).iteritems():
            paths = composite_name_full_path.split('/')
            # Prepare the tree from to perform a Depth First Search
            create_tree(paths, walkable_tree)

        # Perform a Depth First Search to print all the directory and files properly
        print_tree(walkable_tree, 0)

        # rval.append('<li><a href="%s">%s</a>%s' % (composite_name, composite_name, opt_text))
        rval.append('</ul></html>')
        return "\n".join(rval)

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek = "Track Hub structure: Visualization in UCSC Track Hub"
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
