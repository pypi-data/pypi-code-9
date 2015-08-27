from puq import *
# create PDF from gap histogram (Lnom = 400um)

def run():
    A1 = UniformParameter('strainf', 'st factor', min=-0.002, max=0.002)

    # host = PBSHost(env='/group/prism/data/memosa/env-hansen_seq.sh',cpus=1, cpus_per_node=48, walltime='2:00:00', qname='standby')

    host = InteractiveHost()
    
    uq = Smolyak([A1], level=1)

    prog0 = TestProgram('seqUQ',
                       newdir=True,
                       infiles=['Cu_volumetric.tape5','Cu.atm'],
                       exe="../v_main.py --A1 $strainf",
                       desc='SeqQuest strain factor')

    return Sweep(uq, host, prog0)
