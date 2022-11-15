#!/usr/bin/env python
import requests
from argparse import ArgumentParser
from dnacentersdk import api
from dnacentersdk.exceptions import ApiError
import logging
import csv
import sys
import json
from  time import sleep, time, strftime, localtime
from task import Task, TaskTimeoutError, TaskError
from dnac_config import DNAC, DNAC_USER, DNAC_PASSWORD
logger = logging.getLogger(__name__)

def format_time(secs):
    fmt = "%Y-%m-%d %H:%M:%S"
    timestr = strftime(fmt,localtime(secs))
    return timestr

def map_site_name_to_id(dnac, sitename):
    logger.debug("looking up site:{}".format(sitename))
    try:
        response = dnac.sites.get_site(name=sitename)
    except ApiError:
        print("cannot find site: {}".format(sitename))
        sys.exit(1)

    if (len(response.response)) != 1:
        print("multiple matches found, taking the first")
    logger.debug(response.response)
    return response.response[0].id


def sync_site(dnac, siteid, timeout):
    task = dnac.custom_caller.call_api(method="POST", resource_path="/api/v1/dna-maps-service/cmx/{}/map/export".format(siteid))
    logger.debug(task)
    try:
        t = Task(dnac, task.response.taskId)
        result = t.wait_for_task(timeout=timeout)
        logger.debug(result)
        elapsed = int((result.response.endTime - result.response.startTime)/ 1000)
        if result.response.progress == "Error":
            message = result.response.failureReason
        else:
            message = result.response.progress
        print("Task completed:{} - elapsed time:{}sec".format(message, elapsed))
    except TaskTimeoutError as e:
        print(e)

def main(dnac, sitename,timeout=100):
    siteid = map_site_name_to_id(dnac,sitename)
    sync_site(dnac, siteid, timeout)

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    parser.add_argument('--sitename',  type=str, required=True,
                        help='site to sync')
    parser.add_argument('--timeout',  type=int,
                        help='timeout in seconds')
    args = parser.parse_args()

    if args.v:
        root_logger=logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
        logger.debug("logging enabled")
#    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    dnac = api.DNACenterAPI(base_url='https://{}:443'.format(DNAC),
                                #username=DNAC_USER,password=DNAC_PASSWORD,verify=False,debug=True)
                                username=DNAC_USER,password=DNAC_PASSWORD,verify=False)

    main(dnac, args.sitename, args.timeout)
