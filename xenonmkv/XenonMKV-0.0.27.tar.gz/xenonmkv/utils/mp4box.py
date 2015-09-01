import os

from xenonmkv.utils.process_handler import ProcessHandler


class MP4Box():
    video_path = audio_path = video_fps = video_pixel_ar = ""

    args = log = None

    def __init__(self, video_path, audio_path, video_fps,
                 video_pixel_ar, args, log):
        self.video_path = video_path
        self.audio_path = audio_path
        self.video_fps = str(video_fps)
        self.video_pixel_ar = video_pixel_ar
        self.args = args
        self.log = log

    def package(self):
        prev_dir = os.getcwd()
        os.chdir(self.args.scratch_dir)

        # Make sure there is no 'output.mp4' in the scratch directory
        # MP4Box has a tendency to add tracks
        output_file = os.path.join(os.getcwd(), self.args.name + ".mp4")
        if os.path.isfile(output_file):
            os.unlink(output_file)

        cmd = ["ffmpeg", "-i", self.audio_path,
               "-i", self.video_path,
               "-codec", "copy",
               "-fflags", "+genpts",
               "-absf", "aac_adtstoasc",
               self.args.name + ".mp4"]

        ph = ProcessHandler(self.args, self.log)
        process = ph.start_output(cmd)

        if process != 0:
            # Destroy temporary file
            # so it does not have multiple tracks imported
            os.unlink(output_file)
            self.log.warning("An error occurred while creating "
                             "an MP4 file with ffmpeg")
            # Continue retrying to create the file

        self.log.debug("ffmpeg process complete")

        # When complete, change back to original directory
        os.chdir(prev_dir)
