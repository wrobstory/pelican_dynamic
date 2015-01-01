# -*- coding: utf-8 -*-
"""
Embedded JS and CSS for Pelican
================================

This plugin allows you to easily embed JS and CSS in the header of individual
articles. It also allows for single-tag embedding of D3.js.
"""
import os
import shutil

from pelican import signals

def format_resource(gen, metastring, formatter):
    """
    Create a list of URL-formatted script/style tags

    Parameters
    ----------
    gen: generator
        Pelican Generator
    metastring: string
        metadata['scripts'] or metadata['styles']
    formatter: string
        String format for output.

    Output
    ------
    List of formatted strings
    """
    metalist = metastring.replace(" ", "").split(',')
    site_url = gen.settings['SITEURL']
    return [formatter.format(site_url, x) for x in metalist]

def copy_resources(src, dest, file_list):
    """
    Copy files from content folder to output folder

    Parameters
    ----------
    src: string
        Content folder path
    dest: string,
        Output folder path
    file_list: list
        List of files to be transferred

    Output
    ------
    Copies files from content to output
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
    for file_ in file_list:
        file_src = os.path.join(src, file_)
        shutil.copy2(file_src, dest)

def add_tags(gen, metadata):
    """
        The registered handler for the dynamic resources plugin. It will
        add the scripts and/or styles to the article
    """
    if 'scripts' in metadata.keys():
        script = '<script src="{0}/js/{1}"></script>'
        metadata['scripts'] = format_resource(gen, metadata['scripts'], script)

    if 'styles' in metadata.keys():
        style = '<link rel="stylesheet" href="{0}/css/{1}" type="text/css" />'
        metadata['styles'] = format_resource(gen, metadata['styles'], style)

    if 'd3' in metadata.keys():
        d3_script = '<script src="http://d3js.org/d3.v3.min.js"></script>'
        metadata['scripts'].insert(0, d3_script)

def move_resources(gen):
    """
    Move files from js/css folders to output folder
    """
    js_files = gen.get_files('js', extensions='js')
    css_files = gen.get_files('css', extensions='css')

    js_dest = os.path.join(gen.output_path, 'js')
    copy_resources(gen.path, js_dest, js_files)

    css_dest = os.path.join(gen.output_path, 'css')
    copy_resources(gen.path, css_dest, css_files)


def register():
    """
        Plugin registration
    """
    signals.article_generator_context.connect(add_tags)
    signals.page_generator_context.connect(add_tags)
    signals.article_generator_finalized.connect(move_resources)
