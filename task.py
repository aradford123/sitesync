from  time import sleep, time
import logging
logger = logging.getLogger(__name__)

class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass



class Task:
    def __init__(self,dnac, taskid):
        self.dnac = dnac
        self.taskid = taskid
        logger.debug("created task for id:{}".format(taskid))
    def wait_for_task(self, timeout=10,retry=1):
        start_time = time()
        first = True
        while True:
            result = self.dnac.task.get_task_by_id(self.taskid)

            if result.response.endTime is not None:
                return result
            else:
                # print a message the first time throu
                if first:
                    logger.debug("Task:{} not complete, waiting {} seconds, polling {}".format(self.taskid, timeout, retry))
                    first = False
                if timeout and (start_time + timeout < time()):
                    raise TaskTimeoutError("Task %s did not complete within the specified timeout "
                                           "(%s seconds)" % (self.taskid, timeout))

                logging.debug("Task=%s has not completed yet. Sleeping %s seconds..." % (self.taskid, retry))
                sleep(retry)
            if result.response.isError == "True":
                raise TaskError("Task {} had error {}".format(self.taskid, result.response.progress))
        return response

