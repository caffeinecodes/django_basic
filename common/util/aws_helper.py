from __future__ import unicode_literals
from common.config.config import ConfigSectionMap
import boto
from boto.s3.key import Key
import os
import logging    

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def upload_image_and_return_url(id):
    """ Returns S3 image url after uploading the image of the given file name to s3.

    """
    try:
        temp_image_path = ConfigSectionMap('paths')['temp_image_path']
        key = "{0}".format(id)
        fn = "{0}/{1}".format(temp_image_path, id)
        bucket_name = ConfigSectionMap('amazon_s3')['bucket_name']
        image_url = "http://s3.amazonaws.com/{0}/{1}".format(bucket_name, key)

        # connect to the bucket
        conn = boto.connect_s3(ConfigSectionMap('amazon_s3')['access_key_id'],
                        ConfigSectionMap('amazon_s3')['secret_access_key'])
        bucket = conn.get_bucket(bucket_name)
        # create a key to keep track of our file in the storage
        k = Key(bucket)
        k.key = key
        k.set_contents_from_filename(fn)
        # we need to make it public so it can be accessed publicly
        k.make_public()
        # remove the file from the web server
        os.remove(fn)
        log.info("Image url : {0}".format(image_url))
        return image_url
    except Exception, err:
        logging.exception("Error Message {0}".format(err))
        return None


