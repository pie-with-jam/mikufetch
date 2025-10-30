from mikufetch.info import get_sys_info

def test_sys_info_returns_list():
    info = get_sys_info()
    assert isinstance(info, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in info)
