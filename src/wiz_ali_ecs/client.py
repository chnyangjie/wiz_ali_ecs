import json
import logging
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstanceAutoRenewAttributeRequest import \
    DescribeInstanceAutoRenewAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


class AliEcsClient(object):

    def __init__(self, access_key_id, access_key, region):
        self.access_key_id = access_key_id
        self.access_key = access_key
        self.region = region

    def __enter__(self):
        self.client = AcsClient(self.access_key_id, self.access_key, self.region)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def query_ecs_renew_status(self, instance_id_list: list):
        instance_list = []
        instance_id_group_list = []
        for group in range(0, len(instance_id_list), 100):
            instance_id_group_list.append(instance_id_list[group:group + 100])
        for group in instance_id_group_list:
            request = DescribeInstanceAutoRenewAttributeRequest()
            request.set_InstanceId(",".join(group))
            response = self.client.do_action_with_exception(request).decode()
            response = json.loads(response)
            instance_list += response['InstanceRenewAttributes']['InstanceRenewAttribute']
        return instance_list

    def query_ecs_instance_list(self):
        logging.info("query for instance list")
        instance_list = []
        page = 0
        size = 100
        total = sys.maxsize

        while page * size < total:
            page += 1
            request = DescribeInstancesRequest()
            logging.debug("request for ecs|| page: %s| size: %s| total: %s", page, size, total)
            request.set_PageNumber(page)
            request.set_PageSize(size)
            response = self.client.do_action_with_exception(request).decode()
            response = json.loads(response)
            total = response['TotalCount']
            instances = response['Instances']['Instance']
            instance_list += instances
        logging.info("get ecs instance list done|| len: %s", len(instance_list))
        return instance_list
