import pytest
from os.path import join, exists
from ideskeleton import builder, ideprocesses as ide

@pytest.fixture(scope='session')
def solution_builder(tmpdir_factory):
    basic = tmpdir_factory.mktemp('solution_builder')
    git_file = basic.join(".gitignore")
   
    git_file.write_text(u".git/\n" +
                     "#this is a comment\n" + 
                     "\n" +
                     "*.sln\n" + 
                     "[Dd]ebug/\n", 'ascii')
    basic.join(".travis.yml").write("")
    basic.join("LICENSE").write("")
    basic.join("README.md").write("")
    basic.join("requirements.txt").write("")
    ideskeleton = basic.mkdir("ideskeleton")
    test = basic.mkdir("tests")
    data = test.mkdir("data")
    ideskeleton.join("builder.py").write("")
    ideskeleton.join("__init__.py").write("")
    ideskeleton.join("__main__.py").write("")
    test.join("test_builder.py").write("")
    test.join("__init__.py").write("")
    data.join("ideskeleton_pyproj.xml").write("")
    data.join("ideskeleton_sln.txt").write("")
    data.join("tests_pyproj.xml").write("")

    builder.build(str(basic),ide = "vstudio")

    return basic

def test_none_read_it_just_returns_the_input_within_a_list():
    actual = ide.none_read(0,".",["dir1"],["file"])

    assert actual == [(0,".",["dir1"],["file"])]

def test_none_write_returns_input_ignoring_path():
    actual = ide.none_write([],"C:/projects")

    assert actual == []

def test_parse_path_at_first_level_returns_last_folder_name():
    container, relative = ide.parse_path(0, "C:/Projects/MySolution")

    assert (container, relative) == ("MySolution", "")

def test_parse_path_at_second_level_returns_last_folder_as_project_name():
    container, relative = ide.parse_path(1, "C:/Projects/MySolution/MyProject")

    assert (container, relative) == ("MyProject", "")

@pytest.mark.parametrize("level,path,expected", [
    (2, "C:/Projects/MySolution/MyProject/Folder1", ("MyProject", join("Folder1",""))),
    (2, "./MySolution/MyProject/Folder1", ("MyProject", join("Folder1",""))),
    (3, "./MySolution/MyProject/Folder1/Folder2", ("MyProject", join("Folder1","Folder2",""))),
    (4, "./MySolution/MyProject/Folder1/Folder2/Folder3", ("MyProject", join("Folder1","Folder2","Folder3","")))
])
def test_parse_path_at_higher_levels_returns_project_name_and_relative_path_to_it(level,path,expected):
    container, relative = ide.parse_path(level, path)
    assert (container, relative) == expected

def test_arrange_actions_into_structure_groups_actions_to_files_and_action_type():
    actions = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_CONTAINER, "MySolution.sln", "Proj1.pyproj"),
        (ide.ADD_CONTAINER, "MySolution.sln", "Proj2.pyproj"),
        (ide.ADD_COMPILE, "MySolution.sln","file1.py"),
        (ide.ADD_CONTENT, "MySolution.sln","file2.txt"),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2","")),
        (ide.ADD_FOLDER, "Proj2.pyproj", join("sub_dir3","")),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_CONTENT, "Proj1.pyproj", "sub_file2.txt"),
        (ide.ADD_CONTENT, "Proj2.pyproj", "sub_file3.txt")
        ]

    expected = {
        "MySolution.sln" : {
            "identifier": ide.build_uuid("MySolution.sln"),
            ide.ADD_COMPILE : [
                "file1.py"
                ],
            ide.ADD_CONTENT : [
                "file2.txt"
                ],
            "projects" : [
                "Proj1.pyproj",
                "Proj2.pyproj"
                ]
            },
        "Proj1.pyproj" : {
            "identifier": ide.build_uuid("Proj1.pyproj"),
            ide.ADD_FOLDER: [
                join("sub_dir1",""),
                join("sub_dir2","")
                ],
            ide.ADD_COMPILE: [
                "sub_file1.py"
                ],
            ide.ADD_CONTENT: [
                "sub_file2.txt"
                ]
            },
        "Proj2.pyproj" : {
            "identifier": ide.build_uuid("Proj2.pyproj"),
            ide.ADD_FOLDER: [
                join("sub_dir3","")
                ],
            ide.ADD_COMPILE: [
                ],
            ide.ADD_CONTENT: [
                "sub_file3.txt"
                ]
            }
        }

    assert ide.arrange_actions_into_structure(actions) == expected

