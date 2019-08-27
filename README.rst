=====
chibi
=====

this package is for i can put snippets and other useful things
and i do not need to write the same thing for fifth time

*************
cosas utitles
*************

Chibi_path
==========

the chibi path work like strings but with opperators have sense for folders
and files

.. code-block:: python

	import chibi.file import Chibi_path

	p = Chibi_path( '/tmp/folder' )
	isintance( p, str ) == true
	# return a generator with all the files and folders in
	# the path
	p.ls()
	p = p + 'file'
	str( p ) == '/tmp/folder/file'
	f = p.open()
	# check the file for see is containt the string
	'some string' in f

	# write a dict like json in the file
	f.write_json( { 'stuff': 'str' } )
	# read the json and transform the dict in a Chibi_atlas
	json = f.read_json()
	json.stuff == 'str'

	# the dame but in yaml
	f.write_yaml( { 'stuff': 'str' } )
	yaml = f.read_yaml()
	yaml.stuff == 'str'


Chibi_atlas
===========

this is a dict but his keys can be access like attribute

.. code-block:: python

	import chibi.atals import Chibi_atlas


	c = Chibi_atlas( { 'stuff': 'str', 'l': [ 1, { 'more_stuff': 'str_2' } ] } )
	isintance( c, dict ) == true
	c.stuff == 'str'
	c.l[0] == 1
	c.l[1].more_stuff == 'str_2'
