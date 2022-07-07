import re
import os
import click
import zipfile
import logging
import hashlib
import sys
import unicodedata
import mutator_manager
from mutators import *
from urllib import parse


@click.command()
@click.option('--target', type=click.STRING, required=True, help='마크다운 export zip파일 디렉토리')
@click.option('--config', type=click.STRING, required=False, help='설정파일 경로', default="config/default.conf")
@click.option('--outdir', type=click.STRING, required=False, help='출력파일 위치', default="output")
def main(target, config, outdir):
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(stream = sys.stdout, format = Log_Format, level = logging.INFO)
    logger = logging.getLogger()
    if not os.path.exists(target):
        logger.error("target file not exists", target)
        exit(-1)
    #extract zipfile
    md_zip = zipfile.ZipFile(target)
    if md_zip.testzip() != None:
        logger.error("error openning zip file", target)
    base_name=''
    data = ''
    files = dict()
    for name in md_zip.namelist():
        if name.endswith('.md'):
            base_name = re.search("(.*)[a-f0-9]{32}.md", name).group(1)
            base_name = unicodedata.normalize('NFC', base_name).strip().replace(' ', '_')
            data=md_zip.read(name)

    path = os.path.abspath(outdir + "/" + base_name)
    os.makedirs(path, exist_ok=True)
    img_path = os.path.abspath(path + "/img")
    os.makedirs(img_path, exist_ok=True)

    #adding images and some potential files into img directory
    file_count = 0
    for name in md_zip.namelist():
        if not name.endswith(".md"):
            content = md_zip.read(name)
            _, ext = os.path.splitext(name)
            hash_name = base_name + "_attatchment_%02d"%file_count + ext
            target_path = os.path.abspath(img_path + "/" + hash_name)
            files[parse.quote(name)] = hash_name
            with open(target_path, "wb+") as f:
                f.write(content)
            file_count += 1

    #initailize mutators
    mut_manager = mutator_manager.Mutator_manager(config, files)
    #generate mediawiki data
    res = mut_manager.mutate_all(data.decode())
    out_path = os.path.abspath(path + "/" + base_name + ".txt")
    with open(out_path, "wb+") as f:
            f.write(res.encode())

    #cleanup
    md_zip.close()
    return 0

if __name__ == '__main__':
    main()