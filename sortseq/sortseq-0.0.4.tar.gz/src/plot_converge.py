dbls = pymc.database.sqlite.load('crp_model_max_ls_init_0.sql')
db = pymc.database.sqlite.load('crp_model_max.sql_0.sql')
em = db.trace('emat')
emls = dbls.trace('emat')
Lem = em[:].shape[0]
MI_ls = np.zeros(Lem)
MI = np.zeros(Lem)
seq_dict,inv_dict = utils.choose_dict('dna')
df = pd.io.parsers.read_csv('data.txt',delim_whitespace=True)
df['seq'] = df['seq'].str.slice(start=3,stop=25)
s,b = utils.array_seqs_weights(df,seq_dict)
for i in range(Lem):
    value = em[:][i]
    dot = value[:,:,sp.newaxis]*s
    expression = dot.sum(0).sum(0)               
    #expression,b = utils.expand_sw(expression,b,sw)      
    rankexpression,batch = utils.shuffle_rank(expression,b)        
    n_seqs = len(b)
        
       
    MI[i] = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,batch)

    value2 = emls[:][i]
    dot = value2[:,:,sp.newaxis]*s
    expression = dot.sum(0).sum(0)               
    #expression,b = utils.expand_sw(expression,b,sw)      
    rankexpression,batch = utils.shuffle_rank(expression,b)        
    n_seqs = len(b)
        
       
    MI_ls[i] = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,batch)
    
