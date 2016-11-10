Datatype.py: A datatype to rule them all
========================================

For UCSC Track Hub to work properly, a datatype usually needs a lot of informations,
like the reference genome for example.
You can find the list of the UCSC Track Hub supported datatypes here:
https://genome.ucsc.edu/goldenpath/help/hgTrackHubHelp.html#Setup

We made a generic class *Datatype* to gather the common needs. Please find below this class.

[TODO] Attach a link to the tutorial to create a new datatype.

.. warning:: This class should never be instantiated as is, but inherited!

.. autoclass:: Datatype.Datatype
   :members:
   :undoc-members:
