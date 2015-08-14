from mock import MagicMock, call


def test_links_between_h4_and_h5_tasks(te, std_te_tasks, dry_run_key):
    te.create_link = MagicMock()
    te.create_tasks(std_te_tasks)
    assert te.create_link.call_args_list == [
        call(dry_run_key, dry_run_key),
        call(dry_run_key, dry_run_key),
        call(dry_run_key, dry_run_key)]


def test_load_inward_link(te, dry_run_key):
    input_text = """
h5. h5 task *assignee* %2015-07-11% <JIRA-1234|Gantt-dependency>
=line1 description"""

    expected_result = [{
        'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
        'line_number': 2, 'description': 'line1 description',
        'duedate': '2015-07-11', 'link': 'JIRA-1234|Gantt-dependency'}]
    assert expected_result == te.load(input_text)

    te.create_link = MagicMock()
    te.create_tasks(expected_result)
    assert te.links == [{'inward': 'JIRA-1234', 'type': 'Gantt-dependency',
                         'outward': dry_run_key}]
    te.create_link.assert_called_once_with('JIRA-1234',
                                           dry_run_key,
                                           'Gantt-dependency')


def test_load_outward_link(te, dry_run_key):
    input_text = """
h5. h5 task *assignee* %2015-07-11% <Gantt-dependency|JIRA-1234>
=line1 description"""

    expected_result = [{
        'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
        'line_number': 2, 'description': 'line1 description',
        'duedate': '2015-07-11', 'link': 'Gantt-dependency|JIRA-1234'}]
    assert expected_result == te.load(input_text)

    te.create_link = MagicMock()
    te.create_tasks(expected_result)
    assert te.links == [{'inward': dry_run_key, 'type': 'Gantt-dependency',
                         'outward': 'JIRA-1234'}]
    te.create_link.assert_called_once_with(dry_run_key,
                                           'JIRA-1234',
                                           'Gantt-dependency')


def test_load_default_type_link(te, dry_run_key):
    input_text = """
h5. h5 task *assignee* %2015-07-11% <JIRA-1234>
=line1 description"""

    expected_result = [{
        'assignee': 'assignee', 'markup': 'h5.', 'summary': 'h5 task',
        'line_number': 2, 'description': 'line1 description',
        'duedate': '2015-07-11', 'link': 'JIRA-1234'}]
    assert expected_result == te.load(input_text)

    te.create_link = MagicMock()
    te.create_tasks(expected_result)
    assert te.links == [{'inward': dry_run_key, 'type': 'Inclusion',
                         'outward': 'JIRA-1234'}]
    te.create_link.assert_called_once_with(dry_run_key,
                                           'JIRA-1234',
                                           'Inclusion')


def test_link_with_rt_var(te, dry_run_key):
    input_json = [{'assignee': 'assignee', 'markup': 'h5.',
                   'summary': 'h5 task1', 'rt_ext': 'LINK'},
                  {'assignee': 'assignee', 'markup': 'h5.',
                   'summary': 'h5 task2', 'line_number': 2,
                   'description': 'line1 description', 'link': '$LINK'}]

    te.create_link = MagicMock()
    te.create_tasks(input_json)
    assert te.links == [{'inward': dry_run_key, 'type': 'Inclusion',
                         'outward': '$LINK'}]
    te.create_link.assert_called_once_with(dry_run_key,
                                           dry_run_key,
                                           'Inclusion')
