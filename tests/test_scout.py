from jobs import fetch_vetted_jobs


def test_job_source_is_directly_callable_without_an_mcp_tool_wrapper():
    assert callable(fetch_vetted_jobs)
    assert len(fetch_vetted_jobs('')) == 3
