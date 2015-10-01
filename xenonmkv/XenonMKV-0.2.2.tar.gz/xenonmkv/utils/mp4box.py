import os

from xenonmkv.utils.process_handler import ProcessHandler


class MP4Box():
    video_path = audio_path = video_fps = video_pixel_ar = ""

    args = log = None

    def __init__(self, video_path, audio_path, video_fps,
                 args, log):
        self.video_path = video_path
        self.audio_path = audio_path
        self.video_fps = str(video_fps)
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

        cmd = [self.args.tool_paths["mp4box"], self.args.name + ".mp4",
               # Always create new file with mp4box/GPAC
               "-add", self.video_path, "-fps", self.video_fps,
               "-add", self.audio_path, "-tmp", self.args.scratch_dir,
               "-new",
               "-itags", "name=" + self.args.name.split('/')[:1] + ".mp4"]

        ph = ProcessHandler(self.args, self.log)
        process = ph.start_output(cmd)

        if process != 0:
            # Destroy temporary file
            # so it does not have multiple tracks imported
            os.unlink(output_file)
            self.log.warning("An error occurred while creating "
                             "an MP4 file with MP4Box")
            # Continue retrying to create the file

        self.log.debug("MP4Box process complete")

        # When complete, change back to original directory
        os.chdir(prev_dir)
