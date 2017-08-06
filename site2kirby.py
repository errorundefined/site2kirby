#!/usr/bin/env python

import os

from html2kirby import HTML2Kirby

inputdir = os.getcwd()
basename = os.path.basename(inputdir)
outputdir = '../' + basename + '-kirby'

i = 0

# make outputfolder for converted files
if not os.path.exists(outputdir):
    os.makedirs(outputdir)

for root, dirs, filenames in os.walk(inputdir):

    # clone directory structure to outputfolder
    subfolder = os.path.join(outputdir, root[len(inputdir):])
    if not os.path.exists(subfolder):
        os.makedirs(outputdir + subfolder, exist_ok=True)

    # convert and write txt-files to outputfolder structure
    for filename in [f for f in filenames if (f.endswith('.html')) or (f.endswith('.htm')) ]:

        i += 1

        if root.lstrip(inputdir):
            subdir = '/' + root.lstrip(inputdir) + '/'
        else:
            subdir = '/'

        filewithpath = os.path.join(root, filename)

        file = open(filewithpath, 'r')
        markup = file.read()
        file.close()

        # call html2kirby
        formatter = HTML2Kirby()
        formatter.feed(markup)

        file_name, file_extension = os.path.splitext(filename)
        
        file = open(outputdir + subdir + file_name + '.txt', 'w')
        file.write(formatter.kirbytext)
        file.close()

# remove empty directories from outputfolder
for root, dirs, filenames in os.walk(outputdir):
        for dirname in dirs:
            dir_name = os.path.join(root, dirname)
            if not os.listdir(dir_name):
                os.removedirs(dir_name)

print()
print('==> ', str(i), 'files converted to Kirby Markdown.')
print('[Converted files were created in: ', outputdir, ']')
print()