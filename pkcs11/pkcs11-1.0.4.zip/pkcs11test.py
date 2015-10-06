#!/c/Python23/python
import sys, getpass, struct, getopt, os, os.path
import pkcs11

optvals, args = getopt.getopt(sys.argv[1:], 'd:lMmsu:x?')

dllname = os.path.join(os.environ['windir'], 'system32\\dspkcs.dll')
do_mozilla = 0
do_mechanisms = 0
do_login = 1
select_slot = 0
use_mutex = None
user_type = pkcs11.CKU_USER

for k, v in optvals :
    if k == '-d' :
        dllname = v
    elif k == '-l' :
        do_login = 0
    elif k == '-s' :
        select_slot = 1
    elif k == '-M' :
        do_mozilla = 1
        dllname = 'c:/Program Files/mozilla.org/Mozilla/softokn3.dll'
        os.environ['PATH'] = os.environ['PATH'] + ';c:/Program Files/mozilla.org/Mozilla'
    elif k == '-m' :
        do_mechanisms = 1
    elif k == '-u' :
        if v == 'SO' :
            user_type = pkcs11.CKU_SO
        elif v == 'USER' :
            user_type = pkcs11.CKU_USER
        else :
            raise RuntimeError('unknown user type "%s"' % v)
    elif k == '-x' :
        use_mutex = 1
    elif k == '-?' :
        print 'usage: %s [-d <dll_path>] [-l] [-s] [-M] [-m] [-u <user_type>] [-x]' % sys.argv[0]
        sys.exit(0)
        
if do_mozilla :
    pdll = pkcs11.open(dllname, init_str="configdir='C:/Documents and Settings/jbj1/Application Data/Mozilla/Profiles/default/csl30ups.slt' certPrefix='' keyPrefix='' secmod='secmod.db' flags=  manufacturerID='Mozilla.org' libraryDescription='PSM Internal Crypto Services' cryptoTokenDescription='Generic Crypto Services' dbTokenDescription='Software Security Device' cryptoSlotDescription='PSM Internal Cryptographic Services' dbSlotDescription='PSM Private Keys' FIPSSlotDescription='PSM Internal FIPS-140-1 Cryptographic Services' FIPSTokenDescription='PSM FIPS-140-1 User Private Key Services' minPS=0", mutex=use_mutex)
else :
    pdll = pkcs11.open(dllname, mutex=use_mutex)

ci = pdll.getInfo()
print 'Cryptoki Info:'
print '  manufacturer: %s' % ci.manufacturerID.strip()
print '  library:      %s' % ci.libraryDescription.strip()
v = ci.cryptokiVersion
print '  version:      %d.%d' % (v[0], v[1])
print ''

slot_list = pdll.getSlotList(0)
print '%d slots' % len(slot_list)
print ''

if select_slot :
    for s in slot_list :
        si = pdll.getSlotInfo(s)
        print '%s: %s' % (s, si.slotDescription)
        if si.flags & pkcs11.CKF_TOKEN_PRESENT :
            ti = pdll.getTokenInfo(s)
            print ' token: %s' % ti.label
    slot_num = raw_input('slot num? ')
    slot_list = (int(slot_num),)

# we keep a mapping from OBJECT type constants to their names so we can
# print them out
object_type_names = {
    pkcs11.CKO_DATA : 'CKO_DATA',
    pkcs11.CKO_CERTIFICATE : 'CKO_CERTIFICATE',
    pkcs11.CKO_PUBLIC_KEY : 'CKO_PUBLIC_KEY',
    pkcs11.CKO_PRIVATE_KEY : 'CKO_PRIVATE_KEY',
    pkcs11.CKO_SECRET_KEY : 'CKO_SECRET_KEY',
    pkcs11.CKO_HW_FEATURE : 'CKO_HW_FEATURE',
    pkcs11.CKO_DOMAIN_PARAMETERS : 'CKO_DOMAIN_PARAMETERS',
    pkcs11.CKO_VENDOR_DEFINED : 'CKO_VENDOR_DEFINED'
    }

def get_object_name(t_id) :
    if object_type_names.has_key(t_id) :
        return object_type_names[t_id]
    return hex(t_id)

