How to test HubArchiveCreator?
==============================

The Galaxy tool HubArchiveCreator, which is currently mandatory for G-OnRamp,
can go through unit testing, and has been developed with TDD (Test Driven Development)
method.

Unfortunately, the UCSC Track Hub testing part has not yet been implemented. Thus, the UCSC Track Hub
<=> G-OnRamp connection needs currently to be manually tested.

Let's proceed to the documentation of how to test the HubArchiveCreator tool:

1. HubArchiveCreator is a Galaxy tool
-------------------------------------

HubArchiveCreator has been designed to work in conjunction with `Galaxy <https://galaxyproject.org/>`_.
Even though you could use it within the command line, it will be difficult due to the required metadata
(if you want take a look at the
`json required input <https://github.com/remimarenco/hub-archive-creator/blob/master/hubArchiveCreator.xml#L47-L146>`_.

Knowing that, Galaxy has been really good at helping developers to integrate their tools into the platform.
You can check the `full documentation <https://wiki.galaxyproject.org/>`_, the `tool development documentation
<https://wiki.galaxyproject.org/Admin/Tools>`_, and the
`test documentation <https://wiki.galaxyproject.org/Admin/Tools/WritingTests>`_.

On top of that, the team has developed a tool called `Planemo <https://planemo.readthedocs.io/en/latest/>`_, which
helps the tool developers **even more**.

2. Planemo to facilitate TDD (and more)
---------------------------------------

As a Galaxy tool developer, Planemo helps us to develop faster with an increased software quality.

For this section, we are going to be interested in the testing part. To get a sense of how it works, please follow `this
link <https://planemo.readthedocs.io/en/latest/writing_standalone.html>`_ to learn how to build a tool and test it with
Planemo.

Once you are done, you will be able to understand the following:

  1. HubArchiveCreator follows the testing Planemo guidelines:

    - Use `Test Driven Development <https://en.wikipedia.org/wiki/Test-driven_development>`_
    - The tests are located in the `Tool Definition File <https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial#A3._Create_Tool_Definition_File>`_.
      You can find this file `here <https://github.com/remimarenco/hub-archive-creator/blob/master/hubArchiveCreator.xml#L326>`_

  2. hubArchiveCreator has its own test-data structure we are going to see below
  3. hubArchiveCreator uses the simple :code:`planemo test` command to generate the tests

3. HubArchiveCreator testing workflow
-------------------------------------

**Requirements**:

  - Python 2.7
  - Planemo (`pip install planemo` or any other package management supporting it)
  - HubArchiveCreator (`git clone`)

As a developer, you are invited to test your code as much as you can. It has a slight cost upfront, but save you big
overtime.

The workflow in HubArchiveCreator follows TDD guidelines when implementing a new feature:

1. Write the test (find below the explanation)
***********************************************

Example:
++++++++

.. code-block:: xml

  <!-- Test with only the fasta file -->
  <test>
      <param name="genome_name" value="Dbia3"/>
      <param name="fasta_file" value="common/dbia3.fa"/>
      <output name="output" file="only_genome/only_genome.html">
          <extra_files type="file" name="__main__.log" value="only_genome/__main__.log" />
          <extra_files type="file" name="myHub/genomes.txt" value="only_genome/myHub/genomes.txt" />
          <extra_files type="file" name="myHub/Dbia3.html" value="only_genome/myHub/Dbia3.html"/>
          <!-- Email could be different, but we need to ensure we still have the email line -->
          <extra_files type="file" name="myHub/hub.txt" value="only_genome/myHub/hub.txt" lines_diff="2">
              <assert_contents>
                  <has_text text="email"/>
              </assert_contents>
          </extra_files>
          <extra_files type="file" name="myHub/Dbia3/Dbia3.2bit" value="common/Dbia3.2bit">
          </extra_files>
          <extra_files type="file" name="myHub/Dbia3/description.html" value="only_genome/myHub/Dbia3/description.html"/>
      </output>
  </test>

Explanation:
++++++++++++

<test> Markup:
``````````````

.. code-block:: xml

  <!-- Test with only the fasta file -->
  <test>
      ...
  </test>

This piece of code uses a comment first (`<!-- Content -->`) to explain the type of test,
**then** opens the `test` XML markup to tell Galaxy/Planemo the content is a test.

Follow the `tool syntax documentation <https://docs.galaxyproject.org/en/latest/dev/schema.html#tool-tests-test>`_
for more details.

<param> Markup:
```````````````

.. code-block:: xml

  <param name="genome_name" value="Dbia3"/>
  <param name="fasta_file" value="common/dbia3.fa"/>

This piece of code use the `param` XML markup to tell Galaxy/Planemo to use these two files as input for our tool.

`name` matches the name of the associated input parameter in the tool definition file. For us, **genome_name** can
be found `here <https://github.com/remimarenco/hub-archive-creator/blob/master/hubArchiveCreator.xml#L162-L168>`_:

.. code-block:: xml

  <param
        name="genome_name"
        type="text"
        size="30"
        value="unknown"
        label="UCSC Genome Browser assembly ID"
  />

`value` matches one of the legal values that can be assigned to this very input parameter. For `genome_name`, we
can see it is a type `text` (look again above). So we have assigned to it a simple string `Dbia3`.

4. G-OnRamp <=> UCSC Track Hub: Manual part
-------------------------------------------

