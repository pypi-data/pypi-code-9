# -*- coding: utf-8 -*-


#http://localization-guide.readthedocs.org/en/latest/l10n/pluralforms.html
__plural_forms = {}

#Acholi; nplurals=2; plural = (n > 1);
__plural_forms['ach'] = lambda n:(n > 1)

#Afrikaans; nplurals=2; plural = (n != 1);
__plural_forms['af'] = lambda n:(n != 1)

#Akan; nplurals=2; plural = (n > 1);
__plural_forms['ak'] = lambda n:(n > 1)

#Amharic; nplurals=2; plural = (n > 1);
__plural_forms['am'] = lambda n:(n > 1)

#Aragonese; nplurals=2; plural = (n != 1);
__plural_forms['an'] = lambda n:(n != 1)

#Angika; nplurals=2; plural = (n != 1);
__plural_forms['anp'] = lambda n:(n != 1)

#Arabic; nplurals=6; plural = (n == 0 ? 0 : n == 1 ? 1 : n == 2 ? 2 : n % 100 >= 3 && n % 100 <= 10 ? 3 : n % 100 >= 11 ? 4 : 5);
__plural_forms['ar'] = lambda n:(0 if n == 0 else 1 if n == 1 else 2 if n == 2 else 3 if n % 100 >= 3 and n % 100 <= 10 else 4 if n % 100 >= 11 else 5)

#Mapudungun; nplurals=2; plural = (n > 1);
__plural_forms['arn'] = lambda n:(n > 1)

#Assamese; nplurals=2; plural = (n != 1);
__plural_forms['as'] = lambda n:(n != 1)

#Asturian; nplurals=2; plural = (n != 1);
__plural_forms['ast'] = lambda n:(n != 1)

#Aymará; nplurals=1; plural = 0;
__plural_forms['ay'] = lambda n:0

#Azerbaijani; nplurals=2; plural = (n != 1);
__plural_forms['az'] = lambda n:(n != 1)

#Belarusian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['be'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Bulgarian; nplurals=2; plural = (n != 1);
__plural_forms['bg'] = lambda n:(n != 1)

#Bengali; nplurals=2; plural = (n != 1);
__plural_forms['bn'] = lambda n:(n != 1)

#Tibetan; nplurals=1; plural = 0;
__plural_forms['bo'] = lambda n:0

#Breton; nplurals=2; plural = (n > 1);
__plural_forms['br'] = lambda n:(n > 1)

#Bodo; nplurals=2; plural = (n != 1);
__plural_forms['brx'] = lambda n:(n != 1)

#Bosnian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['bs'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Catalan; nplurals=2; plural = (n != 1);
__plural_forms['ca'] = lambda n:(n != 1)

#Chiga; nplurals=1; plural = 0;
__plural_forms['cgg'] = lambda n:0

#Czech; nplurals=3; plural = (n == 1) ? 0 : (n >= 2 && n <= 4) ? 1 : 2;
__plural_forms['cs'] = lambda n:(0 if n == 1 else 1 if (n >= 2 and n <= 4) else 2)

