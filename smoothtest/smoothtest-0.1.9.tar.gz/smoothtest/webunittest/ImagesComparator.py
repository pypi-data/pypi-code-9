# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import subprocess
import logging
from smoothtest.base import SmoothTestBase
from PIL import Image
import tempfile
import shutil
import os


class ImagesComparator(SmoothTestBase):
    def exec_cmd(self, cmd):
        '''
        Exec a shell command. Returns its stdout output
        Command's return value must be 0.
        :param cmd: command line as written in OS shell
        '''
        logging.debug('Getting output of: %r' % cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        assert not p.returncode, 'Command %r failed output: %s err: %s' % (cmd, out, err)
        return out

    def create_diff(self, ref_img, new_img, diff, crop_threshold=100):
        '''
        Creates images difference using Imagemagick 'compare' command
        http://www.imagemagick.org/Usage/compare/
        It highlights differences.
        
        Since 'compare' command does not accept images of different sizes, 
        this method will crop to the smallest common area of the two.
        
        If such area differs from the original one too much, we simply raise an 
        exception, since difference image won't make any sense.
        
        :param ref_img: path to the reference image. (correct one)
        :param new_img: path to the current image. (new one)
        :param diff: path to the difference image to create.
        :param crop_threshold:
        '''
        if not (0 <= crop_threshold <= 100):
            raise ValueError('crop_threshold outside range: 0 <= crop_threshold <= 100.')
        atempdir = btempdir = None
        # Open images to compare image sizes
        aimg = Image.open(ref_img)
        bimg = Image.open(new_img)
        if aimg.size != bimg.size:
            # Raise exception if we don't tolerate cropping
            if crop_threshold == 100:
                raise ValueError('crop_threshold is 100 and images are from different sizes.')
            # Calculate smaller common size
            w,h = min((aimg.size[0], bimg.size[0])), min((aimg.size[1], bimg.size[1]))
            # Make sure we are within the crop threshold
            wratio = w/float(aimg.size[0])*100
            hratio = h/float(aimg.size[1])*100
            if wratio < crop_threshold or hratio < crop_threshold:
                raise ValueError('Cropping ratios %r are smaller than '
                                 'crop_threshold=%r.' % ((wratio, hratio), crop_threshold))
            # If needed, crop reference image to common size
            if aimg.size != (w,h):
                atempdir = tempfile.mkdtemp()
                ref_img = self.crop_image(atempdir, ref_img, w, h)
            # If needed, crop new image to common size
            if bimg.size != (w,h):
                btempdir = tempfile.mkdtemp()
                new_img =self.crop_image(btempdir, new_img, w, h)
        # Run the image magick command
        self.exec_cmd('compare %s %s %s'%(ref_img,new_img,diff))
        # Remove any created temp dir
        for tempdir in [atempdir, btempdir]:
            if tempdir:
                shutil.rmtree(tempdir)

    def crop_image(self, tempdir, img_file, w, h):
        '''
        Crop image file to w,h size and save it to the temporary dir
        :param tempdir: temporary dir (user should rmtree it later)
        :param img_file: image file to crop
        :param w: new width size
        :param h: new height size
        '''
        new_file = os.path.join(tempdir, os.path.basename(img_file))
        cmd = 'convert {img_file} -crop {w}x{h}+0+0  +repage {new_file}'.format(**locals())
        self.exec_cmd(cmd)
        return new_file

    def compare(self, ref_img, new_img, treshold=100):
        '''
        Compare two images using the 'findimagedupes' command.
        Return true if both images match.
        :param ref_img: path to the reference image. (correct one)
        :param new_img: path to the current image. (new one)
        :param treshold: threshold value in percent to tolerate in comparison
        '''
        command = 'findimagedupes -t=%s %s %s' % (treshold, ref_img, new_img)
        return bool(self.exec_cmd(command))


def smoke_test_module():
    ic = ImagesComparator()
    this_dir = os.path.dirname(__file__)
    a_file = os.path.join(this_dir, 'tests/img/street.jpg') 
    b_file = os.path.join(this_dir, 'tests/img/street_diff.jpg')
    diff = os.path.join(this_dir, 'tests/img/diff.jpg')
    assert ic.compare(a_file, b_file, treshold=100) == False
    assert ic.compare(a_file, b_file, treshold=50) == True
    ic.create_diff(a_file, b_file, diff, crop_threshold=100)


if __name__ == "__main__":
    smoke_test_module()
