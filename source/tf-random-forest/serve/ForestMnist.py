import logging

import os, sys
import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest
from tensorflow.python.ops import resources
import boto3
import subprocess
import time

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)


class ForestMnist(object):
    def __init__(self):
        self.model_name = os.environ.get('MODEL_NAME', '').lower()
        self.model_version = os.environ.get('MODEL_VERSION', '0').lower()

        self.model_name_version = "%s.%s" % (self.model_name, self.model_version)

        self.s3_endpoint_url = os.environ.get('S3_ENDPOINT_URL', '')
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
        self.bucket_name = os.environ.get('BUCKET_NAME', '')
        
        if len(self.model_name) == 0:
            _LOGGER.error("Provide path to saved model in $MODEL_PATH env var")
            sys.exit(1)

        self.prep_model()
            
        tf.reset_default_graph()
        self.sess = tf.Session()
        saver = tf.train.import_meta_graph("model/%s.meta" % (self.model_name_version))
        saver.restore(self.sess,tf.train.latest_checkpoint("model/"))

        graph = tf.get_default_graph()
        self.x = graph.get_tensor_by_name("X:0")
        self.y = graph.get_tensor_by_name("probabilities:0")

    def predict(self, X, feature_names):
        predictions = self.sess.run(self.y, feed_dict={self.x: X})
        return predictions

    def prep_model(self):
        tarball = "%s.tgz" % (self.model_name_version)

        conn = boto3.client(service_name='s3', endpoint_url=self.s3_endpoint_url)
        conn.download_file(Bucket=self.bucket_name, Key=tarball, Filename=tarball)
        _LOGGER.info("Downloaded model to %s" % tarball)
        if subprocess.call(["tar", "--no-overwrite-dir", "-xzf", tarball]) != 0:
            _LOGGER.error("Failed to unpack %s" % tarball)
            time.sleep(10000)
            raise Exception
        
        _LOGGER.info("Unpacked the model")
