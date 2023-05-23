import datetime
import logging
from upload_to_container import UploadToContainer

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    upload_instance = UploadToContainer()

    lf = upload_instance.load_forecasts()
    
    logging.info(lf)