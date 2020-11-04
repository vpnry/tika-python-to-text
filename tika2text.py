
"""
Information:
=============
It will convert all kind of docs in a directory (including all sub dirs)
to txt, including metadata and keeping the input document directory.
It uses tika-python to do the convert task https://github.com/chrismattmann/tika-python
The output txt files is then used for full text search index etc.

Requirements:
=============
Java: sudo apt install openjdk-11-jdk-headless
python3: sudo apt install python3
Tika-python: pip3 install tika

Instructions:
=============
Tika python need tika-server every time it runs offline (see tika-python on Github).

  Download tika-server-x???.jar, tika-server-x??.jar.md5 from the Internet, and rename them to tika-server.jar, tika-server.jar.md5

  And move to /tmp/ tika-server.jar tika-server.jar.md5. After that run this env configure:

  export TIKA_SERVER_JAR="file:////tika-server.jar"
  export PYTHONIOENCODING=utf8

  Then run this:
  python3 tika2text.py

"""


# Based on Stackoverflow answers
# https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python/328389

import os
import time
import tika
# tika.initVM()
from tika import parser




def mkPaths(file_path):
  # Modified https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-dir
  dir = os.path.dirname(file_path)
  if not os.path.exists(dir):
    os.makedirs(dir)

def lsFiles(dir, extStr):
    """
    Modified https://stackoverflow.com/a/21281918
    @extStr = 'html, htm' or '*' to list all
    Return: ['full','file','path']
    """

    matches =[]
    if (not dir.endswith('/')):
      dir = dir + "/"
    extStr = extStr.strip(' ,') 
    lis = extStr.split(',')
    tupleExt = tuple([i.strip() for i in lis])
    print ('Listing files end with: '+ str(tupleExt))
    for root, dirs, files in os.walk(dir):
        for file in files:
            if (extStr == "*" ):
              matches.append(os.path.join(root, file))
            else:
              if file.endswith(tupleExt):
                matches.append(os.path.join(root, file))
    print('Finished listing, total files: ' + str(len(matches)))
    return matches

def tika2text(inDir, outDir, frExt, toExt = ".txt", fixBrokenLine = False):

  """
  inDir: Input doc directory
  outDir: Output doc directory
  frExt: Filter input file 'html, htm' or '*' to list all
  toExt: Save converted text in this file extention
  fixBrokenLine = False/True Try to fix  broken lines in some html files (experimental function)
  """


  i = 0
  if (not inDir.endswith('/')):
    inDir = inDir + "/"
  if (not outDir.endswith('/')):
    outDir = outDir + "/"
  if (not toExt.startswith('.')):
    toExt = '.' + toExt

  mkPaths(outDir)
  files = lsFiles(inDir,frExt)
  print('')
  print('----- Tika Convert Files to TXT -----------')
  print('Input dir: \033[0;31m'+ inDir +'\033[0m')
  print('Input file total: \033[0;32m' + str(len(files)) +'\033[0m files.')
  print('Output dir: \033[0;32m'+ outDir +'\033[0m')
  print('-----------------------------------------')
  print('Processing...')
  for url in files:
    # parsed = parser.from_file(url, xmlContent=True)
    parsed = parser.from_file(url)

    metadata = str(parsed["metadata"])
    content = str(parsed["content"])

    if (fixBrokenLine):
      content = re.sub(r'\n+','150815',content)
      content = re.sub(r'\.150815',r'.\n',content)
      content = re.sub(r'([\s]*150815[\s]*){1,}',r' ',content) # multi 150815 to one space
    
    newpath = url.replace(inDir, outDir, 1)
    mkPaths(newpath)

    with open(newpath + "_meta_" + toExt, 'w') as f:
      f.write(metadata)
    with open(newpath + toExt, 'w') as fc:
      fc.write(content)
    
    i = i + 1
    print(str(i) +'. Converted: ' + url)

    # # You can limit how many files to be converted here
    # limitFile = 10
    # if(i == limitFile):
    #   break

  print('')
  print('-----------------------------------------')
  print('Input file total: \033[0;32m' + str(len(files)) + '\033[0m files.')
  print('\033[0;32mDone\033[0m, processes total: \033[0;32m' + str(i) + '\033[0m files.')
  print('Process time: '+ str(time.process_time()) + ' seconds')
  print('-----------------------------------------')





tika2text("pSearchLib", "pSearchLib_txt","*","txt", False)
