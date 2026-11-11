from streamlit.testing.v1 import AppTest
import jobs
def test_verdict_denominator_agrees_with_score(monkeypatch):
    monkeypatch.setattr(jobs, 'fetch_vetted_jobs', lambda _: [{'company':'Example', 'title':'Intern', 'location':'Remote', 'requirements':['Python','python',' '], 'target_link':'https://example.test'}])
    app = AppTest.from_file('../app.py').run()
    app.text_area(key='vault_candidate_skills').set_value('Python')
    app.button(key='btn_deploy_scout').click().run()
    assert not app.exception
    assert any('1 of 1 requirements matched' in item.value for item in app.success)
