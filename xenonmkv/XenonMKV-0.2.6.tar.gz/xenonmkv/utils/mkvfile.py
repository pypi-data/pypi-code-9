import os
import subprocess
import traceback

from process_handler import ProcessHandler


class MKVFile:
    def __init__(self, args, log):
        self.options = args
        self.options.tracks = {}
        self.video_id = self.audio_id = 0
        self.logger = log

    def get_mkvinfo(self):
        args = ['ffprobe', '-show_streams', self.options.source_file]
        self.logger.debug("Executing '{0}'".format(' '.join(args)))
        try:
            proc = subprocess.Popen(args, shell=False, bufsize=0, close_fds=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
            result, errs = proc.communicate()
        except subprocess.CalledProcessError:
            self.logger.debug("ffprobe process error: {0}".format(traceback.format_exc()))
            raise Exception("Error occurred while obtaining MKV information "
                            "for {0} - please make sure the file exists, is readable and "
                            "a valid MKV file".format(self.options.source_file))

        self.logger.debug("mediainfo finished; attempting to parse output")
        try:
            self.parse_mediainfo(result)
        except:
            # Punt back exception from inner function to the main application
            raise Exception("Do not parse ffprobe result.")

    # Parse the output from mediainfo for the file.
    def parse_mediainfo(self, lines):
        self.logger.debug("Started to parse the output from ffprobe for the file.")
        result = self.format_lines(lines)
        audio = self.select_audio(result)
        self.parse_groups(result, audio)
        self.logger.debug("Finished to parse the output from ffprobe for the file.")

    def format_lines(self, lines):
        self.logger.debug("Started to format tracks")
        # Parse groups and remove last tilde separator character
        result = {}
        prefix = 'video_'

        for line in lines.split(os.linesep):
            if not line.strip():
                continue
            if line.startswith('index='):
                index = line[6:]
                if index != '0':
                    prefix = 'audio{index}_'.format(index=index)
                result['{prefix}index'.format(prefix=prefix)] = index
                continue

            row = '{prefix}{key}'.format(prefix=prefix, key=line)
            try:
                key, value = row.split('=')
                result[key] = value
            except:
                pass
        self.logger.debug("Finished that format to tracks")
        return result

    def parse_groups(self, lines, audio):
        self.logger.debug("Started to parse tracks")
        tmp = {}
        for line in lines:
            if line.split('_')[0] == 'video':
                tmp[line] = lines.get(line)
            elif line.split('_')[0] == audio:
                key = 'audio_' + '_'.join(line.split('_')[1:])
                tmp[key] = lines.get(line)

        self.options.tracks = tmp
        self.logger.debug("Finished that parse to track")

    def select_audio(self, lines):
        channels = 0
        audio = ''

        for line in lines:
            if line.startswith('audio') and line.endswith('_channels'):
                tmp = int(lines[line].split(' ')[0])
                if tmp > channels:
                    channels = tmp
                    audio = line.split('_')[0]

        if channels < self.options.channels:
            self.options.channels = channels

        self.logger.debug('Select audio channels: {channels}'
                          .format(channels=str(self.options.channels)))
        return audio

    def extract_mkv(self):
        self.logger.debug("Executing mkvextract on '{0}'".format(self.options.source_file))
        os.chdir(self.options.scratch_dir)

        if self.options.scratch_dir != ".":
            self.logger.debug("Using {0} as scratch directory for "
                              "MKV extraction".format(self.options.scratch_dir))

        try:
            temp_video_file = "temp_video.{extension}".format(
                extension=self.options.tracks.get('video_codec_name'))
            self.logger.debug("Detected video extension: {extension}".format(
                extension=self.options.tracks.get('video_codec_name')))

            temp_audio_file = "temp_audio.{extension}".format(
                extension=self.options.tracks.get('audio_codec_name'))
            self.logger.debug("Detected audio extension: {extension}".format(
                extension=self.options.tracks.get('audio_codec_name')))
        except UnsupportedCodecError:
            # Send back to main application
            raise

        if (os.path.isfile(temp_video_file) and
                os.path.isfile(temp_audio_file)):
            self.logger.debug("Temporary video and audio files already exist; "
                              "cancelling extract")
            temp_video_file = os.path.join(self.options.scratch_dir, temp_video_file)
            temp_audio_file = os.path.join(self.options.scratch_dir, temp_audio_file)
            return temp_video_file, temp_audio_file

        # Remove any existing files with the same names
        if os.path.isfile(temp_video_file):
            self.logger.debug("Deleting temporary video file {0}".format(
                os.path.join(self.options.scratch_dir, temp_video_file)))
            os.unlink(temp_video_file)
        if os.path.isfile(temp_audio_file):
            self.logger.debug("Deleting temporary audio file {0}".format(
                os.path.join(self.options.scratch_dir, temp_audio_file)))
            os.unlink(temp_audio_file)

        for circle in range(2):
            self.video_id = int(self.options.tracks.get('video_index')) + circle
            self.audio_id = int(self.options.tracks.get('audio_index')) + circle

            self.logger.debug("Using video track from MKV file with ID {0} "
                              .format(str(self.video_id)))
            self.logger.debug("Using audio track from MKV file with ID {0} "
                              .format(str(self.audio_id)))

            video_output = str(self.video_id) + ":" + temp_video_file
            audio_output = str(self.audio_id) + ":" + temp_audio_file

            cmd = ['mkvextract', "tracks",
                   self.options.source_file, video_output, audio_output]
            ph = ProcessHandler(self.options, self.logger)
            process = ph.start_output(cmd)

            if process == 0:
                break

            if process != 0 and circle == 1:
                raise Exception("An error occurred while extracting tracks from {0}"
                                " - please make sure this file exists and is readable"
                                .format(self.options.source_file))

        temp_video_file = os.path.join(self.options.scratch_dir, temp_video_file)
        temp_audio_file = os.path.join(self.options.scratch_dir, temp_audio_file)

        self.logger.debug("mkvextract finished; attempting to parse output")

        if not temp_video_file or not temp_audio_file:
            raise Exception("Audio or video file missing from "
                            "mkvextract output")

        return temp_video_file, temp_audio_file


class UnsupportedCodecError(Exception):
    pass
