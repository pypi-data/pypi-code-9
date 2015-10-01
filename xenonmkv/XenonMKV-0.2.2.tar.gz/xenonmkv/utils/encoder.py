import os

from xenonmkv.utils.process_handler import ProcessHandler


class AACEncoder():
    file_path = ""
    log = args = None
    encoder = ""

    def __init__(self, file_path, log, args):
        self.file_path = file_path
        self.log = log
        self.args = args

    def detect_encoder(self):
        # New encoders can be added here when necessary
        self.encoder = "aac"

    def encode(self):
        if not self.encoder:
            self.detect_encoder()

        prev_dir = os.getcwd()
        os.chdir(self.args.scratch_dir)

        # Based on the encoder, perform the appropriate operation
        # so self.encoder = aac will call self.encode_aac()
        getattr(self, "encode_%s" % self.encoder)()

        os.chdir(prev_dir)

        self.log.debug("Encoding to AAC audio file complete")

    def encode_faac(self):
        # Start encoding
        self.log.debug("Using ffmpeg to encode AAC audio file")

        if self.args.resume_previous and os.path.isfile("audiodump.aac"):
            self.log.debug("audiodump.aac already exists in scratch "
                           "directory; cancelling encode")
            return True

        cmd = ["ffmpeg",
               "-i", os.path.join(self.file_path, "audiodump.wav"),
               '-acodec', 'aac',
               '-strict', 'experimental',
               '-b:a', '192k',
               os.path.join(self.file_path, 'audiodump.aac')]
        ph = ProcessHandler(self.args, self.log)

        return ph.start_output(cmd)
