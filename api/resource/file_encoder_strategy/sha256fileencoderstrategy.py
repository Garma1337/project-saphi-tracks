# coding: utf-8

import hashlib
import time

from werkzeug.utils import secure_filename

from api.resource.file_encoder_strategy.fileencoderstrategy import FileEncoderStrategy, EncodedResourceTarget


class Sha256FileEncoderStrategy(FileEncoderStrategy):

    def encode_file_name(self, file_name: str) -> EncodedResourceTarget:
        current_ts = self.get_current_timestamp()
        encoded_file_name = secure_filename(f'{current_ts}_{file_name}')

        hash_value = str(hashlib.sha256(encoded_file_name.encode()).hexdigest())
        base_directory = f'{hash_value[0]}{hash_value[1]}/{hash_value[2]}{hash_value[3]}/{hash_value[4]}{hash_value[5]}'

        return EncodedResourceTarget(encoded_file_name, base_directory)

    def get_current_timestamp(self) -> int:
        return int(time.time())
