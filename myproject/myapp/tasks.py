from celery.decorators import task

from collections import OrderedDict
import ffmpy

@task
def add(x, y):
	print str(x) + str(y) + "******************************************************************************"

@task
def tax():
	for i in range(1000):
		print i

@task
def merge(img, audio, new_file_name):
	ff = ffmpy.FFmpeg(
	    global_options='-loop 1',
	    inputs=OrderedDict([(img, None), (audio, None)]),
	    outputs={new_file_name: '-c:v libx264 -c:a aac -shortest'}
	)
	ff.run()