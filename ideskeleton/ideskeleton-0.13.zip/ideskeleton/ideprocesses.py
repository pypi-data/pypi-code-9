"""Specific functions to process folder structures for distinct IDE's. """
from os.path import abspath, basename, splitext, dirname, join
from uuid import uuid5, UUID

COMPILABLES = set([".py"])

ADD_CONTAINER = "container"
ADD_CONTENT = "content"
ADD_COMPILE = "compile"
ADD_FOLDER = "folders"

PROJ_TYPE = "888888A0-9F3D-457C-B088-3A5042F75D52"
SOL_TYPE = "2150E333-8FDC-42A3-9474-1A3956D46DE8"

def build_uuid(path):
    """Build an uuid from path in upper string format."""
    namespace = UUID("{D4A33062-9785-467D-8179-05177E00F1E2}")
    return str(uuid5(namespace, path)).upper()

def parse_path(level, path):
    """Get project name and relative path to it depending on level."""
    if level > 1:
        proj, rel_path = parse_path(level - 1, dirname(path))
        return proj, join(rel_path, basename(path), "")
    else:
        return basename(path), ""

def none_read(level, root, dirs, files):
    """Just return parameters."""
    return [(level, root, dirs, files)]

def none_write(actions, path, overwrite=False):
    """Just return actions."""
    # pylint: disable=unused-argument
    return actions

def vstudio_read(level, root, dirs, files):
    """Process function for visual studio IDE."""
    next_actions = []

    container, relative_path = parse_path(level, abspath(root))

    if level == 0:
        container += ".sln"
        next_actions.append((ADD_CONTAINER, None, container))
        for itm in dirs:
            next_actions.append((ADD_CONTAINER, container, itm + ".pyproj"))

    if level >= 1:
        container += ".pyproj"
        for itm in dirs:
            next_actions.append(
                (ADD_FOLDER, container, join(relative_path, itm, "")))

    for itm in files:
        extension = splitext(itm)[1]
        if extension in COMPILABLES:
            next_actions.append(
                (ADD_COMPILE, container, join(relative_path, itm)))
        else:
            next_actions.append(
                (ADD_CONTENT, container, join(relative_path, itm)))

    return next_actions

def arrange_actions_into_structure(actions):
    """Group actions and files in a dictionary structure to facilitate further processing."""
    structure = {}
    for action, container, path in actions:

        if action == ADD_CONTAINER:
            if not container:
                structure[path] = {
                    "identifier":build_uuid(path),
                    "compile":[],
                    "content":[],
                    "projects":[]
                    }
            else:
                structure[container]["projects"].append(path)
                structure[path] = {
                    "identifier":build_uuid(path),
                    "folders":[],
                    "compile":[],
                    "content":[]
                    }
        else:
            structure[container][action].append(path)

    return structure

def __process_solution(metadata, structure):
    """Process solution file."""
    lines = []
    lines.extend([
        "Microsoft Visual Studio Solution File, Format Version 12.00",
        "# Visual Studio 14",
        "VisualStudioVersion = 14.0.23107.0",
        "MinimumVisualStudioVersion = 10.0.40219.1"
        ])

    for project in metadata["projects"]:
        proj_name = splitext(project)[0]
        lines.append(
            "Project(\"{{{}}}\") = \"{}\", \"{}\", \"{{{}}}\"".format(
                PROJ_TYPE,
                proj_name,
                join(proj_name, project),
                structure[project]["identifier"]))
        lines.append("EndProject")

    sol_items = "\"Solution Items\""
    lines.extend([
        "Project(\"{{{}}}\") = {}, {}, \"{{{}}}\"".format(
            SOL_TYPE, sol_items, sol_items, metadata["identifier"]),
        "\tProjectSection(SolutionItems) = preProject",
        ])

    for item in metadata[ADD_CONTENT]:
        lines.append("\t\t{} = {}".format(item, item))

    for item in metadata[ADD_COMPILE]:
        lines.append("\t\t{} = {}".format(item, item))

    lines.extend([
        "\tEndProjectSection",
        "EndProject"
        ])

    lines.extend([
        "Global",
        "\tGlobalSection(SolutionConfigurationPlatforms) = preSolution",
        "\t\tDebug|Any CPU = Debug|Any CPU",
        "\t\tRelease|Any CPU = Release|Any CPU",
        "\tEndGlobalSection"
        ])

    if metadata["projects"]:
        lines.append(
            "\tGlobalSection(ProjectConfigurationPlatforms) = postSolution")
        for project in metadata["projects"]:
            identifier = str(structure[project]["identifier"])
            lines.append(
                "\t\t{{{}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU".format(
                    identifier))
            lines.append(
                "\t\t{{{}}}.Release|Any CPU.ActiveCfg = Release|Any CPU".format(
                    identifier))
        lines.append("\tEndGlobalSection")

    lines.extend([
        "\tGlobalSection(SolutionProperties) = preSolution",
        "\t\tHideSolutionNode = FALSE",
        "\tEndGlobalSection",
        "EndGlobal",
        ""
        ])
    return lines