mechanism_type_names = {
	pkcs11.CKM_RSA_PKCS_KEY_PAIR_GEN : 'CKM_RSA_PKCS_KEY_PAIR_GEN',
	pkcs11.CKM_RSA_PKCS : 'CKM_RSA_PKCS',
	pkcs11.CKM_RSA_9796 : 'CKM_RSA_9796',
	pkcs11.CKM_RSA_X_509 : 'CKM_RSA_X_509',
	pkcs11.CKM_MD2_RSA_PKCS : 'CKM_MD2_RSA_PKCS',
	pkcs11.CKM_MD5_RSA_PKCS : 'CKM_MD5_RSA_PKCS',
	pkcs11.CKM_SHA1_RSA_PKCS : 'CKM_SHA1_RSA_PKCS',
	pkcs11.CKM_RIPEMD128_RSA_PKCS : 'CKM_RIPEMD128_RSA_PKCS',
	pkcs11.CKM_RIPEMD160_RSA_PKCS : 'CKM_RIPEMD160_RSA_PKCS',
	pkcs11.CKM_RSA_PKCS_OAEP : 'CKM_RSA_PKCS_OAEP',
	pkcs11.CKM_RSA_X9_31_KEY_PAIR_GEN : 'CKM_RSA_X9_31_KEY_PAIR_GEN',
	pkcs11.CKM_RSA_X9_31 : 'CKM_RSA_X9_31',
	pkcs11.CKM_SHA1_RSA_X9_31 : 'CKM_SHA1_RSA_X9_31',
	pkcs11.CKM_RSA_PKCS_PSS : 'CKM_RSA_PKCS_PSS',
	pkcs11.CKM_SHA1_RSA_PKCS_PSS : 'CKM_SHA1_RSA_PKCS_PSS',
	pkcs11.CKM_DSA_KEY_PAIR_GEN : 'CKM_DSA_KEY_PAIR_GEN',
	pkcs11.CKM_DSA : 'CKM_DSA',
	pkcs11.CKM_DSA_SHA1 : 'CKM_DSA_SHA1',
	pkcs11.CKM_DH_PKCS_KEY_PAIR_GEN : 'CKM_DH_PKCS_KEY_PAIR_GEN',
	pkcs11.CKM_DH_PKCS_DERIVE : 'CKM_DH_PKCS_DERIVE',
	pkcs11.CKM_X9_42_DH_KEY_PAIR_GEN : 'CKM_X9_42_DH_KEY_PAIR_GEN',
	pkcs11.CKM_X9_42_DH_DERIVE : 'CKM_X9_42_DH_DERIVE',
	pkcs11.CKM_X9_42_DH_HYBRID_DERIVE : 'CKM_X9_42_DH_HYBRID_DERIVE',
	pkcs11.CKM_X9_42_MQV_DERIVE : 'CKM_X9_42_MQV_DERIVE',
	pkcs11.CKM_RC2_KEY_GEN : 'CKM_RC2_KEY_GEN',
	pkcs11.CKM_RC2_ECB : 'CKM_RC2_ECB',
	pkcs11.CKM_RC2_CBC : 'CKM_RC2_CBC',
	pkcs11.CKM_RC2_MAC : 'CKM_RC2_MAC',
	pkcs11.CKM_RC2_MAC_GENERAL : 'CKM_RC2_MAC_GENERAL',
	pkcs11.CKM_RC2_CBC_PAD : 'CKM_RC2_CBC_PAD',
	pkcs11.CKM_RC4_KEY_GEN : 'CKM_RC4_KEY_GEN',
	pkcs11.CKM_RC4 : 'CKM_RC4',
	pkcs11.CKM_DES_KEY_GEN : 'CKM_DES_KEY_GEN',
	pkcs11.CKM_DES_ECB : 'CKM_DES_ECB',
	pkcs11.CKM_DES_CBC : 'CKM_DES_CBC',
	pkcs11.CKM_DES_MAC : 'CKM_DES_MAC',
	pkcs11.CKM_DES_MAC_GENERAL : 'CKM_DES_MAC_GENERAL',
	pkcs11.CKM_DES_CBC_PAD : 'CKM_DES_CBC_PAD',
	pkcs11.CKM_DES2_KEY_GEN : 'CKM_DES2_KEY_GEN',
	pkcs11.CKM_DES3_KEY_GEN : 'CKM_DES3_KEY_GEN',
	pkcs11.CKM_DES3_ECB : 'CKM_DES3_ECB',
	pkcs11.CKM_DES3_CBC : 'CKM_DES3_CBC',
	pkcs11.CKM_DES3_MAC : 'CKM_DES3_MAC',
	pkcs11.CKM_DES3_MAC_GENERAL : 'CKM_DES3_MAC_GENERAL',
	pkcs11.CKM_DES3_CBC_PAD : 'CKM_DES3_CBC_PAD',
	pkcs11.CKM_CDMF_KEY_GEN : 'CKM_CDMF_KEY_GEN',
	pkcs11.CKM_CDMF_ECB : 'CKM_CDMF_ECB',
	pkcs11.CKM_CDMF_CBC : 'CKM_CDMF_CBC',
	pkcs11.CKM_CDMF_MAC : 'CKM_CDMF_MAC',
	pkcs11.CKM_CDMF_MAC_GENERAL : 'CKM_CDMF_MAC_GENERAL',
	pkcs11.CKM_CDMF_CBC_PAD : 'CKM_CDMF_CBC_PAD',
	pkcs11.CKM_MD2 : 'CKM_MD2',
	pkcs11.CKM_MD2_HMAC : 'CKM_MD2_HMAC',
	pkcs11.CKM_MD2_HMAC_GENERAL : 'CKM_MD2_HMAC_GENERAL',
	pkcs11.CKM_MD5 : 'CKM_MD5',
	pkcs11.CKM_MD5_HMAC : 'CKM_MD5_HMAC',
	pkcs11.CKM_MD5_HMAC_GENERAL : 'CKM_MD5_HMAC_GENERAL',
	pkcs11.CKM_SHA_1 : 'CKM_SHA_1',
	pkcs11.CKM_SHA_1_HMAC : 'CKM_SHA_1_HMAC',
	pkcs11.CKM_SHA_1_HMAC_GENERAL : 'CKM_SHA_1_HMAC_GENERAL',
	pkcs11.CKM_RIPEMD128 : 'CKM_RIPEMD128',
	pkcs11.CKM_RIPEMD128_HMAC : 'CKM_RIPEMD128_HMAC',
	pkcs11.CKM_RIPEMD128_HMAC_GENERAL : 'CKM_RIPEMD128_HMAC_GENERAL',
	pkcs11.CKM_RIPEMD160 : 'CKM_RIPEMD160',
	pkcs11.CKM_RIPEMD160_HMAC : 'CKM_RIPEMD160_HMAC',
	pkcs11.CKM_RIPEMD160_HMAC_GENERAL : 'CKM_RIPEMD160_HMAC_GENERAL',
	pkcs11.CKM_CAST_KEY_GEN : 'CKM_CAST_KEY_GEN',
	pkcs11.CKM_CAST_ECB : 'CKM_CAST_ECB',
	pkcs11.CKM_CAST_CBC : 'CKM_CAST_CBC',
	pkcs11.CKM_CAST_MAC : 'CKM_CAST_MAC',
	pkcs11.CKM_CAST_MAC_GENERAL : 'CKM_CAST_MAC_GENERAL',
	pkcs11.CKM_CAST_CBC_PAD : 'CKM_CAST_CBC_PAD',
	pkcs11.CKM_CAST3_KEY_GEN : 'CKM_CAST3_KEY_GEN',
	pkcs11.CKM_CAST3_ECB : 'CKM_CAST3_ECB',
	pkcs11.CKM_CAST3_CBC : 'CKM_CAST3_CBC',
	pkcs11.CKM_CAST3_MAC : 'CKM_CAST3_MAC',
	pkcs11.CKM_CAST3_MAC_GENERAL : 'CKM_CAST3_MAC_GENERAL',
	pkcs11.CKM_CAST3_CBC_PAD : 'CKM_CAST3_CBC_PAD',
	pkcs11.CKM_CAST5_KEY_GEN : 'CKM_CAST5_KEY_GEN',
	pkcs11.CKM_CAST128_KEY_GEN : 'CKM_CAST128_KEY_GEN',
	pkcs11.CKM_CAST5_ECB : 'CKM_CAST5_ECB',
	pkcs11.CKM_CAST128_ECB : 'CKM_CAST128_ECB',
	pkcs11.CKM_CAST5_CBC : 'CKM_CAST5_CBC',
	pkcs11.CKM_CAST128_CBC : 'CKM_CAST128_CBC',
	pkcs11.CKM_CAST5_MAC : 'CKM_CAST5_MAC',
	pkcs11.CKM_CAST128_MAC : 'CKM_CAST128_MAC',
	pkcs11.CKM_CAST5_MAC_GENERAL : 'CKM_CAST5_MAC_GENERAL',
	pkcs11.CKM_CAST128_MAC_GENERAL : 'CKM_CAST128_MAC_GENERAL',
	pkcs11.CKM_CAST5_CBC_PAD : 'CKM_CAST5_CBC_PAD',
	pkcs11.CKM_CAST128_CBC_PAD : 'CKM_CAST128_CBC_PAD',
	pkcs11.CKM_RC5_KEY_GEN : 'CKM_RC5_KEY_GEN',
	pkcs11.CKM_RC5_ECB : 'CKM_RC5_ECB',
	pkcs11.CKM_RC5_CBC : 'CKM_RC5_CBC',
	pkcs11.CKM_RC5_MAC : 'CKM_RC5_MAC',
	pkcs11.CKM_RC5_MAC_GENERAL : 'CKM_RC5_MAC_GENERAL',
	pkcs11.CKM_RC5_CBC_PAD : 'CKM_RC5_CBC_PAD',
	pkcs11.CKM_IDEA_KEY_GEN : 'CKM_IDEA_KEY_GEN',
	pkcs11.CKM_IDEA_ECB : 'CKM_IDEA_ECB',
	pkcs11.CKM_IDEA_CBC : 'CKM_IDEA_CBC',
	pkcs11.CKM_IDEA_MAC : 'CKM_IDEA_MAC',
	pkcs11.CKM_IDEA_MAC_GENERAL : 'CKM_IDEA_MAC_GENERAL',
	pkcs11.CKM_IDEA_CBC_PAD : 'CKM_IDEA_CBC_PAD',
	pkcs11.CKM_GENERIC_SECRET_KEY_GEN : 'CKM_GENERIC_SECRET_KEY_GEN',
	pkcs11.CKM_CONCATENATE_BASE_AND_KEY : 'CKM_CONCATENATE_BASE_AND_KEY',
	pkcs11.CKM_CONCATENATE_BASE_AND_DATA : 'CKM_CONCATENATE_BASE_AND_DATA',
	pkcs11.CKM_CONCATENATE_DATA_AND_BASE : 'CKM_CONCATENATE_DATA_AND_BASE',
	pkcs11.CKM_XOR_BASE_AND_DATA : 'CKM_XOR_BASE_AND_DATA',
	pkcs11.CKM_EXTRACT_KEY_FROM_KEY : 'CKM_EXTRACT_KEY_FROM_KEY',
	pkcs11.CKM_SSL3_PRE_MASTER_KEY_GEN : 'CKM_SSL3_PRE_MASTER_KEY_GEN',
	pkcs11.CKM_SSL3_MASTER_KEY_DERIVE : 'CKM_SSL3_MASTER_KEY_DERIVE',
	pkcs11.CKM_SSL3_KEY_AND_MAC_DERIVE : 'CKM_SSL3_KEY_AND_MAC_DERIVE',
	pkcs11.CKM_SSL3_MASTER_KEY_DERIVE_DH : 'CKM_SSL3_MASTER_KEY_DERIVE_DH',
	pkcs11.CKM_TLS_PRE_MASTER_KEY_GEN : 'CKM_TLS_PRE_MASTER_KEY_GEN',
	pkcs11.CKM_TLS_MASTER_KEY_DERIVE : 'CKM_TLS_MASTER_KEY_DERIVE',
	pkcs11.CKM_TLS_KEY_AND_MAC_DERIVE : 'CKM_TLS_KEY_AND_MAC_DERIVE',
	pkcs11.CKM_TLS_MASTER_KEY_DERIVE_DH : 'CKM_TLS_MASTER_KEY_DERIVE_DH',
	pkcs11.CKM_SSL3_MD5_MAC : 'CKM_SSL3_MD5_MAC',
	pkcs11.CKM_SSL3_SHA1_MAC : 'CKM_SSL3_SHA1_MAC',
	pkcs11.CKM_MD5_KEY_DERIVATION : 'CKM_MD5_KEY_DERIVATION',
	pkcs11.CKM_MD2_KEY_DERIVATION : 'CKM_MD2_KEY_DERIVATION',
	pkcs11.CKM_SHA1_KEY_DERIVATION : 'CKM_SHA1_KEY_DERIVATION',
	pkcs11.CKM_PBE_MD2_DES_CBC : 'CKM_PBE_MD2_DES_CBC',
	pkcs11.CKM_PBE_MD5_DES_CBC : 'CKM_PBE_MD5_DES_CBC',
	pkcs11.CKM_PBE_MD5_CAST_CBC : 'CKM_PBE_MD5_CAST_CBC',
	pkcs11.CKM_PBE_MD5_CAST3_CBC : 'CKM_PBE_MD5_CAST3_CBC',
	pkcs11.CKM_PBE_MD5_CAST5_CBC : 'CKM_PBE_MD5_CAST5_CBC',
	pkcs11.CKM_PBE_MD5_CAST128_CBC : 'CKM_PBE_MD5_CAST128_CBC',
	pkcs11.CKM_PBE_SHA1_CAST5_CBC : 'CKM_PBE_SHA1_CAST5_CBC',
	pkcs11.CKM_PBE_SHA1_CAST128_CBC : 'CKM_PBE_SHA1_CAST128_CBC',
	pkcs11.CKM_PBE_SHA1_RC4_128 : 'CKM_PBE_SHA1_RC4_128',
	pkcs11.CKM_PBE_SHA1_RC4_40 : 'CKM_PBE_SHA1_RC4_40',
	pkcs11.CKM_PBE_SHA1_DES3_EDE_CBC : 'CKM_PBE_SHA1_DES3_EDE_CBC',
	pkcs11.CKM_PBE_SHA1_DES2_EDE_CBC : 'CKM_PBE_SHA1_DES2_EDE_CBC',
	pkcs11.CKM_PBE_SHA1_RC2_128_CBC : 'CKM_PBE_SHA1_RC2_128_CBC',
	pkcs11.CKM_PBE_SHA1_RC2_40_CBC : 'CKM_PBE_SHA1_RC2_40_CBC',
	pkcs11.CKM_PKCS5_PBKD2 : 'CKM_PKCS5_PBKD2',
	pkcs11.CKM_PBA_SHA1_WITH_SHA1_HMAC : 'CKM_PBA_SHA1_WITH_SHA1_HMAC',
	pkcs11.CKM_KEY_WRAP_LYNKS : 'CKM_KEY_WRAP_LYNKS',
	pkcs11.CKM_KEY_WRAP_SET_OAEP : 'CKM_KEY_WRAP_SET_OAEP',
	pkcs11.CKM_SKIPJACK_KEY_GEN : 'CKM_SKIPJACK_KEY_GEN',
	pkcs11.CKM_SKIPJACK_ECB64 : 'CKM_SKIPJACK_ECB64',
	pkcs11.CKM_SKIPJACK_CBC64 : 'CKM_SKIPJACK_CBC64',
	pkcs11.CKM_SKIPJACK_OFB64 : 'CKM_SKIPJACK_OFB64',
	pkcs11.CKM_SKIPJACK_CFB64 : 'CKM_SKIPJACK_CFB64',
	pkcs11.CKM_SKIPJACK_CFB32 : 'CKM_SKIPJACK_CFB32',
	pkcs11.CKM_SKIPJACK_CFB16 : 'CKM_SKIPJACK_CFB16',
	pkcs11.CKM_SKIPJACK_CFB8 : 'CKM_SKIPJACK_CFB8',
	pkcs11.CKM_SKIPJACK_WRAP : 'CKM_SKIPJACK_WRAP',
	pkcs11.CKM_SKIPJACK_PRIVATE_WRAP : 'CKM_SKIPJACK_PRIVATE_WRAP',
	pkcs11.CKM_SKIPJACK_RELAYX : 'CKM_SKIPJACK_RELAYX',
	pkcs11.CKM_KEA_KEY_PAIR_GEN : 'CKM_KEA_KEY_PAIR_GEN',
	pkcs11.CKM_KEA_KEY_DERIVE : 'CKM_KEA_KEY_DERIVE',
	pkcs11.CKM_FORTEZZA_TIMESTAMP : 'CKM_FORTEZZA_TIMESTAMP',
	pkcs11.CKM_BATON_KEY_GEN : 'CKM_BATON_KEY_GEN',
	pkcs11.CKM_BATON_ECB128 : 'CKM_BATON_ECB128',
	pkcs11.CKM_BATON_ECB96 : 'CKM_BATON_ECB96',
	pkcs11.CKM_BATON_CBC128 : 'CKM_BATON_CBC128',
	pkcs11.CKM_BATON_COUNTER : 'CKM_BATON_COUNTER',
	pkcs11.CKM_BATON_SHUFFLE : 'CKM_BATON_SHUFFLE',
	pkcs11.CKM_BATON_WRAP : 'CKM_BATON_WRAP',
	pkcs11.CKM_ECDSA_KEY_PAIR_GEN : 'CKM_ECDSA_KEY_PAIR_GEN',
	pkcs11.CKM_EC_KEY_PAIR_GEN : 'CKM_EC_KEY_PAIR_GEN',
	pkcs11.CKM_ECDSA : 'CKM_ECDSA',
	pkcs11.CKM_ECDSA_SHA1 : 'CKM_ECDSA_SHA1',
	pkcs11.CKM_ECDH1_DERIVE : 'CKM_ECDH1_DERIVE',
	pkcs11.CKM_ECDH1_COFACTOR_DERIVE : 'CKM_ECDH1_COFACTOR_DERIVE',
	pkcs11.CKM_ECMQV_DERIVE : 'CKM_ECMQV_DERIVE',
	pkcs11.CKM_JUNIPER_KEY_GEN : 'CKM_JUNIPER_KEY_GEN',
	pkcs11.CKM_JUNIPER_ECB128 : 'CKM_JUNIPER_ECB128',
	pkcs11.CKM_JUNIPER_CBC128 : 'CKM_JUNIPER_CBC128',
	pkcs11.CKM_JUNIPER_COUNTER : 'CKM_JUNIPER_COUNTER',
	pkcs11.CKM_JUNIPER_SHUFFLE : 'CKM_JUNIPER_SHUFFLE',
	pkcs11.CKM_JUNIPER_WRAP : 'CKM_JUNIPER_WRAP',
	pkcs11.CKM_FASTHASH : 'CKM_FASTHASH',
	pkcs11.CKM_AES_KEY_GEN : 'CKM_AES_KEY_GEN',
	pkcs11.CKM_AES_ECB : 'CKM_AES_ECB',
	pkcs11.CKM_AES_CBC : 'CKM_AES_CBC',
	pkcs11.CKM_AES_MAC : 'CKM_AES_MAC',
	pkcs11.CKM_AES_MAC_GENERAL : 'CKM_AES_MAC_GENERAL',
	pkcs11.CKM_AES_CBC_PAD : 'CKM_AES_CBC_PAD',
	pkcs11.CKM_DSA_PARAMETER_GEN : 'CKM_DSA_PARAMETER_GEN',
	pkcs11.CKM_DH_PKCS_PARAMETER_GEN : 'CKM_DH_PKCS_PARAMETER_GEN',
	pkcs11.CKM_X9_42_DH_PARAMETER_GEN : 'CKM_X9_42_DH_PARAMETER_GEN',
	pkcs11.CKM_VENDOR_DEFINED : 'CKM_VENDOR_DEFINED'
    }

