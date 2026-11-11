from streamlit.testing.v1 import AppTest
def test_whitespace_equivalent_query_preserves_results():
    app = AppTest.from_file('../app.py').run()
    app.text_input(key='search_keyword').set_value('AI Platform')
    app.button(key='btn_deploy_scout').click().run()
    assert any('TechScale AI' in item.value for item in app.markdown)
    app.text_input(key='search_keyword').set_value(' AI   Platform ').run()
    assert not app.exception
    assert any('TechScale AI' in item.value for item in app.markdown)
