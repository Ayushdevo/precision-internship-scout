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


def test_every_sample_explicitly_reports_unverified_demo_provenance():
    assert all(job['source_type'] == 'demo' and job['verified'] is False for job in fetch_vetted_jobs(''))


def test_dashboard_renders_search_results_including_empty_state():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file('../app.py', default_timeout=20).run()
    app.text_input(key='search_keyword').set_value('unobtainium')
    app.button(key='btn_deploy_scout').click().run()
    assert not app.exception
    assert any('No sample listings' in item.value for item in app.info)
    assert not any('job-card-title' in item.value and 'Google DeepMind' in item.value for item in app.markdown)


def test_scoring_uses_case_insensitive_skill_boundaries_and_unique_requirements():
    from scoring import compute_dynamic_match
    _, matched, missing = compute_dynamic_match(['Python','SQL','C++','R','Python',' '], 'PYTHON, NoSQL, C++, Docker')
    assert matched == ['Python','C++']
    assert missing == ['SQL','R']


def test_scores_report_actual_overlap_without_an_artificial_floor():
    from scoring import compute_dynamic_match
    assert compute_dynamic_match(['Python','SQL'], 'Python')[0] == 50
    assert compute_dynamic_match(['Python'], 'Docker')[0] == 0
    assert compute_dynamic_match(['Python'], '')[0] == 0
    assert compute_dynamic_match([], 'Python')[0] == 0
    assert compute_dynamic_match(['Python'], 'Python')[0] == 100
