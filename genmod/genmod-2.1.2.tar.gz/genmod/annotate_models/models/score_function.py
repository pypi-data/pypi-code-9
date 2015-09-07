#!/usr/bin/env python
# encoding: utf-8
"""
score_function.py

Class for creating score functions.

Created by Måns Magnusson on 2015-04-08.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import (print_function, unicode_literals)

import sys
import os
import logging


class ScoreFunction(object):
    """
    Class for creating a score function.
    
    There are two types of scorings.
    Either the value in the vcf is a string, then we do a string match based
    on the information given in score_information
    Or we compare numerical values then we check for operators and what to
    compare with in score information.
    
    Args:
        score_information (dict): All the necessary information about scoring
        and how to get the data from a vcf. This information have been checked
        with the config parser.
     
    """
    def __init__(self, score_information):
        super(ScoreFunction, self).__init__()
        
        self.logger = logging.getLogger(__name__)
        
        self.vcf_field = score_information['field']
        self.logger.info("VCF field: {0}".format(self.vcf_field))
        self.family_level = False
        if score_information.get('family_level', None):
            self.family_level = True
        self.logger.debug("Family level: {0}".format(self.family_level))
        
        self.info_key = None
        self.csq_key = None
        
        if self.vcf_field == 'INFO':
            self.info_key = score_information['info_key']
            self.logger.debug("Info key: {0}".format(self.info_key))
            
            if self.info_key == 'CSQ':
                self.csq_key = score_information['csq_key']
                self.logger.debug("CSQ key: {0}".format(self.csq_key))
        
        self.data_type = score_information['data_type']
        self.logger.debug("Data type: {0}".format(self.data_type))
        self.field_separators = score_information['field_separators']
        self.logger.debug("Field separators: {0}".format(self.field_separators))
        self.record_aggregation = score_information['record_aggregation']
        self.logger.debug("Record aggregation: {0}".format(self.record_aggregation))
        
        # These are the scores that are found for a variant
        self.scores = []
        self.score_dict = {}
        # We allways need to have a "not reported" score
        self.not_reported_score = 0
        # We check for the scoring rules, these are dictionaries
        for key in score_information:
            if isinstance(score_information[key], dict):
                score_dict = score_information[key]
                self.logger.debug("Found score information with score={0}, "\
                    "operator={1}, value={2}".format(
                        score_dict['score'],
                        score_dict['operator'],
                        score_dict['value'],
                        ))
                
                if score_dict['value'] == 'na':
                    self.not_reported_score = float(score_dict['score'])
                    self.logger.debug("Setting not reported score to {0}".format(
                        score_dict['score']
                    ))
                    
                else:
                    self.scores.append(score_dict)
        
        # If the datatype in vcf is a string we build a dictionary with the 
        # string matches as keys and scores as values:
        if self.data_type == 'string':
            self.logger.debug("Building string dict for string matcing.")
            self.score_dict = self.build_string_dict(self.scores)
    
    def build_string_dict(self, scores):
        """
        Build a dictionary where the string matches are keys and scores are
        values.
        
        Args:
            scores (list): A list of dictionarys with scoring information
        
        Returns:
            score_dict: A dictionary with string match as key and score as 
                        value
        """
        score_dict = {}
        for score in scores:
            score_dict[score['value']] = float(score['score'])
        
        return score_dict
    
    def get_vep_annotations(self, variant):
        """
        Return the proper annotations from the vep annotation.
        
        Arguments:
            variant (dict): A variant dictionary
        
        Returns:
            annotations (list): A list with the annotations
        """
        annotations = []
        for allele in variant['vep_info']:
            if allele != 'gene_ids':
                for vep_annotation in variant['vep_info'][allele]:
                    # Get the vep entrys:
                    if vep_annotation.get(self.csq_key, None):
                        annotations.append(vep_annotation[self.csq_key])
        
        return annotations
        
    
    def get_family_annotations(self, variant, family_id):
        """
        Return a dictionary with family id as key and a list of annotations as 
        values.
        
        Arguments:
            variant (dict): A variant dictionary
            family_id (str): String that represents the family id
        
        Returns:
            annotations (list): A list with the annotations for this family
        """
        annotations = []
        if self.info_key == 'GeneticModels':
            annotations = variant['genetic_models'].get(family_id,[])
        
        return annotations
        
    def score(self, variant, family_id):
        """
        Score a variant based on the given information for this ScoreFunction
        
        Args:
            variant (dict): A dictionary with variant information
        
        Returns:
            score (float): A score according to the given rules
        """
        scores = []
        # pp(variant)
        if self.vcf_field == 'INFO':
            self.logger.debug("Collecting INFO field for {0}".format(
                    self.info_key
                    )
            )
            
            if self.info_key == 'CSQ':
                self.logger.debug("Collecting CSQ field for {0}".format(
                        self.csq_key
                        )
                )
                vcf_annotations = self.get_vep_annotations(variant)
            # We make a special case for genetic models since it is genmod that
            # does this annotation
            elif self.info_key == 'GeneticModels':
                vcf_annotations = self.get_family_annotations(variant, family_id)
            else:
                vcf_annotations = variant['info_dict'].get(self.info_key, [])
        else:
            vcf_annotations = variant.get(self.vcf_field,'').split(
                self.field_separators[0]
            )
        self.logger.debug("Found annotation {0}".format(vcf_annotations))
        
        if self.data_type == 'string':
            for annotation in vcf_annotations:
                self.logger.debug("Scoring {0}".format(annotation))
                score = self.score_dict.get(annotation, None)
                self.logger.debug("Found score {0}".format(score))
                if score:
                    scores.append(score)
        
        elif self.data_type in ['float', 'integer']:
            for annotation in vcf_annotations:
                for score_function in self.scores:
                    if score_function['operator'] == 'le':
                        if float(annotation) <= float(score_function['value']):
                            scores.append(float(score_function['score']))
                    if score_function['operator'] == 'lt':
                        if float(annotation) < float(score_function['value']):
                            scores.append(float(score_function['score']))
                    elif score_function['operator'] == 'gt':
                        if float(annotation) > float(score_function['value']):
                            scores.append(float(score_function['score']))
                    elif score_function['operator'] == 'ge':
                        if float(annotation) >= float(score_function['value']):
                            scores.append(float(score_function['score']))
                    elif score_function['operator'] == 'eq':
                    # If the value is 'eq' the score is the annotation
                        if score_function['score'] == 'eq':
                            scores.append(float(annotation))
                        elif float(annotation) == float(score_function['value']):
                            scores.append(float(score_function['score']))
        
        # If there were no scores we return the score found:
        if len(scores) == 0:
            scores = [self.not_reported_score]
        
        # If the aggregation is min we return the minimal score
        # else we return the maimum score for the annotation.
        if self.record_aggregation == 'min':
            score = min(scores)
        else:
            score = max(scores)
        
        return score
    
    
    def __repr__(self):
        return "ScoreFunction(vcf_field={0}, info_key={1}, csq_key={2}, "
                "data_type={3}, field_separators={4}, "
                "record_aggregation={5})".format(
                    self.vcf_field, self.info_key, self.csq_key, self.data_type,
                    self.field_separators, self.record_aggregation)
