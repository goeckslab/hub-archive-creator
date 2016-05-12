Conversion of NCBI BLAST+ tblastn results to PSL format
=======================================================
Wilson Leung <wleung@wustl.edu>

Last Update: 04/24/2016


Version information
-------------------
* Kent source tree: v324
* NCBI BLAST+: BLAST 2.2.30+

Data sources
-------------------
For testing purposes, the database consists of only contig1 in the Dbia3 assembly while the protein sequences correspond to the three isoforms of the *D. melanogaster* *ci* gene in contig1. The protein sequences are available through [FlyBase](http://flybase.org/cgi-bin/getseq.html?source=dmel&id=FBgn0004859&chr=4&dump=PrecompiledFasta&targetset=translation).

* Dbia3.fa = contig1 sequence in the Dbia3 asssembly
* ci.pep = Protein sequences for the three isoforms of the *ci* gene in *D. melanogaster*

Conversion protocol
-----------------------
1. Create BLAST database for the assembly
```
makeblastdb -in Dbia3.fa -dbtype nucl
```

2. Perform tblastn search and output results in XML format
```
tblastn -outfmt 5 -db Dbia3.fa -query ci.pep -out tblastn_Dbia3_ci.xml -evalue 1e-2
```

3. Convert results into PSL format
```
blastXmlToPsl -convertToNucCoords tblastn_Dbia3_ci.xml tblastn_Dbia3_ci.xml.psl
```

4. Convert PSL output into BED format
```
pslToBed tblastn_Dbia3_ci.xml.psl tblastn_Dbia3_ci.xml.bed
```

Output files
-----------------------
* tblastn_Dbia3_ci.xml = tblastn results in XML format
* tblastn_Dbia3_ci.xml.psl = tblastn results in PSL format
* tblastn_Dbia3_ci.xml.bed = tblastn results in BED format


