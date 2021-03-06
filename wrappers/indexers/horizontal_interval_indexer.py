#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis-rodan
# Program Description:    Job wrappers that allows vis-framework to work in Rodan.
#
# Filename:               vis-rodan/indexers/horizontal_interval_indexer.py
# Purpose:                Wrapper for NoteRest Indexer.
#
# Copyright (C) 2015 DDMAL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

from pandas import DataFrame
from rodan.jobs.base import RodanTask
from vis.analyzers.indexers.interval import HorizontalIntervalIndexer

import logging
logger = logging.getLogger('rodan')

class VRHorizontalIntervalIndexer(RodanTask):

    name = 'Horizontal Interval Indexer'
    author = "Ryan Bannon"
    description = "Generate horizontal indices for given piece of music."
    settings = {
        'title': 'Horizontal interval indexer settings',
        'type': 'object',
        'properties': {
            'Simple or Compound Intervals': {
                'enum': [ 'simple', 'compound' ],
                'type': 'string',
                'default': 'simple',
                'description': 'Choose whether intervals beyond an octave will be reduced (simple) or not (compound).'
            },
            'Interval Quality': { 
                'type': 'boolean',
                'default': False,
                'description': 'Choose whether intervals should include quality or not.'
            },
            'Directed': {
                'type': 'boolean',
                'default': True,
                'description': 'Choose whether intervals should include direction or not. Descending intervals are prefixed with -. Ascending intervals will have no prefix.'
            },
            'Horizontal attach later': {
                'type': 'boolean',
                'default': True,
                'description': 'TO REMOVE! Just know this: dissonance false, n-gram true.'
            }
        }
    }

    enabled = True
    category = "VIS - Indexer"
    interactive = False

    input_port_types = [{
        'name': 'NoteRest Interval Indexer Result',
        'resource_types': ['application/x-vis_noterest_pandas_series+csv'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Horizontal Interval Indexer Result',
        'resource_types': ['application/x-vis_horizontal_pandas_series+csv'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Set execution settings.
        wrapper_settings = dict( [(k, settings[k]) for k in ('Simple or Compound Intervals', 'Interval Quality', 'Directed', 'Horizontal attach later')] )
        execution_settings = dict()
        if wrapper_settings['Simple or Compound Intervals'] == 0:
            execution_settings['simple or compound'] = 'simple'
        else:
            execution_settings['simple or compound'] = 'compound'
        execution_settings['quality'] = wrapper_settings['Interval Quality']
        execution_settings['mp'] = False
        execution_settings['horiz_attach_later'] = wrapper_settings['Horizontal attach later']
        execution_settings['directed'] = wrapper_settings['Directed']
        
        # Run.
        infile = inputs['NoteRest Interval Indexer Result'][0]['resource_path']
        outfile = outputs['Horizontal Interval Indexer Result'][0]['resource_path']
        data = DataFrame.from_csv(infile, header = [0, 1]) # We know the first two rows constitute a MultiIndex
        horizontal_intervals = HorizontalIntervalIndexer(data, execution_settings).run()
        horizontal_intervals.to_csv(outfile)

        return True