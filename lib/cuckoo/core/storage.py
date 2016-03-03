import boto
import logging
import os

from lib.cuckoo.common.config import Config
from lib.cuckoo.common.constants import CUCKOO_ROOT

log = logging.getLogger(__name__)

def storeResultsAWS(analysis_id):
    cfg = Config()
    folder = os.path.abspath( os.path.join( CUCKOO_ROOT, "storage", "analyses", str(analysis_id) ))

    for (srcDir, dirName, filename) in os.walk(folder):
        for fname in filename:
            sourcepath = os.path.join(srcDir, fname)
            aws_filename = sourcepath.split("analyses/")[1]

            try:
                s3 = boto.s3.connect_to_region("us-east-1")
                log.info("Connected to S3")
                log.info("AWS Bucket {}".format(cfg.cuckoo.aws_bucket))
                bucket = s3.get_bucket(cfg.cuckoo.aws_bucket)
                log.debug("Connected to the bucket")
                key = bucket.new_key("%s" % (aws_filename))
                log.info("New key created for filename: %s" % (aws_filename))
                key.set_contents_from_filename(sourcepath)
                log.debug("Set file contents")
                key.set_acl("authenticated-read")
                if key.storage_class != "REDUCED_REDUNDANCY":
                    key.change_storage_class("REDUCED_REDUNDANCY")

            except Exception as ex:
                log.warn("[x] storeResultsAWS: %s" % ex)

