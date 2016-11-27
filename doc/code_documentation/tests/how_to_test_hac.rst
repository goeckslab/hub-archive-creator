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

3. G-OnRamp <=> UCSC Track Hub: Manual part
-------------------------------------------

