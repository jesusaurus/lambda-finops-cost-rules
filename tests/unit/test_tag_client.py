import cost_rules.tag_client
from .fixtures.account_list import *
from .fixtures.code_tags import *
from .fixtures.owner_tags import *
from .fixtures.tag_names import *

import boto3
from botocore.stub import Stubber


def test_account_tags():
    '''Test getting account code mapping from account tags'''
    # stub organizations client
    org = boto3.client('organizations')
    cost_rules.tag_client.org_client = org
    with Stubber(org) as _stub:
            # inject mock account response
            _stub.add_response('list_accounts', mock_account_list)

            # inject a mock tags response for each mock account

            # we are using two owners for three accounts to ensure
            # that accounts are properly grouped
            _stub.add_response('list_tags_for_resource', mock_resource_owner_tags_foo1)
            _stub.add_response('list_tags_for_resource', mock_resource_owner_tags_bar)
            _stub.add_response('list_tags_for_resource', mock_resource_owner_tags_foo2)

            # assert owners were collected
            found_account_owners = cost_rules.tag_client.collect_account_tags(expected_tag_list)
            assert found_account_owners == expected_account_owners


def test_account_tags_regex():
    '''Test getting account code mapping from account tags'''
    # stub organizations client
    org = boto3.client('organizations')
    cost_rules.tag_client.org_client = org
    with Stubber(org) as _stub:
            # inject mock account response
            _stub.add_response('list_accounts', mock_account_list)

            # inject a mock tags response for each mock account

            # we are using two codes for three accounts to ensure
            # that accounts are properly grouped under the code
            # found in their respective tags
            _stub.add_response('list_tags_for_resource', mock_resource_code_tags_a)
            _stub.add_response('list_tags_for_resource', mock_resource_code_tags_other)
            _stub.add_response('list_tags_for_resource', mock_resource_code_tags_b)

            # assert codes were collected
            found_account_codes = cost_rules.tag_client.collect_account_tags(expected_tag_list, cost_rules.tag_client.tag_regex)
            assert found_account_codes == expected_account_codes
