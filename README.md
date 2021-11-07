# infaxmlutil.py

Set of utilities focus on perform a series of operations on exported Infa XML files such as:
* Find components from files and export it into different formats as text (printed to stdout), csv and Excel files.
* [To Do] Generate diagrams of the mappings and workflows within a file.
* [To Do] Compare two files to get relevant differencies among them.
* [To Do] Validate if a file is compliant with a set of defined rules.

All those functionalities are implemented as commands of the `infaxmlutil` module.

At this moment, only the export capability is implemented.

**Table of Contents**

[TOCM]

[TOC]

# Usage

```bash
> python infaxmlutil.py --help
Usage: infaxmlutil.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export  Find all instances from a given component from the specified...
```

It is expected to integrate more commands as they will code.

Each command has its own help page whith its own parameters and options that apply in each case.

# export

## Description

Given a set of defined components, such as workflows, mappings, sessions or many more, find it into a XML file and export the resulting set either to the stdout or to a file in csv or Excel format with the hierarchy associated to the elements found.

The generated files, have the TAG name of all the hierarchy that preced to the nodes to extract as the header for the intended files, apply for csv and Excel format.

## Usage

```bash
> python infaxmlutil.py export --help
Usage: infaxmlutil.py export [OPTIONS] [FILE_NAME]...

  Find all instances from a given component from the specified exported Infa
  XML file

Options:
  -fr, --from TEXT               Parent element to retrieve (optional)
  -e, --extract TEXT             Component to export  [default: workflows]
  -c, --config FILENAME          Configuration file to get components (YAML,
                                 optional)

  -f, --format [text|csv|excel]  Format for output file  [default: excel]
  -o, --output FILENAME          Output file name (optional)
  -l, --list                     List the available components to export
  --help                         Show this message and exit.
```

The above options, are explained with more detail in further sections of this document.

## Options

### Hierarchy

