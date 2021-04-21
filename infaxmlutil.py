#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Invoke the infa xml utils functions to perform some tasks such as:
* Find all nodes that match a pattern and export it to a specific format
It's implemented as click commands
'''
# standart 
import os, sys
# third party 
import click
# custom 
from infa.format import find_from_file, list_of_components

@click.group()
def cli():
	pass

@cli.command(name='export')
@click.argument('file_name', type=click.Path(exists=True), nargs=-1)
@click.option('-fr', '--from', 'parent', default=None, help='Parent element to retrieve (optional)')
@click.option('-e', '--extract', default='workflows', help='Component to export', show_default=True)
@click.option('-c', '--config', default=None, help='Configuration file to get components (YAML, optional)', type=click.File('rb'))
@click.option('-f', '--format', default='excel', type=click.Choice(['text', 'csv', 'excel']), help='Format for output file', show_default=True)
@click.option('-o', '--output', default=None, help='Output file name (optional)', type=click.File('wb'))
@click.option('-l', '--list', default=False, is_flag=True, help='List the available components to export')
def export_it(file_name, parent, extract, config, format, output, list):
	'''Find all instances from a given component from the specified exported Infa XML file'''
	if list:
		list_of_components(config)
		return
	if len(file_name)==0:
		click.echo('Notice: No file(s) provided, no files generated. Please verify')
		sys.exit(1)
	for file in file_name:
		click.echo(f'Processing {file}:')
		find_from_file(filename=file, comp=extract, parent=parent, conf=config, format=format, target=output)

if __name__ == '__main__':
	cli()
