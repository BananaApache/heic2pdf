
# import sys
# sys.path.append("/usr/local/lib/python3.10/site-packages")
from PIL import Image
import glob
import os
import subprocess
import shutil


def convert(inp, outp, quality=90, rec=False, verbose=False):
    ''' Converts images from HEIC to JPG.
    Args:
        inp: Input file/directory.
        outp: Output file/directory.
        quality: JPG quality in [0, 100]. Default is 90.
        rec: If True, subdirectories are parsed recursively, else
            they are copied.
        verbose: Verbosity. Default = False.
    '''
    if os.path.isfile(inp):
        pre, ext = os.path.splitext(inp)
        if ext.lower() in ['.heic', '.heif']:
            if outp is None:
                outp = pre + '.jpg'
            else:
                assert not os.path.isdir(
                    outp), "Both inp and outp should be files"
                pre, ext = os.path.splitext(outp)
                assert ext.lower() in ['.jpg']
                dirname = os.path.dirname(outp)
            subprocess.call(
                'heif-convert -q {} "{}" "{}"'.format(quality, inp, outp), shell=True)
        else:
            outp = inp if outp is None else outp
            shutil.copy2(src=inp, dst=outp, follow_symlinks=True)

    elif os.path.isdir(inp):
        if outp is None:
            outp = inp
        for name in os.listdir(inp):
            inpath = os.path.join(inp, name)
            outpath = os.path.join(outp, name)
            if os.path.isfile(inpath):
                pre, ext = os.path.splitext(name)
                outpath = os.path.join(
                    outp, pre + '.jpg') if ext.lower() in ['.heic', '.heif'] else outpath
                convert(inpath, outpath, quality, rec, verbose)
            elif os.path.isdir(inpath) and rec:
                convert(inpath, outpath, quality, rec, verbose)
            elif os.path.isdir(inpath) and not rec:
                shutil.copytree(src=inpath, dst=outpath, symlinks=True,
                                ignore_dangling_symlinks=True)


if __name__ == '__main__':

    home_folder = os.path.expanduser('~')

    list_of_files = glob.glob(f'{home_folder}/Downloads/*')
    latest_file = max(list_of_files, key=os.path.getctime)

    convert(inp=latest_file,
            outp=f"{latest_file}.jpg")

    list_of_files = glob.glob(f'{home_folder}/Downloads/*')
    latest_file = max(list_of_files, key=os.path.getctime)

    image_1 = Image.open(latest_file)
    im_1 = image_1.convert('RGB')
    im_1=im_1.rotate(270, expand=True)
    im_1.save(f'{latest_file}.pdf')