def test_vstudio_read_a_solution_is_created_at_level_zero_for_relative_paths():
    actual =  ide.vstudio_read(0,".", [],[])
    assert actual[0] == (ide.ADD_CONTAINER, None, "ideskeleton.sln")

def test_vstudio_read_a_solution_is_created_at_level_zero_for_absolute_paths():
    actual = ide.vstudio_read(0,"C:/Projects/MySolution",[],[])
    assert actual[0] == (ide.ADD_CONTAINER, None, "MySolution.sln")

def test_vstudio_read_files_at_the_first_level_are_added_as_solution_files():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", [], ["file1.py", "file2.txt"])
    expected = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_COMPILE, "MySolution.sln","file1.py"),
        (ide.ADD_CONTENT, "MySolution.sln","file2.txt")
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_first_level_are_added_as_solution_projects():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", ["dir1","dir2"], [])
    expected = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_CONTAINER, "MySolution.sln", "dir1.pyproj"),
        (ide.ADD_CONTAINER, "MySolution.sln", "dir2.pyproj")
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_second_level_are_added_as_project_folders_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2",""))
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_second_level_are_added_as_project_folders_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Proj1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2",""))
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_are_added_as_project_items_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Proj1", [], ["sub_file1.py","sub_file2.py"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file2.py")
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_are_added_as_project_items_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", [], ["sub_file1.py","sub_file2.py"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file2.py")
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_distinguises_compilable_from_content_files():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", [], ["sub_file1.py","sub_file2.txt"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_CONTENT, "Proj1.pyproj", "sub_file2.txt")
        ]
    assert actual == expected

def test_vstudio_read_files_at_a_higher_than_second_level_are_added_as_project_items_considering_relative_path_from_project_path():
    actual = ide.vstudio_read(2, "./MySolution/Proj1/Dir1", [], ["sub_file1.py","sub_file2.txt"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", join("Dir1","sub_file1.py")),
        (ide.ADD_CONTENT, "Proj1.pyproj", join("Dir1","sub_file2.txt"))
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_a_higher_than_second_level_are_added_as_project_folders_considering_relative_path_from_project_path():
    actual = ide.vstudio_read(2, "C:/Projects/MySolution/Proj1/Dir1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("Dir1","sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("Dir1","sub_dir2",""))
        ]
    assert actual == expected

def test_vstudio_write_solution_and_project_files_are_created(solution_builder):
    solution = str(solution_builder.join("solution_builder0.sln"))
    ideskeleton = str(solution_builder.join("ideskeleton").join("ideskeleton.pyproj"))
    tests = str(solution_builder.join("tests").join("tests.pyproj"))
    
    assert all(map(exists, [solution, ideskeleton, tests]))

def test_vstudio_write_solution_file_content_is_correct(solution_builder):
    # Due to Linux/Windows different treatment of directory separators comparing
    # the exact written output is not feasible, so just some weak probabilistic tests are done.
    solution = str(solution_builder.join("solution_builder0.sln"))

    with open(solution,"r") as file:
        text = file.read()

        assert all([
            ".gitignore = .gitignore" in text,
            "Project(\"{888888A0-9F3D-457C-B088-3A5042F75D52}\") = \"ideskeleton\"" in text,
            "Project(\"{888888A0-9F3D-457C-B088-3A5042F75D52}\") = \"tests\"" in text,
            "Project(\"{2150E333-8FDC-42A3-9474-1A3956D46DE8}\") = \"Solution Items\"" in text
            ])

def test_vstudio_write_project_file_content_is_correct(solution_builder):
    # Due to Linux/Windows different treatment of directory separators comparing
    # the exact written output is not feasible, so just some weak probabilistic tests are done.
    tests = str(solution_builder.join("tests").join("tests.pyproj"))

    with open(tests, "r") as file:
        text = file.read()

        assert all([
            "<ProjectGuid>{FFFE5AC8-6AB7-53F7-8C22-07C267C567CC}</ProjectGuid>" in text,
            "<Compile Include=\"test_builder.py\" />" in text,
            "<Folder Include=\"{}\" />".format(join("data","")) in text,
            "<Content Include=\"{}\" />".format(join("data","ideskeleton_pyproj.xml")) in text
            ])


