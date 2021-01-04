from mock import patch, Mock

from tahoe_lti.processors import basic_user_info, personal_user_info


@patch('tahoe_lti.processors.get_xblock_user')
def test_basic_user_info(mock_get_xblock_user):
    """Happy scenario for test_basic_user_info"""
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    assert basic_user_info(xblock=None) == {
        'lis_person_sourcedid': 'mock_username',
        'lis_person_contact_email_primary': 'mock_email@example.com',
    }
    assert not hasattr(basic_user_info, 'lti_xblock_default_params')


@patch('tahoe_lti.processors.get_xblock_user')
def test_personal_user_info(mock_get_xblock_user):
    """Happy scenario for personal_user_info"""
    assert personal_user_info.lti_xblock_default_params == {
        'lis_person_name_full': '',
        'lis_person_name_given': '',
        'lis_person_name_family': '',
        'custom_user_id': '',
    }
    mock_user = Mock()
    mock_user.profile.name = 'Bob Robot'
    mock_user.id = 20
    mock_get_xblock_user.return_value = mock_user

    info = personal_user_info(xblock=None)
    assert info == {
        'custom_user_id': '20',
        'lis_person_name_full': 'Bob Robot',
        'lis_person_name_given': 'Bob',
        'lis_person_name_family': 'Robot',
    }