def get_mechanism_name(m_id) :
    if mechanism_type_names.has_key(m_id) :
        return mechanism_type_names[m_id]
    return hex(m_id)

def hex_str(s) :
    hx_l = []
    for c in s :
        n = ord(c)
        if n > 15 :
            hx_l.append(hex(n)[2:])
        else :
            hx_l.append('0' + hex(n)[2:])
    return ':'.join(hx_l)

for s in slot_list :
    si = pdll.getSlotInfo(s)
    print 'Slot %d' % s
    print '  Description: %s' % si.slotDescription.strip()
    flag_list = []
    if si.flags & pkcs11.CKF_TOKEN_PRESENT :
        flag_list.append('Token is present')
    else :
        flag_list.append('Token not present')
    if si.flags & pkcs11.CKF_REMOVABLE_DEVICE :
        flag_list.append('Removable device')
    if si.flags & pkcs11.CKF_HW_SLOT :
        flag_list.append('Hardware device')
    else :
        flag_list.append('Software device')
    print '  %s' % ', '.join(flag_list)
    if si.flags & pkcs11.CKF_TOKEN_PRESENT :
        ti = pdll.getTokenInfo(s)
        print '  Token Info:'
        print '             label: %s' % ti.label.strip()
        print '    manufacturerID: %s' % ti.manufacturerID.strip()
        print '             model: %s' % ti.model.strip()
        print '      serialNumber: %s' % ti.serialNumber.strip()
        if ti.flags & pkcs11.CKF_CLOCK_ON_TOKEN :
            print '           utcTime: %s' % ti.utcTime.strip()
        flag_list = []
        if ti.flags & pkcs11.CKF_RNG :
            flag_list.append('has Random Number Generator')
        if ti.flags & pkcs11.CKF_WRITE_PROTECTED :
            flag_list.append('read-only')
        if ti.flags & pkcs11.CKF_LOGIN_REQUIRED :
            flag_list.append('requires login')
        if ti.flags & pkcs11.CKF_USER_PIN_INITIALIZED :
            flag_list.append('user pin set')
        if ti.flags & pkcs11.CKF_RESTORE_KEY_NOT_NEEDED :
            flag_list.append('restore key not needed')
        if ti.flags & pkcs11.CKF_PROTECTED_AUTHENTICATION_PATH :
            flag_list.append('has external login')
        if ti.flags & pkcs11.CKF_DUAL_CRYPTO_OPERATIONS :
            flag_list.append('dual crypto capable')
        if ti.flags & pkcs11.CKF_TOKEN_INITIALIZED :
            flag_list.append('token initialized')
        if ti.flags & pkcs11.CKF_SECONDARY_AUTHENTICATION :
            flag_list.append('secondary authentication support')
        if ti.flags & pkcs11.CKF_USER_PIN_COUNT_LOW :
            flag_list.append('user pin failure')
        if ti.flags & pkcs11.CKF_USER_PIN_FINAL_TRY :
            flag_list.append('user pin final try')
        if ti.flags & pkcs11.CKF_USER_PIN_LOCKED :
            flag_list.append('user pin locked')
        if ti.flags & pkcs11.CKF_USER_PIN_TO_BE_CHANGED :
            flag_list.append('user pin set to default')
        if ti.flags & pkcs11.CKF_SO_PIN_COUNT_LOW :
            flag_list.append('so pin failure')
        if ti.flags & pkcs11.CKF_SO_PIN_FINAL_TRY :
            flag_list.append('so pin final try')
        if ti.flags & pkcs11.CKF_SO_PIN_LOCKED :
            flag_list.append('so pin locked')
        if ti.flags & pkcs11.CKF_SO_PIN_TO_BE_CHANGED :
            flag_list.append('so pin set to default')
        print '             flags: %s' % ', '.join(flag_list)
        if do_mechanisms :
            #print 'C_GetMechanismList(%d):' % s
            print '  Mechanisms available:'
            mech_list = pdll.getMechanismList(s)
            #print mech_list
            for m in mech_list :
                #print 'C_GetMechanismInfo(%d, %d)' % (s, m)
                print '    %s %s' % (get_mechanism_name(m), pdll.getMechanismInfo(s, m))
        
        # open up a session
        #session = pdll.openSession(slot_list[0], pkcs11.CKF_RW_SESSION)
        session = pdll.openSession(s, 0)
        #print "session.sh = %s" % session.sh

        # now we'll log in!
        if ti.flags & pkcs11.CKF_LOGIN_REQUIRED and do_login :
            passwd = getpass.getpass('Please enter User PIN: ')
            session.login(user_type, passwd)

        obj_list = session.findObjects(None)
        print 'C_FindObjectsXX: '
        print obj_list
        for h in obj_list :
            cls = struct.unpack("i", session.getAttributeValue(h, (pkcs11.CKA_CLASS,))[0])[0]
            print '%d CKA_CLASS = %s' % (h, get_object_name(cls))
            if cls == pkcs11.CKO_CERTIFICATE :
                print '   label = %s' % session.getAttributeValue(h, (pkcs11.CKA_LABEL,))[0]
                print '   s/n = %s' % hex_str(session.getAttributeValue(h, (pkcs11.CKA_SERIAL_NUMBER,))[0])
                print '   id = %s' % hex_str(session.getAttributeValue(h, (pkcs11.CKA_ID,))[0])
            elif cls == pkcs11.CKO_PRIVATE_KEY or cls == pkcs11.CKO_PUBLIC_KEY :
                print '   id = %s' % hex_str(session.getAttributeValue(h, (pkcs11.CKA_ID,))[0])
            #print '%d CKA_SERIAL_NUMBER = %s' % (h, repr(session.getAttributeValue(h, pkcs11.CKA_SERIAL_NUMBER)))
            #print '%d CKA_CERTIFICATE_TYPE = %s' % (h, struct.unpack("i", session.getAttributeValue(h, pkcs11.CKA_CERTIFICATE_TYPE))[0])

