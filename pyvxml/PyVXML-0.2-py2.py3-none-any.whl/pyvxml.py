# coding=utf-8


class PyVXML(object):
    """Simple VXML object creator class"""

    def __init__(self, **kwargs):
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        self.document = '<?xml version="1.0" encoding="UTF-8"?>\n'

        # start the vxml tag
        result = '<vxml'
        if kwargs.get('application', False):
            result += ' application="{}"'.format(kwargs.get('application'))
        if kwargs.get('xml_base', False):
            result += ' xml:base="{}"'.format(kwargs.get('xml_base'))
        if kwargs.get('xml:lang', False):
            result += ' xml_lang="{}"'.format(kwargs.get('xml_lang'))

        result += ' xmlns="http://www+w3+org/2001/vxml"'

        if kwargs.get('xmlns_xsi', False):
            result += ' xmlns:xsi="{}"'.format(kwargs.get('xmlns_xsi'))
        if kwargs.get('xsi_schemaLocation', False):
            result += ' xsi:schemaLocation="{}"'.format(kwargs.get('xsi_schemaLocation'))
        if kwargs.get('version', False):
            result += ' version="{}"'.format(kwargs.get('version'))

        result += '>\n'
        self.document += result

    def close_document(self):
        """

        :return:
        :rtype:
        """
        self.document += '</vxml>\n'

    def set_meta(self, name='', content='', http_equiv=''):
        """

        :param name:
        :type name:
        :param content:
        :type content:
        :param http_equiv:
        :type http_equiv:
        :return:
        :rtype:
        """
        result = '<meta'
        if name != '':
            result += ' name=' + format(name)
        if content != '':
            result += ' content=' + format(content)
        if http_equiv != '':
            result += ' http_equiv=' + format(http_equiv)

        self.document += ' />\n'

    def start_prompt(self, bargein='', bargeintype='', cond='', count='', xml_lang='', timeout='', xml_base=''):
        """
        
        :param bargein:
        :type bargein:
        :param bargeintype:
        :type bargeintype:
        :param cond:
        :type cond:
        :param count:
        :type count:
        :param xml_lang:
        :type xml_lang:
        :param timeout:
        :type timeout:
        :param xml_base:
        :type xml_base:
        :return:
        :rtype:
        """

        result = '<prompt'

        if bargein != '':
            result += ' bargein="' + bargein + '"'

        if bargeintype != '':
            result += ' bargeintype="' + bargeintype + '"'

        if cond != '':
            result += ' cond="' + cond + '"'

        if count != '':
            result += ' count="' + count + '"'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        if timeout != '':
            result += ' timeout="' + timeout + '"'

        if xml_base != '':
            result += ' xml:base="' + xml_base + '"'

        result += ' version = \'1.0\' '

        result += '>\n  '
        self.document += result

    def end_prompt(self):
        """
        
        :return:
        :rtype:
        """
        self.document += '</prompt>\n'

    def start_enumerate(self):
        """
        
        :return:
        :rtype:
        """
        self.document += '<enumerate>\n'

    def end_enumerate(self):
        """
        
        :return:
        :rtype:
        """
        self.document += '</enumerate>\n'

    def start_reprompt(self):
        """
        
        :return:
        :rtype:
        """
        self.document += '<reprompt />\n'

    def start_form(self, fid='', scope=''):
        """

        :param fid:
        :type fid:
        :param scope:
        :type scope:
        :return:
        :rtype:
        """

        result = '<form'

        if fid != '':
            result += ' id="' + fid + '"'

        if scope != '':
            result += ' scope="' + scope + '"'

        result += '>\n'
        self.document += result

    def end_form(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</form>\n'

    def start_menu(self, id='', scope='', dtmf=''):
        """
        
        :param id: 
        :type id: 
        :param scope: 
        :type scope: 
        :param dtmf: 
        :type dtmf: 
        :return:
        :rtype:
        """

        result = '<menu'

        if id != '':
            result += ' id="' + id + '"'

        if scope != '':
            result += ' scope="' + scope + '"'

        if dtmf != '':
            result += ' dtmf="' + dtmf + '"'

        result += '>\n  '
        self.document += result

    def end_menu(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</menu>\n'

    def start_choice(self, accept='', dtmf='', fetchaudio='', next='', fetchtimeout=''):
        """
        
        :param accept: 
        :type accept: 
        :param dtmf: 
        :type dtmf: 
        :param fetchaudio: 
        :type fetchaudio: 
        :return:
        :rtype:
        """

        result = '<choice'

        if accept != '':
            result += ' accept=' + accept + '"'

        if dtmf != '':
            result += ' dtmf="' + dtmf + '"'

        if fetchaudio != '':
            result += ' fetchaudio="' + fetchaudio + '"'

        if fetchtimeout != '':
            result += ' fetchtimeout="' + fetchtimeout + '"'

        if next != '':
            result += ' next="' + next + '"'

        result += '>\n  '
        self.document += result

    def end_choice(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</choice>\n'

    def start_p(self, xml_lang=''):
        """

        :param xml_lang:
        :type xml_lang:
        :return:
        :rtype:
        """

        result = '<p'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_p(self):
        """

        :return:
        :rtype:
        """

        self.document += '</p>\n'

    def start_s(self, xml_lang=''):
        """

        :param xml_lang:
        :type xml_lang:
        :return:
        :rtype:
        """

        result = '<s'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_s(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</s>\n'

    def start_voice(self, xml_lang='', gender='', age='', variant='', name=''):
        """
        
        :param xml_lang: 
        :type xml_lang: 
        :param gender: 
        :type gender: 
        :param age: 
        :type age: 
        :param variant: 
        :type variant: 
        :param name: 
        :type name: 
        :return:
        :rtype:
        """

        result = '<voice'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        if gender != '':
            result += ' gender="' + gender + '"'

        if age != '':
            result += ' age="' + age + '"'

        if variant != '':
            result += ' variant="' + variant + '"'

        if name != '':
            result += ' name="' + name + '"'

        result += '>\n  '
        self.document += result

    def end_voice(self):
        """

        :return:
        :rtype:
        """

        self.document += '</voice>\n'

    def start_prosody(self, pitch='', contour='', range='', rate='', duration='', volume=''):

        result = '<prosody'

        if pitch != '':
            result += ' pitch="' + pitch + '"'

        if contour != '':
            result += ' contour="' + contour + '"'

        if range != '':
            result += ' range="' + range + '"'

        if rate != '':
            result += ' rate="' + rate + '"'

        if duration != '':
            result += ' duration="' + duration + '"'

        if volume != '':
            result += ' volume="' + volume + '"'

        result += '>\n  '
        self.document += result

    def end_prosody(self):
        """

        :return:
        :rtype:
        """

        self.document += '</prosody>\n'

    def start_audio(self, src='', expr=''):
        """
        
        :param src: 
        :type src: 
        :param expr: 
        :type expr: 
        :return:
        :rtype:
        """

        result = '<audio'

        if src != '':
            result += ' src="' + src + '"'

        if expr != '':
            result += ' expr="' + expr + '"'

        result += '>\n  '
        self.document += result

    def end_audio(self):
        """

        :return:
        :rtype:
        """

        self.document += '</audio>\n'

    def start_desc(self, xml_lang=''):
        """
        
        :param xml_lang:
        :type xml_lang:
        :return:
        :rtype:
        """

        result = '<desc'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_desc(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</desc>\n'

    def start_emphasis(self, level=''):
        """
        
        :param level: 
        :type level: 
        :return:
        :rtype:
        """

        result = '<emphasis'

        if level != '':
            result += ' level="' + level + '"'

        result += '>\n  '
        self.document += result

    def end_emphasis(self):
        """

        :return:
        :rtype:
        """

        self.document += '</emphasis>\n'

    def start_say_as(self, interpret_as='', format='', detail=''):
        """
        
        :param interpret_as:
        :type interpret_as:
        :param format:
        :type format:
        :param detail:
        :type detail:
        :return:
        :rtype:
        """

        result = '<say-as'

        if interpret_as != '':
            result += ' interpret-as="' + interpret_as + '"'
        else:
            result += ' <!-- Error occured in say-as+ Need to pass "interpret-as"=+++ -->'

        if format != '':
            result += ' format="' + format + '"'

        if detail != '':
            result += ' detail="' + detail + '"'

        result += '>\n  '
        self.document += result

    def end_say_as(self):
        """

        :return:
        :rtype:
        """

        self.document += '</say-as>\n'

    def start_sub(self, alias=''):
        """
        
        :param alias: 
        :type alias: 
        :return:
        :rtype:
        """

        result = '<sub'

        if alias != '':
            result += ' alias="' + alias + '"'
        else:
            result += ' <!-- Error occured in sub+ Need to pass "alias"=+++ -->'

        result += '>\n  '
        self.document += result

    def end_sub(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</sub>\n'

    def start_phoneme(self, ph='', alphabet=''):
        """
        
        :param ph: 
        :type ph: 
        :param alphabet: 
        :type alphabet: 
        :return:
        :rtype:
        """

        result = '<phoneme'

        if ph != '':
            result += ' ph="' + ph + '"'
        else:
            result += ' <!-- Error occured in phoneme+ Need to pass "ph"=+++ -->'

        if alphabet != '':
            result += ' alphabet="' + alphabet + '"'

        result += '>\n  '
        self.document += result

    def end_phoneme(self):
        """

        :return:
        :rtype:
        """
        self.document += '</phoneme>\n'

    def start_break(self, time='', strength=''):
        """
        
        :param time: 
        :type time: 
        :param strength: 
        :type strength: 
        :return:
        :rtype:
        """

        result = '<break'

        if time != '':
            result += ' time="' + time + '"'

        if strength != '':
            result += ' strength="' + strength + '"'

        result += ">\n  "
        self.document += result

    def end_break(self):
        """

        :return:
        :rtype:
        """

        self.document += '</break>\n'

    def start_mark(self, name=''):
        """
        
        :param name:
        :type name:
        :return:
        :rtype:
        """

        result = '<mark'

        if name != '':
            result += ' name="' + name + '"'
        else:
            result += ' <!-- Error occured in mark+ Need to pass "name"=+++ -->'

        result += ">\n  "
        self.document += result

    def end_mark(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</mark>\n'

    def start_field(self, type='', slot='', modal=''):
        """
        
        :param type: 
        :type type: 
        :param slot: 
        :type slot: 
        :param modal: 
        :type modal: 
        :return:
        :rtype:
        """

        result = '<field'

        if type != '':
            result += ' type="' + type + '"'

        if slot != '':
            result += ' slot="' + slot + '"'

        if modal != '':
            result += ' modal="' + modal + '"'

        result += '>\n  '
        self.document += result

    def end_field(self):
        """

        :return:
        :rtype:
        """

        self.document += '</field>\n'

    def start_option(self, dtmf='', value=''):
        """
        
        :param dtmf: 
        :type dtmf: 
        :param value: 
        :type value: 
        :return:
        :rtype:
        """

        result = '<option'

        if dtmf != '':
            result += ' dtmf="' + dtmf + '"'

        if value != '':
            result += ' value="' + value + '"'

        result += '>\n  '
        self.document += result

    def end_option(self):
        """

        :return:
        :rtype:
        """

        self.document += '</option>\n'

    def start_var(self, name='', expr=''):
        """

        :param name:
        :type name:
        :param expr:
        :type expr:
        :return:
        :rtype:
        """

        result = '<var'

        if name != '':
            result += ' name="' + name + '"'
        else:
            result += ' <!-- Error occured in var+ Need to pass "name"=+++ -->'

        if expr != '':
            result += ' expr="' + expr + '"'

        result += ">\n  "
        self.document += result

    def end_var(self):
        """

        :return:
        :rtype:
        """
        self.document += '</var>\n'

    def start_assign(self, name='', expr=''):
        """

        :param name:
        :type name:
        :param expr:
        :type expr:
        :return:
        :rtype:
        """

        result = '<assign'

        if name != '':
            result += ' name="' + name + '"'
        else:
            result += ' <!-- Error occured in assign+ Need to pass "name"=+++ -->'

        if expr != '':
            result += ' expr="' + expr + '"'
        else:
            result += ' <!-- Error occured in assign+ Need to pass "expr"=+++ -->'

        result += ">\n  "
        self.document += result

    def end_assign(self):
        """

        :return:
        :rtype:
        """
        self.document += '</assign>\n'

    def start_clear(self, namelist=''):
        """

        :param namelist:
        :type namelist:
        :return:
        :rtype:
        """

        result = '<clear'

        if namelist != '':
            result += ' namelist="' + namelist + '"'

        result += ">\n  "
        self.document += result

    def end_clear(self):
        """

        :return:
        :rtype:
        """

        self.document += '</clear>\n'

    def start_value(self, expr=''):
        """

        :param expr:
        :type expr:
        :return:
        :rtype:
        """

        result = '<value'

        if expr != '':
            result += ' expr="' + expr + '"'
        else:
            result += ' <!-- Error occured in value+ Need to pass "expr"=+++ -->'

        result += ">\n  "
        self.document += result

    def end_value(self):
        """

        :return:
        :rtype:
        """

        self.document += '</value>\n'

    def start_catch(self, event='', count=''):
        """

        :param event:
        :type event:
        :return:
        :rtype:
        """
        result = '<catch'

        if event != '':
            result += ' event="' + event + '"'

        if count != '':
            result += ' count="' + count + '"'

        result += '>\n  '
        self.document += result

    def end_catch(self):
        """

        :return:
        :rtype:
        """

        self.document += '</catch>\n'

    def start_link(self, fetchaudio='', dtmf=''):
        """

        :param fetchaudio:
        :type fetchaudio:
        :param dtmf:
        :type dtmf:
        :return:
        :rtype:
        """

        result = '<link'

        if fetchaudio != '':
            result += ' fetchaudio="' + fetchaudio + '"'

        if dtmf != '':
            result += ' dtmf="' + dtmf + '"'

        result += '>\n  '
        self.document += result

    def end_link(self):
        """

        :return:
        :rtype:
        """

        self.document += '</link>\n'

    def start_throw(self):
        """

        :return:
        :rtype:
        """

        self.document += '<throw>\n'

    def end_throw(self):
        """

        :return:
        :rtype:
        """

        self.document += '</throw>\n'

    def start_ruleref(self, uri='', type='', special=''):
        """

        :param uri:
        :type uri:
        :param type:
        :type type:
        :param special:
        :type special:
        :return:
        :rtype:
        """

        result = '<ruleref'

        if uri != '':
            result += ' uri="' + uri + '"'

        if type != '':
            result += ' type="' + type + '"'

        if special != '':
            result += ' special="' + special + '"'

        result += ">\n  "
        self.document += result

    def end_ruleref(self):
        """

        :return:
        :rtype:
        """
        self.document += '</ruleref>\n'

    def start_token(self, xml_lang=''):
        """

        :param xml_lang:
        :type xml_lang:
        :return:
        :rtype:
        """

        result = '<token'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_token(self):
        """

        :return:
        :rtype:
        """

        self.document += '</token>\n'

    def start_tag(self):
        """

        :return:
        :rtype:
        """

        self.document += '<tag>\n'

    def end_tag(self):
        """

        :return:
        :rtype:
        """

        self.document += '</tag>\n'

    def start_one_of(self, xml_lang=''):

        result = '<one-of'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_one_of(self):
        """

        :return:
        :rtype:
        """

        self.document += '</one-of>\n'

    def start_item(self, repeat='', repeat_prob='', weight='', xml_lang=''):
        """

        :param repeat:
        :type repeat:
        :param repeat_prob:
        :type repeat_prob:
        :param weight:
        :type weight:
        :param xml_lang:
        :type xml_lang:
        :return:
        :rtype:
        """

        result = '<item'

        if repeat != '':
            result += ' repeat="' + repeat + '"'

        if repeat_prob != '':
            result += ' repeat-prob="' + repeat_prob + '"'

        if weight != '':
            result += ' weight="' + weight + '"'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        result += '>\n  '
        self.document += result

    def end_item(self):
        """

        :return:
        :rtype:
        """

        self.document += '</item>\n'

    def start_rule(self, id='', scope=''):
        """

        :param id:
        :type id:
        :param scope:
        :type scope:
        :return:
        :rtype:
        """

        result = '<rule'

        if id != '':
            result += ' id="' + id + '"'
        else:
            result += ' <!-- Error occured in rule+ Need to pass "id"=+++ -->'

        if scope != '':
            result += ' scope="' + scope + '"'

        result += '>\n  '
        self.document += result

    def end_rule(self):
        """

        :return:
        :rtype:
        """

        self.document += '</rule>\n'

    def start_example(self):
        """

        :return:
        :rtype:
        """

        self.document += '<example>\n'

    def end_example(self):
        """

        :return:
        :rtype:
        """

        self.document += '</example>\n'

    def start_lexicon(self, uri='', type=''):

        result = '<lexicon'

        if uri != '':
            result += ' uri="' + uri + '"'
        else:
            result += ' <!-- Error occured in lexicon+ Need to pass "uri"=+++ -->'

        if type != '':
            result += ' type="' + type + '"'

        result += ">\n  "
        self.document += result

    def end_lexicon(self):
        """

        :return:
        :rtype:
        """

        self.document += '</lexicon>\n'

    def start_grammar(self, scope='', src='', type='', weight='', tag_format='', xml_base='', version='',
                      xml_lang='', root='', mode=''):
        """

        :param scope:
        :type scope:
        :param src:
        :type src:
        :param type:
        :type type:
        :param weight:
        :type weight:
        :param tag_format:
        :type tag_format:
        :param xml_base:
        :type xml_base:
        :param version:
        :type version:
        :param xml_lang:
        :type xml_lang:
        :param root:
        :type root:
        :param mode:
        :type mode:
        :return:
        :rtype:
        """

        result = '<grammar'

        if scope != '':
            result += ' scope="' + scope + '"'

        if src != '':
            result += ' src="' + src + '"'

        if type != '':
            result += ' type="' + type + '"'

        if weight != '':
            result += ' weight="' + weight + '"'

        if tag_format != '':
            result += ' tag-format="' + tag_format + '"'

        if xml_base != '':
            result += ' xml:base="' + xml_base + '"'

        if version != '':
            result += ' version="' + version + '"'

        if xml_lang != '':
            result += ' xml:lang="' + xml_lang + '"'

        if root != '':
            result += ' root="' + root + '"'

        if mode != '':
            result += ' mode="' + mode + '"'

        result += '>\n  '
        self.document += result

    def end_grammar(self):
        """

        :return:
        :rtype:
        """

        self.document += '</grammar>\n'

    def start_record(self, type='', beep='', maxtime='', modal='', finalsilence='', dtmfterm=''):
        """

        :param type:
        :type type:
        :param beep:
        :type beep:
        :param maxtime:
        :type maxtime:
        :param modal:
        :type modal:
        :param finalsilence:
        :type finalsilence:
        :param dtmfterm:
        :type dtmfterm:
        :return:
        :rtype:
        """

        result = '<record'

        if type != '':
            result += ' type="' + type + '"'

        if beep != '':
            result += ' beep="' + beep + '"'

        if maxtime != '':
            result += ' maxtime="' + maxtime + '"'

        if modal != '':
            result += ' modal="' + modal + '"'

        if finalsilence != '':
            result += ' finalsilence="' + finalsilence + '"'

        if dtmfterm != '':
            result += ' dtmfterm="' + dtmfterm + '"'

        result += '>\n  '
        self.document += result

    def end_record(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '</record>\n'

    def start_disconnect(self):
        """
        
        :return:
        :rtype:
        """

        self.document += '<disconnect />\n'

    def start_transfer(self, dest='', destexpr='', bridge='', connecttimeout='', maxtime='', transferaudio='',
                       aai='', aaiexpr='', name=''):
        """
        
        :param dest: 
        :type dest: 
        :param destexpr: 
        :type destexpr: 
        :param bridge: 
        :type bridge: 
        :param connecttimeout: 
        :type connecttimeout: 
        :param maxtime: 
        :type maxtime: 
        :param transferaudio: 
        :type transferaudio: 
        :param aai: 
        :type aai: 
        :param aaiexpr: 
        :type aaiexpr: 
        :return:
        :rtype:
        """
        result = '<transfer'

        if dest != '':
            result += ' dest="' + dest + '"'

        if destexpr != '':
            result += ' destexpr="' + destexpr + '"'

        if bridge != '':
            result += ' bridge="' + bridge + '"'

        if connecttimeout != '':
            result += ' connecttimeout="' + connecttimeout + '"'

        if maxtime != '':
            result += ' maxtime="' + maxtime + '"'

        if transferaudio != '':
            result += ' transferaudio="' + transferaudio + '"'

        if aai != '':
            result += ' aai="' + aai + '"'

        if aaiexpr != '':
            result += ' aaiexpr="' + aaiexpr + '"'

        if name != '':
            result += ' name="' + name + '"'

        result += '>\n  '
        self.document += result

    def end_transfer(self):
        """

        :return:
        :rtype:
        """

        self.document += '</transfer>\n'

    def start_elseif(self):
        """

        :return:
        :rtype:
        """

        self.document += '<elseif>\n'

    def end_elseif(self):
        """

        :return:
        :rtype:
        """

        self.document += '</elseif>\n'

    def start_else(self):
        """

        :return:
        :rtype:
        """

        self.document += '<else />\n'

    def start_exit(self, expr='', namelist=''):
        """

        :param expr:
        :type expr:
        :param namelist:
        :type namelist:
        :return:
        :rtype:
        """

        result = '<exit'

        if expr != '':
            result += ' expr="' + expr + '"'

        if namelist != '':
            result += ' namelist="' + namelist + '"'

        result += ">\n  "
        self.document += result

    def end_exit(self):
        """

        :return:
        :rtype:
        """

        self.document += '</exit>\n'

    def start_filled(self, mode='', namelist=''):
        """

        :param mode:
        :type mode:
        :param namelist:
        :type namelist:
        :return:
        :rtype:
        """

        result = '<filled'

        if mode != '':
            result += ' mode="' + mode + '"'

        if namelist != '':
            result += ' namelist="' + namelist + '"'

        result += '>\n  '
        self.document += result

    def end_filled(self):
        """

        :return:
        :rtype:
        """

        self.document += '</filled>\n'

    def start_goto(self, fetchaudio='', expritem='', nextitem='', next='', expr='', fetchtimeout=''):
        """

        :param fetchaudio:
        :type fetchaudio:
        :param expritem:
        :type expritem:
        :param nextitem:
        :type nextitem:
        :return:
        :rtype:
        """

        result = '<goto'

        if fetchaudio != '':
            result += ' fetchaudio="' + fetchaudio + '"'

        if expritem != '':
            result += ' expritem="' + expritem + '"'

        if nextitem != '':
            result += ' nextitem="' + nextitem + '"'

        if next != '':
            result += ' next="' + next + '"'

        if expr != '':
            result += ' expr="' + expr + '"'

        if fetchtimeout != '':
            result += ' fetchtimeout="' + fetchtimeout + '"'

        result += ">\n  "
        self.document += result

    def end_goto(self):
        """

        :return:
        :rtype:
        """

        self.document += '</goto>\n'

    def start_param(self, name='', expr='', value='', valuetype='', type=''):
        """

        :param name:
        :type name:
        :param expr:
        :type expr:
        :param value:
        :type value:
        :param valuetype:
        :type valuetype:
        :param type:
        :type type:
        :return:
        :rtype:
        """

        result = '<param'

        if name != '':
            result += ' name="' + name + '"'
        else:
            result += ' <!-- Error occured in param+ Need to pass "name"=+++ -->'

        if expr != '':
            result += ' expr="' + expr + '"'

        if value != '':
            result += ' value="' + value + '"'

        if valuetype != '':
            result += ' valuetype="' + valuetype + '"'

        if type != '':
            result += ' type="' + type + '"'

        result += ">\n  "
        self.document += result

    def end_param(self):
        """

        :return:
        :rtype:
        """

        self.document += '</param>\n'


    def start_return(self, namelist=''):
        """

        :param namelist:
        :type namelist:
        :return:
        :rtype:
        """

        result = '<return'

        if namelist != '':
            result += ' namelist="' + namelist + '"'

        result += ">\n  "
        self.document += result

    def end_return(self):
        """

        :return:
        :rtype:
        """

        self.document += '</return>\n'

    def start_subdialog(self, name= '', src='', srcexpr='', fetchaudio='', fetchtimeout=''):
        """

        :param src:
        :type src:
        :param srcexpr:
        :type srcexpr:
        :param fetchaudio:
        :type fetchaudio:
        :return:
        :rtype:
        """

        result = '<subdialog'

        if name != '':
            result += ' name="' + name + '"'

        if src != '':
            result += ' src="' + src + '"'

        if srcexpr != '':
            result += ' srcexpr="' + srcexpr + '"'

        if fetchaudio != '':
            result += ' fetchaudio="' + fetchaudio + '"'

        if fetchtimeout != '':
            result += ' fetchtimeout="' + fetchtimeout + '"'

        result += '>\n  '
        self.document += result

    def end_subdialog(self):
        """

        :return:
        :rtype:
        """

        self.document += '</subdialog>\n'

    def start_submit(self, fetchaudio=''):
        """

        :param fetchaudio:
        :type fetchaudio:
        :return:
        :rtype:
        """

        result = '<submit'

        if fetchaudio != '':
            result += ' fetchaudio="' + fetchaudio + '"'

        result += ">\n  "
        self.document += result

    def end_submit(self):
        """

        :return:
        :rtype:
        """

        self.document += '</submit>\n'

    def start_log(self, label='', expr=''):
        """

        :param label:
        :type label:
        :param expr:
        :type expr:
        :return:
        :rtype:
        """

        result = '<log'

        if label != '':
            result += ' label="' + label + '"'

        if expr != '':
            result += ' expr="' + expr + '"'

        result += '>\n  '
        self.document += result

    def end_log(self):
        """

        :return:
        :rtype:
        """

        self.document += '</log>\n'

    def start_object(self, classid='', codebase='', data='', type='', codetype='', archive=''):
        """

        :param classid:
        :type classid:
        :param codebase:
        :type codebase:
        :param data:
        :type data:
        :param type:
        :type type:
        :param codetype:
        :type codetype:
        :param archive:
        :type archive:
        :return:
        :rtype:
        """

        result = '<object'

        if classid != '':
            result += ' classid="' + classid + '"'

        if codebase != '':
            result += ' codebase="' + codebase + '"'

        if data != '':
            result += ' data="' + data + '"'

        if type != '':
            result += ' type="' + type + '"'

        if codetype != '':
            result += ' codetype="' + codetype + '"'

        if archive != '':
            result += ' archive="' + archive + '"'

        result += '>\n  '
        self.document += result


    def end_object(self):
        """

        :return:
        :rtype:
        """

        self.document += '</object>\n'

    def start_property(self, name='', value=''):
        """

        :param name:
        :type name:
        :param value:
        :type value:
        :return:
        :rtype:
        """

        result = '<property'

        if name != '':
            result += ' name="' + name + '"'
        else:
            result += ' <!-- Error occured in property+ Need to pass "name"=+++ -->'

        if value != '':
            result += ' value="' + value + '"'
        else:
            result += ' <!-- Error occured in property+ Need to pass "value"=+++ -->'

        result += ">\n  "
        self.document += result

    def end_property(self):
        """

        :return:
        :rtype:
        """

        self.document += '</property>\n'

    def start_script(self):
        """

        :return:
        :rtype:
        """

        self.document += '<script>\n'

    def end_script(self):
        """

        :return:
        :rtype:
        """

        self.document += '</script>\n'

    def start_block(self, name='', expr='', cond=''):
        """

        :param name:
        :type name:
        :param expr:
        :type expr:
        :param cond:
        :type cond:
        :return:
        :rtype:
        """
        result = '<block'
        if name != '':
            result += " name=\"" + name + "\""

        if expr != '':
            result += " expr=\"" + expr + "\""

        if cond != '':
            result += " cond=\"" + cond + "\""

        result += ">\n  "

        self.document += result

    def end_block(self):
        """

        :return:
        :rtype:
        """
        self.document += '</block>\n'

    def write(self, text=''):
        """

        :param text:
        :type text:
        :return:
        :rtype:
        """

        self.document += ' ' + text + "\n" + ' '

    # def load(module,params)
    #
    #
    # if (ereg('::',module))
    #         d = explode('::',module)
    #         module = d[0]
    #         method = d[1]
    #
    #
    #     // Usage of absolute path to library
    #     if (ereg('WIN',PHP_OS))
    #         path = explode('\\', __FILE__)
    #      else path = explode('/', __FILE__)
    #     array_pop(path)
    #     path = implode('/',path)
    #
    #
    #     if (is_file'path/vxml_mods/module+class+php')
    #
    #         require_once'path/vxml_mods/module+class+php'
    #
    #         m = new module(this,params)
    #         if (isset(method))
    #             m->method(params)
    #

    def addscript(self, script):

        self.document += '<![CDATA[\n  "+script+"\n]]>\n'

    def generate(self):
        """

        :return:
        :rtype:
        """
        self.document += '</vxml>'
        return self.document

    def start_metadata(self):
        """

        :return:
        :rtype:
        """

        self.document += '<metadata>\n'

    def end_metadata(self):
        """

        :return:
        :rtype:
        """

        self.document += '</metadata>\n'

    def start_if(self, cond=""):
        """

        :param cond:
        :type cond:
        :return:
        :rtype:
        """

        result = '<if '
        if cond != '':
            result += " cond=\"" + cond + "\""

        result += ">\n  "

        self.document += result

    def end_if(self):
        """

        :return:
        :rtype:
        """
        self.document += '</if>\n'

    def start_else(self):
        """

        :param cond:
        :type cond:
        :return:
        :rtype:
        """

        result = '<else/>'
        result += ">\n  "

        self.document += result
