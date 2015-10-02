import pytest
import ideskeleton as skeleton
from ideskeleton import builder
import os
import types

@pytest.fixture(scope='session')
def basic_structure(tmpdir_factory):
    basic = tmpdir_factory.mktemp('basic_structure')
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
      
    return basic

def test_build_can_be_called_from_skeleton_package():
    assert type(skeleton.build) == types.FunctionType

def test_build_if_source_path_does_not_exist_error(tmpdir):
    not_existing = os.path.join(tmpdir.dirname, "not_existing")
    with pytest.raises(IOError):
        builder.build(not_existing)

def test_build_if_gitignore_not_found_error(tmpdir):
    with pytest.raises(IOError):
        builder.build(tmpdir.dirname)

def test_read_gitignore_returns_valid_patterns(tmpdir):
    local = tmpdir.mkdir("test_read_gitignore").join(".gitignore")
    local.write_text(u".git/\n" +
                     "#this is a comment\n" + 
                     "\n" +
                     "*.sln\n" + 
                     "[Dd]ebug/\n", 'ascii')
    
    patterns = builder.read_gitignore(local.dirname)
    
    assert patterns == [".git/", "*.sln", "[Dd]ebug/"]

@pytest.mark.parametrize("input,expected", [
    (".git/", True),
    ("sln", False),
    ("debug/", True),
    ("myname.sln", True),
    ("C:\path\myname.sln", True)
])
def test_is_ignored_check_if_patterns_are_satisfied(input, expected):
    patterns = [".git/", "*.sln", "[Dd]ebug/"]

    assert builder.is_ignored(input, patterns) == expected

def test_remove_ignored_modify_input_list_of_files_in_place():
    patterns = [".git/", "*.sln", "[Dd]ebug/"]
    files = [".git", "C:\path\myname.sln", "code.py"]

    builder.remove_ignored(files, patterns)

    assert files == [".git", "code.py"]

def test_remove_ignored_modify_input_list_of_dirs_in_place():
    patterns = [".git/", "*.sln", "[Dd]ebug/"]

    dirs = [".git", "ideskeleton","debug"]
    builder.remove_ignored(dirs, patterns, True)

    assert dirs == ["ideskeleton"]

def test_traverse_executes_the_process_function_per_folder_in_structure(basic_structure):
    base_dir = str(basic_structure)
    expected = [(0, base_dir,['ideskeleton', 'tests'],['.gitignore', '.travis.yml', 'LICENSE', 'README.md', 'requirements.txt']),
                (1, os.path.join(base_dir,"ideskeleton"), [], ['builder.py', '__init__.py', '__main__.py']),
                (1, os.path.join(base_dir,"tests"), ['data'], ['test_builder.py', '__init__.py']),
                (2, os.path.join(base_dir,"tests","data"),[],['ideskeleton_pyproj.xml', 'ideskeleton_sln.txt', 'tests_pyproj.xml'])]

    process = lambda level, root, dirs, files: [(level, root, dirs, files)]

    actual = builder.traverse(str(basic_structure),process)

    assert expected == actual

def test_build_with_none_processing_returns_the_os_walk_result(basic_structure):
    base_dir = str(basic_structure)
    expected = [(0, base_dir,['ideskeleton', 'tests'],['.gitignore', '.travis.yml', 'LICENSE', 'README.md', 'requirements.txt']),
                (1, os.path.join(base_dir,"ideskeleton"), [], ['builder.py', '__init__.py', '__main__.py']),
                (1, os.path.join(base_dir,"tests"), ['data'], ['test_builder.py', '__init__.py']),
                (2, os.path.join(base_dir,"tests","data"),[],['ideskeleton_pyproj.xml', 'ideskeleton_sln.txt', 'tests_pyproj.xml'])]


    actual = builder.build(base_dir)

    assert actual == expected

if __name__ == "__main__":
    pytest.main()