All components, as well as its transformations and properties, are defined inside a XML file. This file is a copy of the information that lies into the Informatica Power Center Repository for a given program at the moment it was exported. Every component are defined as a set of XML properties and other nested tags into the hierarchy defined by the [powrmart.dtd](https://github.com/autodidacticon/informatica-powercenter-automation/blob/master/src/app/config/dtd/powrmart.dtd) file.

Given the fact that all information about components, its properties and relationship with other components are encoded inside this XML file, we can extrac it and generate a report with this information. Moreover, the hierarchy of each component is always the same, in this way the information of all the sources definitions used at mapping level, always will have the same hierarchy.

The details about how to query and display those properties are abstracted into the configuration file used to generate the report of the desired components by assosiating a label with the desired set that holds the information about how to extract it an show it into a report.

Those labels mentioned above, are the used as the `--from` and `--extract` options of the extract command. At the moment, the possible values for those options could be listed by using the `-l` or the `--list` option of the extract command. The list of components available and its associated `--from` and `--extract` options are shown below.

```bash
> python infaxmlutil.py export --list
The list of components defined to extract from exported Infa XML files with its
associated command line options are shown below.
Components:
  sources       --extract sources
  targets       --extract targets
  workflows     --extract workflows
  mappings      --extract mappings
  worklets      --extract worklets
  mapplets      --extract mapplets
  sessions      --extract sessions
  udfs  --extract udfs
  sql-overrides --extract sql-overrides
  connections   --extract connections

The following components are nested by hierachy level and its associated command line
options are shown below.
Nested components:
  sources:
    ports       [--from sources --extract ports] or [--extract sources.ports]
  targets:
    ports       [--from targets --extract ports] or [--extract targets.ports]
  mappings:
    sources     [--from mappings --extract sources] or [--extract mappings.sources]
    targets     [--from mappings --extract targets] or [--extract mappings.targets]
    variables   [--from mappings --extract variables] or [--extract mappings.variables]
    trxs        [--from mappings --extract trxs] or [--extract mappings.trxs]
  mapplets:
    inputs      [--from mapplets --extract inputs] or [--extract mapplets.inputs]
    outputs     [--from mapplets --extract outputs] or [--extract mapplets.outputs]
    trxs        [--from mapplets --extract trxs] or [--extract mapplets.trxs]
  workflows:
    variables   [--from workflows --extract variables] or [--extract workflows.variables]
    components  [--from workflows --extract components] or [--extract workflows.components]
    param-file  [--from workflows --extract param-file] or [--extract workflows.param-file]
  sessions:
    sources     [--from sessions --extract sources] or [--extract sessions.sources]
    targets     [--from sessions --extract targets] or [--extract sessions.targets]
    gral-conns  [--from sessions --extract gral-conns] or [--extract sessions.gral-conns]
    param-file  [--from sessions --extract param-file] or [--extract sessions.param-file]
    log-params  [--from sessions --extract log-params] or [--extract sessions.log-params]
    attrs       [--from sessions --extract attrs] or [--extract sessions.attrs]
    assg        [--from sessions --extract assg] or [--extract sessions.assg]

Tip: You can specify more than one component into the same --extract option by 
separating them by commas.
The option:
  --extract workflows,mappings.sources,mappings.targets
Is equivalent to:
  --extract workflows --extract mappings.sources --extract mappings.targets
Those options will extract all the worflows, sources & targets at mapping level
and, if excel format is selected, put that information into separate tabs of
the generated excel file.
```

As you can see, there are some components where you need to specified both the `--extract` option as well as its correspond `--from` option mainly for those elements that are defined at different levels on the hierarchy on the structure of the XML file. Alternatively, you can specify this hierarchy by putting the component's name for the `--extract` option in the form `parent.component`, which is equivalent to write `--from parent --extract component`.

You can pass multiple components into the same `--extract` option by separate them by commas, in this way the option `--extract component1,component2,component3` is equivalent to `--extract component1 --extract component2 --extract component3`.

### Format

At this moment, you can generate the report in the following formats:

| Format  | File generated |
| ------------ | ------------ |
| text | The report is generated on the screen with the information of all the nodes retrieved  |
| csv | Generates a comma sepparated file with the information of all the nodes retrieved, by default the file generated has the same name as the file processed with .csv extenssion.  |
| excel | Generates an Excel file with the information of all the nodes retrieved, by default the file generated has the same name as the file processed with .xlsx extenssion. If multiple components are specified into the `--extract` option, each given component would be saved into a separated tab. It is not necessary to have MS Excel installed to generate files in this format. |

If not specified, the command will generate Excel files by default.

In all cases, the first column has the information of the hierarchy for each node retrieved.

### Configuration file

As mention earlier, each component is associated to a label that contains the information needed to query and print the desired component. By default, a configuration file is provided, but it can be modified to include more components or to modify the labels to retrieve in each case.

The configuration file is a file in format YAML whith the following structure:

```yaml
components:
   comp1
   comp2
nested:
   parent1:
      comp11
     comp12
   parent2:
      comp21
     comp22
```

The label are grouped into two main categories:
* **components** For components that can be obtained directly from the XML without ambiguety.
* **nested** For components defined to multiple levels in the XML, such as the sources and targets that are defined at FOLDER level as well as at Mapping level, for those components is required to use both `--from` (to specify the parent label) and `--extract` (to query the desired nested component) options.

For simplicity, each label is unique and is associated to a single component to retrieve.

Each label defines the xpath pattern used to retrieve its correspondant component. By default the property `NAME` of each node is used to be retrieved into the report, but this behaviour can be overrided by specifing the desired format for the different tags in the defined hierarchy for a given component.

On its simplest form, each component is defined as a label and a xpath pattern associated, as shown below:

```yaml
   workflows: //FOLDER/WORKFLOW
```

In this example, the label `workflow` is associated to the xpath pattern `//FOLDER/WORKFLOW` and all nodes retrieved from that xpath are printed by using the `NAME` property defined in each level.

But if a level in the hierarchy, including the node itself, does not contains a `NAME` attibute or if a custom label is needed, it could be specified as follows:

```yaml
    sources: 
        xpath: //FOLDER/SOURCE
        format: 
            SOURCE: $DBDNAME.$NAME
```

In this case, the label `source` defines a `xpath` and a `format` property, since a source is described by concatenating their attributes `DBNAME` and `NAME` together.

If additional components are required, it can be defined in a custom config file and then pass to the command by using the `--config` option of this command.

### Examples

The following table, shows how to invoke the command to get a report with the desired components:

| To get ... | Invoke ... | Result |
| ------------ | ------------ | ------------ |
| All workflows in an INFA.xml file | `python infaxmlutil.py export --extract workflows INFA.xml` | An Excel file named INFA.xlsx with all the workflows in the XML file |
| All sources defined at Mapping level | `python infaxmlutil.py export  --from mappings --extract sources INFA.xml` | An Excel file named INFA.xlsx with all the sources defined at mapping level |
| All sources defined at Mapping level | `python infaxmlutil.py export --extract mappings.sources INFA.xml` | An Excel file named INFA.xlsx with all the sources defined at mapping level |
| All sources and targets defined at Mapping level | `python infaxmlutil.py export --extract mappings.sources,mappings.targets INFA.xml` | An Excel file named INFA.xlsx with all the sources and targets defined at mapping level in separated tabs |
| All mappings in csv format | `python infaxmlutil.py export --extract mappings --format csv INFA.xml` | A csv file named INFA.csv with all mappings defined in the XML file |

## Libraries

This command is implemented by using the following libraries:
* [lxml](https://lxml.de/)
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* [pyyaml](https://pypi.org/project/PyYAML/)

Quick reference for using xpath within python [here](https://lxml.de/xpathxslt.html).

# Copyright & License

Copyright (c) 2021, Edgar Merino. MIT License.