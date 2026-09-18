from jobs import fetch_vetted_jobs


def test_job_source_is_directly_callable_without_an_mcp_tool_wrapper():
    assert callable(fetch_vetted_jobs)
    assert len(fetch_vetted_jobs('')) == 3


def test_search_trims_keywords_and_preserves_empty_results():
    assert fetch_vetted_jobs('  PyThOn  ') == fetch_vetted_jobs('Python')
    assert fetch_vetted_jobs('unobtainium') == []


def test_search_results_do_not_share_mutable_requirement_lists():
    first = fetch_vetted_jobs('')
    first[0]['requirements'].append('Mutation')
    assert 'Mutation' not in fetch_vetted_jobs('')[0]['requirements']
