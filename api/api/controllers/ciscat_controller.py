# Copyright (C) 2015-2019, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import asyncio
import logging
from typing import List

import wazuh.ciscat as ciscat
from wazuh.cluster.dapi.dapi import DistributedAPI
from ..util import remove_nones_to_dict, parse_api_param

loop = asyncio.get_event_loop()
logger = logging.getLogger('wazuh')


def get_agents_cistat_results(agent_id: str, pretty: bool = False, wait_for_complete: bool = False, 
                              offset: int = 0, limit: int = None, select: List[str] = None, 
                              sort: str = None, search: str = None, benchmark: str = None, 
                              profile: str = None, passed: int = None, fail: int = None,
                              error: int = None, notchecked: int = None, 
                              unknown: int = None, score: int = None):
    """Get CIS-CAT results from an agent

    Returns the agent's ciscat results info.

    :param agent_id: Agent ID. All posible values since 000 onwards.
    :param pretty: Show results in human-readable format 
    :param wait_for_complete: Disable timeout response
    :param offset: First element to return in the collection
    :param limit: Maximum number of elements to return
    :param select: Select which fields to return (separated by comma)
    :param sort: Sorts the collection by a field or fields (separated by comma). Use +/- at the beginning to list in ascending or descending order. 
    :param search: Looks for elements with the specified string
    :param benchmark: Filters by benchmark type.
    :param profile: Filters by evaluated profile.
    :param passed: Filters by passed checks
    :param fail: Filters by failed checks
    :param error: Filters by encountered errors
    :param notchecked: Filters by not checked
    :param unknown: Filters by unknown results.
    :param score: Filters by final score
    """
    f_kwargs = {'offset': offset,
                'limit': limit,
                'sort': parse_api_param(sort, 'sort'),
                'search': parse_api_param(search, 'search'),
                'select': select,
                'agent_id': agent_id,
                'filters': {
                    'benchmark': benchmark,
                    'profile': profile,
                    'pass': passed,
                    'fail': fail,
                    'error': error,
                    'notchecked': notchecked,
                    'unknown': unknown,
                    'score': score
                }
            }

    dapi = DistributedAPI(f=ciscat.get_results_agent,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='distributed_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          pretty=pretty,
                          logger=logger
                          )
    data = loop.run_until_complete(dapi.distribute_function())

    return data, 200