def vstudio_write(actions, path, overwrite=False):
    """Process actions and write required IDE files to disk."""
    structure = arrange_actions_into_structure(actions)

    for file_name, metadata in structure.items():
        name, extension = splitext(file_name)
        lines = []

        if extension == ".sln":
            full_path = join(path, file_name)
            lines = __process_solution(metadata, structure)

        else:
            full_path = join(path, name, file_name)
            identifier = str(metadata["identifier"])
            sch = "\"http://schemas.microsoft.com/developer/msbuild/2003\""
            lines.extend([
                "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
                "<Project ToolsVersion=\"4.0\" xmlns={} DefaultTargets=\"Build\">".format(sch),
                "\t<PropertyGroup>",
                "\t\t<Configuration Condition=\" '$(Configuration)' == '' \">Debug</Configuration>",
                "\t\t<SchemaVersion>2.0</SchemaVersion>",
                "\t\t<ProjectGuid>{{{}}}</ProjectGuid>".format(identifier),
                "\t\t<ProjectHome />",
                "\t\t<StartupFile />",
                "\t\t<SearchPath />",
                "\t\t<WorkingDirectory>../{}</WorkingDirectory>".format(name),
                "\t\t<OutputPath>.</OutputPath>",
                "\t\t<ProjectTypeGuids>{{{}}}</ProjectTypeGuids>".format(PROJ_TYPE),
                "\t\t<LaunchProvider>Standard Python launcher</LaunchProvider>",
                "\t\t<InterpreterId />",
                "\t\t<InterpreterVersion />",
                "\t</PropertyGroup>",
                "\t<PropertyGroup Condition=\"'$(Configuration)' == 'Debug'\" />",
                "\t<PropertyGroup Condition=\"'$(Configuration)' == 'Release'\" />",
                "\t<PropertyGroup>",
                "\t\t<VisualStudioVersion Condition=\" '$(VisualStudioVersion)' == ''" \
                    "\">10.0</VisualStudioVersion>",
                "\t\t<PtvsTargetsFile>$(MSBuildExtensionsPath32)\\Microsoft\\VisualStudio\\v" \
                    "$(VisualStudioVersion)\\Python Tools\\Microsoft.PythonTools.targets" \
                    "</PtvsTargetsFile>",
                "\t</PropertyGroup>"
                ])

            if metadata[ADD_COMPILE]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_COMPILE]:
                    lines.append("\t\t<Compile Include=\"{}\" />".format(item))
                lines.append("\t</ItemGroup>")

            if metadata[ADD_FOLDER]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_FOLDER]:
                    lines.append("\t\t<Folder Include=\"{}\" />".format(item))
                lines.append("\t</ItemGroup>")

            if metadata[ADD_CONTENT]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_CONTENT]:
                    lines.append("\t\t<Content Include=\"{}\" />".format(item))
                lines.append("\t</ItemGroup>")

            lines.extend([
                "\t<Import Project=\"$(PtvsTargetsFile)\" " \
                    "Condition=\"Exists($(PtvsTargetsFile))\" />",
                "\t<Import Project=\"$(MSBuildToolsPath)\\Microsoft.Common.targets\" " \
                "Condition=\"!Exists($(PtvsTargetsFile))\" />",
                "</Project>"
                ])

        mode = "w+" if overwrite else "w"

        with open(full_path, mode) as ide_file:
            ide_file.write("\n".join(lines))


