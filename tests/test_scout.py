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


def test_profile_scoring_uses_skill_evidence_and_resume_only():
    from scoring import build_profile_text, compute_dynamic_match
    text = build_profile_text('Python', 'Built data pipelines')
    assert compute_dynamic_match(['Python','AI Engineer Intern'], text)[1:] == (['Python'], ['AI Engineer Intern'])


def test_job_rendering_escapes_markup_and_rejects_active_links():
    from rendering import render_job_card, safe_careers_url
    job = {'company':'<script>alert(1)</script>', 'title':'A & B', 'location':'<img src=x>', 'requirements':['<b>Python</b>']}
    html = render_job_card(job, 0, [])
    assert '<script>' not in html and '<img ' not in html and '<b>' not in html
    assert '&lt;script&gt;' in html and 'A &amp; B' in html
    for link in ['javascript:alert(1)', 'data:text/html,x', 'https://user:pass@example.com', 'https://example.com/\nscript', '//example.com']:
        assert safe_careers_url(link) is None
    assert safe_careers_url('https://example.com/careers') == 'https://example.com/careers'


def test_txt_upload_is_repeatable_decodes_bom_and_restores_cursor():
    from io import BytesIO
    from resume import extract_resume_text
    upload = BytesIO(b'\xef\xbb\xbfPython and SQL')
    upload.name = 'resume.TXT'
    upload.seek(4)
    assert extract_resume_text(upload) == 'Python and SQL'
    assert upload.tell() == 4
    assert extract_resume_text(upload) == 'Python and SQL'


def test_upload_rejects_unsupported_empty_or_oversized_files():
    import pytest
    from io import BytesIO
    from resume import extract_resume_text, MAX_UPLOAD_BYTES
    for name, data in [('cv.exe', b'bytes'), ('cv.txt', b''), ('cv.txt', b'x' * (MAX_UPLOAD_BYTES + 1)), ('cv.txt', b'\xff')]:
        upload = BytesIO(data)
        upload.name = name
        with pytest.raises(ValueError):
            extract_resume_text(upload)


def test_pdf_pages_keep_word_boundaries_and_report_unreadable_content(monkeypatch):
    import pytest
    import pypdf
    from io import BytesIO
    from types import SimpleNamespace
    from resume import extract_resume_text
    upload = BytesIO(b'pdf placeholder')
    upload.name = 'cv.pdf'
    pages = [SimpleNamespace(extract_text=lambda: 'Python'), SimpleNamespace(extract_text=lambda: 'SQL')]
    monkeypatch.setattr(pypdf, 'PdfReader', lambda stream: SimpleNamespace(is_encrypted=False, pages=pages))
    assert extract_resume_text(upload) == 'Python\nSQL'
    monkeypatch.setattr(pypdf, 'PdfReader', lambda stream: SimpleNamespace(is_encrypted=True))
    with pytest.raises(ValueError, match='unencrypted'):
        extract_resume_text(upload)
    monkeypatch.setattr(pypdf, 'PdfReader', lambda stream: SimpleNamespace(is_encrypted=False, pages=[]))
    with pytest.raises(ValueError, match='No text'):
        extract_resume_text(upload)


def test_demo_resume_requires_explicit_opt_in():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file('../app.py').run()
    assert app.checkbox(key='use_sample_resume').value is False
    assert not any('Demo Resume (' in item.value for item in app.markdown)
    app.checkbox(key='use_sample_resume').check().run()
    assert not app.exception
    assert any('Demo Resume (' in item.value for item in app.markdown)
