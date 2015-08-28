import logging

def check_individuals(family_parser, vcf_individuals):
    """
    Check if the individuals from ped file is in vcf file
    
    Arguments:
        family_parser (FamilyParser): A FamilyParser object
        vcf_individuals (list): the individuals found in the vcf file 
    """
    logger = logging.getLogger(__name__)
    for individual in family_parser.individuals:
        if individual not in vcf_individuals:
            logger.warning("All individuals in ped file must be in vcf "\
                            "file!")
            logger.warning("Individuals in PED file: {0}".format(
                            ', '.join(list(family_parser.individuals.keys()))))
            logger.warning("Individuals in VCF file: {0}".format(', '.join(vcf_individuals)))
            raise IOError() # Raise proper exception here
    return