#Kashubian; nplurals=3; plural = (n == 1) ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2;
__plural_forms['csb'] = lambda n:(0 if n == 1 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Welsh; nplurals=4; plural = (n == 1) ? 0 : (n == 2) ? 1 : (n != 8 && n != 11) ? 2 : 3;
__plural_forms['cy'] = lambda n:(0 if n == 1 else 1 if n == 2 else 2 if (n != 8 and n != 11) else 3)

#Danish; nplurals=2; plural = (n != 1);
__plural_forms['da'] = lambda n:(n != 1)

#German; nplurals=2; plural = (n != 1);
__plural_forms['de'] = lambda n:(n != 1)

#Dogri; nplurals=2; plural = (n != 1);
__plural_forms['doi'] = lambda n:(n != 1)

#Dzongkha; nplurals=1; plural = 0;
__plural_forms['dz'] = lambda n:0

#Greek; nplurals=2; plural = (n != 1);
__plural_forms['el'] = lambda n:(n != 1)

#English; nplurals=2; plural = (n != 1);
__plural_forms['en'] = lambda n:(n != 1)

#Esperanto; nplurals=2; plural = (n != 1);
__plural_forms['eo'] = lambda n:(n != 1)

#Spanish; nplurals=2; plural = (n != 1);
__plural_forms['es'] = lambda n:(n != 1)

#Argentinean; Spanish nplurals=2; plural = (n != 1);
__plural_forms['es_AR'] = lambda n:(n != 1)

#Estonian; nplurals=2; plural = (n != 1);
__plural_forms['et'] = lambda n:(n != 1)

#Basque; nplurals=2; plural = (n != 1);
__plural_forms['eu'] = lambda n:(n != 1)

#Persian; nplurals=1; plural = 0;
__plural_forms['fa'] = lambda n:0

#Fulah; nplurals=2; plural = (n != 1);
__plural_forms['ff'] = lambda n:(n != 1)

#Finnish; nplurals=2; plural = (n != 1);
__plural_forms['fi'] = lambda n:(n != 1)

#Filipino; nplurals=2; plural = (n > 1);
__plural_forms['fil'] = lambda n:(n > 1)

#Faroese; nplurals=2; plural = (n != 1);
__plural_forms['fo'] = lambda n:(n != 1)

#French; nplurals=2; plural = (n > 1);
__plural_forms['fr'] = lambda n:(n > 1)

#Friulian; nplurals=2; plural = (n != 1);
__plural_forms['fur'] = lambda n:(n != 1)

#Frisian; nplurals=2; plural = (n != 1);
__plural_forms['fy'] = lambda n:(n != 1)

#Irish; nplurals=5; plural = n == 1 ? 0 : n == 2 ? 1 : (n > 2 && n < 7) ? 2 :(n > 6 && n < 11) ? 3 : 4;
__plural_forms['ga'] = lambda n:(0 if n == 1 else 1 if n == 2 else 2 if (n > 2 and n < 7) else 3 if (n > 6 and n < 11) else 4)

#Scottish; Gaelic nplurals=4; plural = (n == 1 || n == 11) ? 0 : (n == 2 || n == 12) ? 1 : (n > 2 && n < 20) ? 2 : 3;
__plural_forms['gd'] = lambda n:(0 if (n == 1 or n == 11) else 1 if (n == 2 or n == 12) else 2 if (n > 2 and n < 20) else 3)

#Galician; nplurals=2; plural = (n != 1);
__plural_forms['gl'] = lambda n:(n != 1)

#Gujarati; nplurals=2; plural = (n != 1);
__plural_forms['gu'] = lambda n:(n != 1)

#Gun; nplurals=2; plural = (n > 1);
__plural_forms['gun'] = lambda n:(n > 1)

#Hausa; nplurals=2; plural = (n != 1);
__plural_forms['ha'] = lambda n:(n != 1)

#Hebrew; nplurals=2; plural = (n != 1);
__plural_forms['he'] = lambda n:(n != 1)

#Hindi; nplurals=2; plural = (n != 1);
__plural_forms['hi'] = lambda n:(n != 1)

#Chhattisgarhi; nplurals=2; plural = (n != 1);
__plural_forms['hne'] = lambda n:(n != 1)

#Croatian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
#__plural_forms['hr'] = lambda n:(n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2)
__plural_forms['hr'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Hungarian; nplurals=2; plural = (n != 1);
__plural_forms['hu'] = lambda n:(n != 1)

#Armenian; nplurals=2; plural = (n != 1);
__plural_forms['hy'] = lambda n:(n != 1)

#erlingua; nplurals=2; plural = (n != 1);
__plural_forms['ia'] = lambda n:(n != 1)

#Indonesian; nplurals=1; plural = 0;
__plural_forms['id'] = lambda n:0

#Icelandic; nplurals=2; plural = (n % 10 != 1 || n % 100 == 11);
__plural_forms['is'] = lambda n:(n % 10 != 1 or n % 100 == 11)

#Italian; nplurals=2; plural = (n != 1);
__plural_forms['it'] = lambda n:(n != 1)

#Japanese; nplurals=1; plural = 0;
__plural_forms['ja'] = lambda n:0

#Lojban; nplurals=1; plural = 0;
__plural_forms['jbo'] = lambda n:0

#Javanese; nplurals=2; plural = (n != 0);
__plural_forms['jv'] = lambda n:(n != 0)

#Georgian; nplurals=1; plural = 0;
__plural_forms['ka'] = lambda n:0

#Kazakh; nplurals=1; plural = 0;
__plural_forms['kk'] = lambda n:0

#Greenlandic; nplurals=2; plural = (n != 1);
__plural_forms['kl'] = lambda n:(n != 1)

#Khmer; nplurals=1; plural = 0;
__plural_forms['km'] = lambda n:0

#Kannada; nplurals=2; plural = (n != 1);
__plural_forms['kn'] = lambda n:(n != 1)

#Korean; nplurals=1; plural = 0;
__plural_forms['ko'] = lambda n:0

#Kurdish; nplurals=2; plural = (n != 1);
__plural_forms['ku'] = lambda n:(n != 1)

#Cornish; nplurals=4; plural = (n == 1) ? 0 : (n == 2) ? 1 : (n  ==  3) ? 2 : 3;
__plural_forms['kw'] = lambda n:(0 if (n == 1) else 1 if (n == 2) else 2 if (n == 3) else 3)

#Kyrgyz; nplurals=1; plural = 0;
__plural_forms['ky'] = lambda n:0

#Letzeburgesch; nplurals=2; plural = (n != 1);
__plural_forms['lb'] = lambda n:(n != 1)

#Lingala; nplurals=2; plural = (n > 1);
__plural_forms['ln'] = lambda n:(n > 1)

#Lao; nplurals=1; plural = 0;
__plural_forms['lo'] = lambda n:0

#Lithuanian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['lt'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Latvian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n != 0 ? 1 : 2);
__plural_forms['lv'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n != 0 else 2)

#Maithili; nplurals=2; plural = (n != 1);
__plural_forms['mai'] = lambda n:(n != 1)

#Mauritian; Creole nplurals=2; plural = (n > 1);
__plural_forms['mfe'] = lambda n:(n > 1)

#Malagasy; nplurals=2; plural = (n > 1);
__plural_forms['mg'] = lambda n:(n > 1)

#Maori; nplurals=2; plural = (n > 1);
__plural_forms['mi'] = lambda n:(n > 1)

#Macedonian; nplurals=2; plural =  n == 1 || n % 10 == 1 ? 0 : 1;
#__plural_forms['mk'] = lambda n: n == 1 or n % 10 == 1 ? 0 : 1 #Can’t be correct needs a 2 somewhere
__plural_forms['mk'] = lambda n:(0 if n == 1 or n % 10 == 1 else 1)

#Malayalam; nplurals=2; plural = (n != 1);
__plural_forms['ml'] = lambda n:(n != 1)

#Mongolian; nplurals=2; plural = (n != 1);
__plural_forms['mn'] = lambda n:(n != 1)

#Manipuri; nplurals=2; plural = (n != 1);
__plural_forms['mni'] = lambda n:(n != 1)

#Mandinka; nplurals=3; plural = (n == 0 ? 0 : n == 1 ? 1 : 2);
__plural_forms['mnk'] = lambda n:(0 if n == 0 else 1 if n == 1 else 2)

#Marathi; nplurals=2; plural = (n != 1);
__plural_forms['mr'] = lambda n:(n != 1)

#Malay; nplurals=1; plural = 0;
__plural_forms['ms'] = lambda n:0

#Maltese; nplurals=4; plural = (n == 1 ? 0 : n == 0 || ( n % 100>1 && n % 100 < 11) ? 1 : (n % 100>10 && n % 100 < 20 ) ? 2 : 3);
__plural_forms['mt'] = lambda n:(0 if n == 1 else 1 if n == 0 or (n % 100 > 1 and n % 100 < 11) else 2 if (n % 100 > 10 and n % 100 < 20) else 3)

#Burmese; nplurals=1; plural = 0;
__plural_forms['my'] = lambda n:0

#Nahuatl; nplurals=2; plural = (n != 1);
__plural_forms['nah'] = lambda n:(n != 1)

#Neapolitan; nplurals=2; plural = (n != 1);
__plural_forms['nap'] = lambda n:(n != 1)

#Norwegian; Bokmal nplurals=2; plural = (n != 1);
__plural_forms['nb'] = lambda n:(n != 1)

#Nepali; nplurals=2; plural = (n != 1);
__plural_forms['ne'] = lambda n:(n != 1)

#Dutch; nplurals=2; plural = (n != 1);
__plural_forms['nl'] = lambda n:(n != 1)

#Norwegian; Nynorsk nplurals=2; plural = (n != 1);
__plural_forms['nn'] = lambda n:(n != 1)

#Norwegian; (old code) nplurals=2; plural = (n != 1);
__plural_forms['no'] = lambda n:(n != 1)

#Northern; Sotho nplurals=2; plural = (n != 1);
__plural_forms['nso'] = lambda n:(n != 1)

#Occitan; nplurals=2; plural = (n > 1);
__plural_forms['oc'] = lambda n:(n > 1)

#Oriya; nplurals=2; plural = (n != 1);
__plural_forms['or'] = lambda n:(n != 1)

#Punjabi; nplurals=2; plural = (n != 1);
__plural_forms['pa'] = lambda n:(n != 1)

#Papiamento; nplurals=2; plural = (n != 1);
__plural_forms['pap'] = lambda n:(n != 1)

#Polish; nplurals=3; plural = (n == 1 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['pl'] = lambda n:(0 if n == 1 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Piemontese; nplurals=2; plural = (n != 1);
__plural_forms['pms'] = lambda n:(n != 1)

#Pashto; nplurals=2; plural = (n != 1);
__plural_forms['ps'] = lambda n:(n != 1)

#Portuguese; nplurals=2; plural = (n != 1);
__plural_forms['pt'] = lambda n:(n != 1)

#Brazilian; Portuguese nplurals=2; plural = (n > 1);
__plural_forms['pt_BR'] = lambda n:(n > 1)

#Romansh; nplurals=2; plural = (n != 1);
__plural_forms['rm'] = lambda n:(n != 1)

#Romanian; nplurals=3; plural = (n == 1 ? 0 : (n == 0 || (n % 100 > 0 && n % 100 < 20)) ? 1 : 2);
__plural_forms['ro'] = lambda n:(0 if n == 1 else 1 if (n == 0 or (n % 100 > 0 and n % 100 < 20)) else 2)

#Russian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['ru'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Kinyarwanda; nplurals=2; plural = (n != 1);
__plural_forms['rw'] = lambda n:(n != 1)

#Yakut; nplurals=1; plural = 0;
__plural_forms['sah'] = lambda n:0

#Santali; nplurals=2; plural = (n != 1);
__plural_forms['sat'] = lambda n:(n != 1)

#Scots; nplurals=2; plural = (n != 1);
__plural_forms['sco'] = lambda n:(n != 1)

#Sindhi; nplurals=2; plural = (n != 1);
__plural_forms['sd'] = lambda n:(n != 1)

#Northern; Sami nplurals=2; plural = (n != 1);
__plural_forms['se'] = lambda n:(n != 1)

#Sinhala; nplurals=2; plural = (n != 1);
__plural_forms['si'] = lambda n:(n != 1)

#Slovak; nplurals=3; plural = (n == 1) ? 0 : (n >= 2 && n <= 4) ? 1 : 2;
__plural_forms['sk'] = lambda n:(0 if n == 1 else 1 if (n >= 2 and n <= 4) else 2)

#Slovenian; nplurals=4; plural = (n % 100 == 1 ? 1 : n % 100 == 2 ? 2 : n % 100 == 3 || n % 100 == 4 ? 3 : 0);
__plural_forms['sl'] = lambda n:(1 if n % 100 == 1 else 2 if n % 100 == 2 else 3 if n % 100 == 3 or n % 100 == 4 else 0)

#Somali; nplurals=2; plural = (n != 1);
__plural_forms['so'] = lambda n:(n != 1)

#Songhay; nplurals=2; plural = (n != 1);
__plural_forms['son'] = lambda n:(n != 1)

#Albanian; nplurals=2; plural = (n != 1);
__plural_forms['sq'] = lambda n:(n != 1)

#Serbian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['sr'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Sundanese; nplurals=1; plural = 0;
__plural_forms['su'] = lambda n:0

#Swedish; nplurals=2; plural = (n != 1);
__plural_forms['sv'] = lambda n:(n != 1)

#Swahili; nplurals=2; plural = (n != 1);
__plural_forms['sw'] = lambda n:(n != 1)

#Tamil; nplurals=2; plural = (n != 1);
__plural_forms['ta'] = lambda n:(n != 1)

#Telugu; nplurals=2; plural = (n != 1);
__plural_forms['te'] = lambda n:(n != 1)

#Tajik; nplurals=2; plural = (n > 1);
__plural_forms['tg'] = lambda n:(n > 1)

#Thai; nplurals=1; plural = 0;
__plural_forms['th'] = lambda n:0

#Tigrinya; nplurals=2; plural = (n > 1);
__plural_forms['ti'] = lambda n:(n > 1)

#Turkmen; nplurals=2; plural = (n != 1);
__plural_forms['tk'] = lambda n:(n != 1)

#Turkish; nplurals=2; plural = (n > 1);
__plural_forms['tr'] = lambda n:(n > 1)

#Tatar; nplurals=1; plural = 0;
__plural_forms['tt'] = lambda n:0

#Uyghur; nplurals=1; plural = 0;
__plural_forms['ug'] = lambda n:0

#Ukrainian; nplurals=3; plural = (n % 10 == 1 && n % 100 != 11 ? 0 : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 1 : 2);
__plural_forms['uk'] = lambda n:(0 if n % 10 == 1 and n % 100 != 11 else 1 if n % 10 >= 2 and n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20) else 2)

#Urdu; nplurals=2; plural = (n != 1);
__plural_forms['ur'] = lambda n:(n != 1)

#Uzbek; nplurals=2; plural = (n > 1);
__plural_forms['uz'] = lambda n:(n > 1)

#Vietnamese; nplurals=1; plural = 0;
__plural_forms['vi'] = lambda n:0

#Walloon; nplurals=2; plural = (n > 1);
__plural_forms['wa'] = lambda n:(n > 1)

#Wolof; nplurals=1; plural = 0;
__plural_forms['wo'] = lambda n:0

#Yoruba; nplurals=2; plural = (n != 1);
__plural_forms['yo'] = lambda n:(n != 1)

#Chinese; [2] nplurals=1; plural = 0;
__plural_forms['zh'] = lambda n:0

#Chinese; [3] nplurals=2; plural = (n > 1);
__plural_forms['zh'] = lambda n:(n > 1)


def get_plural_forms():
    
    return __plural_forms.copy()
    

def get_plural_form(language_code, n):
    
    plural_key = language_code.lower()
    plural_form = __plural_forms.get(plural_key, None)
    
    if not plural_form:
        
        plural_key = plural_key.split('-')[0]
        plural_form = __plural_forms.get(plural_key, None)
        
        if not plural_form:
            
            plural_key = plural_key.split('_')[0]
            plural_form = __plural_forms.get(plural_key, None)
            
            if not plural_form:
                raise ValueError('Invalid/Unsupported language code: %s' % (language_code, ))
                
    return int(plural_form( n ))
    
    