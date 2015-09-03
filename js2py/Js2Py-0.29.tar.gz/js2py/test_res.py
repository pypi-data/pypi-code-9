import js2py.pyjs, sys
# Redefine builtin objects... Do you have a better idea?
for m in sys.modules.keys():
	if m.startswith('js2py'):
		del sys.modules[m]
del js2py.pyjs
del js2py
from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([u'dateFormat'])
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments}, var)
    var.registers([u'timezone', u'token', u'timezoneClip', u'pad'])
    var.put(u'token', JsRegExp(u'/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\x01?|[LloSZ]|"[^"]*"|\'[^\']*\'/g'))
    var.put(u'timezone', JsRegExp(u'/\x08(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]d{4})?)\x08/g'))
    var.put(u'timezoneClip', JsRegExp(u'/[^-+dA-Z]/g'))
    @Js
    def PyJs_anonymous_1_(val, len, this, arguments, var=var):
        var = Scope({u'this':this, u'len':len, u'val':val, u'arguments':arguments}, var)
        var.registers([u'len', u'val'])
        var.put(u'val', var.get(u'String')(var.get(u'val')))
        var.put(u'len', (var.get(u'len') or Js(2.0)))
        while (var.get(u'val').get(u'length')<var.get(u'len')):
            var.put(u'val', (Js(u'0')+var.get(u'val')))
        return var.get(u'val')
    PyJs_anonymous_1_._set_name(u'anonymous')
    var.put(u'pad', PyJs_anonymous_1_)
    @Js
    def PyJs_anonymous_2_(date, mask, utc, this, arguments, var=var):
        var = Scope({u'date':date, u'utc':utc, u'this':this, u'mask':mask, u'arguments':arguments}, var)
        var.registers([u'M', u'd', u'utc', u'dF', u'H', u'm', u'L', u'o', u'date', u's', u'flags', u'y', u'mask', u'_', u'D'])
        var.put(u'dF', var.get(u'dateFormat'))
        if (((var.get(u'arguments').get(u'length')==Js(1.0)) and (var.get(u'Object').get(u'prototype').get(u'toString').callprop(u'call', var.get(u'date'))==Js(u'[object String]'))) and JsRegExp(u'/d/').callprop(u'test', var.get(u'date')).neg()):
            var.put(u'mask', var.get(u'date'))
            var.put(u'date', var.get(u'undefined'))
        var.put(u'date', (var.get(u'Date').create(var.get(u'date')) if var.get(u'date') else var.get(u'Date').create()))
        if var.get(u'isNaN')(var.get(u'date')):
            PyJsTempException = JsToPyException(var.get(u'SyntaxError')(Js(u'invalid date')))
            raise PyJsTempException
        var.put(u'mask', var.get(u'String')(((var.get(u'dF').get(u'masks').get(var.get(u'mask')) or var.get(u'mask')) or var.get(u'dF').get(u'masks').get(u'default'))))
        if (var.get(u'mask').callprop(u'slice', Js(0.0), Js(4.0))==Js(u'UTC:')):
            var.put(u'mask', var.get(u'mask').callprop(u'slice', Js(4.0)))
            var.put(u'utc', var.get(u'true'))
        var.put(u'_', (Js(u'getUTC') if var.get(u'utc') else Js(u'get')))
        var.put(u'd', var.get(u'date').callprop((var.get(u'_')+Js(u'Date'))))
        var.put(u'D', var.get(u'date').callprop((var.get(u'_')+Js(u'Day'))))
        var.put(u'm', var.get(u'date').callprop((var.get(u'_')+Js(u'Month'))))
        var.put(u'y', var.get(u'date').callprop((var.get(u'_')+Js(u'FullYear'))))
        var.put(u'H', var.get(u'date').callprop((var.get(u'_')+Js(u'Hours'))))
        var.put(u'M', var.get(u'date').callprop((var.get(u'_')+Js(u'Minutes'))))
        var.put(u's', var.get(u'date').callprop((var.get(u'_')+Js(u'Seconds'))))
        var.put(u'L', var.get(u'date').callprop((var.get(u'_')+Js(u'Milliseconds'))))
        var.put(u'o', (Js(0.0) if var.get(u'utc') else var.get(u'date').callprop(u'getTimezoneOffset')))
        PyJs_Object_3_ = Js({u'd':var.get(u'd'),u'dd':var.get(u'pad')(var.get(u'd')),u'ddd':var.get(u'dF').get(u'i18n').get(u'dayNames').get(var.get(u'D')),u'dddd':var.get(u'dF').get(u'i18n').get(u'dayNames').get((var.get(u'D')+Js(7.0))),u'm':(var.get(u'm')+Js(1.0)),u'mm':var.get(u'pad')((var.get(u'm')+Js(1.0))),u'mmm':var.get(u'dF').get(u'i18n').get(u'monthNames').get(var.get(u'm')),u'mmmm':var.get(u'dF').get(u'i18n').get(u'monthNames').get((var.get(u'm')+Js(12.0))),u'yy':var.get(u'String')(var.get(u'y')).callprop(u'slice', Js(2.0)),u'yyyy':var.get(u'y'),u'h':((var.get(u'H')%Js(12.0)) or Js(12.0)),u'hh':var.get(u'pad')(((var.get(u'H')%Js(12.0)) or Js(12.0))),u'H':var.get(u'H'),u'HH':var.get(u'pad')(var.get(u'H')),u'M':var.get(u'M'),u'MM':var.get(u'pad')(var.get(u'M')),u's':var.get(u's'),u'ss':var.get(u'pad')(var.get(u's')),u'l':var.get(u'pad')(var.get(u'L'), Js(3.0)),u'L':var.get(u'pad')((var.get(u'Math').callprop(u'round', (var.get(u'L')/Js(10.0))) if (var.get(u'L')>Js(99.0)) else var.get(u'L'))),u't':(Js(u'a') if (var.get(u'H')<Js(12.0)) else Js(u'p')),u'tt':(Js(u'am') if (var.get(u'H')<Js(12.0)) else Js(u'pm')),u'T':(Js(u'A') if (var.get(u'H')<Js(12.0)) else Js(u'P')),u'TT':(Js(u'AM') if (var.get(u'H')<Js(12.0)) else Js(u'PM')),u'Z':(Js(u'UTC') if var.get(u'utc') else (var.get(u'String')(var.get(u'date')).callprop(u'match', var.get(u'timezone')) or Js([Js(u'')])).callprop(u'pop').callprop(u'replace', var.get(u'timezoneClip'), Js(u''))),u'o':((Js(u'-') if (var.get(u'o')>Js(0.0)) else Js(u'+'))+var.get(u'pad')(((var.get(u'Math').callprop(u'floor', (var.get(u'Math').callprop(u'abs', var.get(u'o'))/Js(60.0)))*Js(100.0))+(var.get(u'Math').callprop(u'abs', var.get(u'o'))%Js(60.0))), Js(4.0))),u'S':Js([Js(u'th'), Js(u'st'), Js(u'nd'), Js(u'rd')]).get((Js(0.0) if ((var.get(u'd')%Js(10.0))>Js(3.0)) else (((((var.get(u'd')%Js(100.0))-(var.get(u'd')%Js(10.0)))!=Js(10.0))*var.get(u'd'))%Js(10.0))))})
        var.put(u'flags', PyJs_Object_3_)
        @Js
        def PyJs_anonymous_4_(PyJsArg_2430_, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'$0':PyJsArg_2430_}, var)
            var.registers([u'$0'])
            return (var.get(u'flags').get(var.get(u'$0')) if var.get(u'flags').contains(var.get(u'$0')) else var.get(u'$0').callprop(u'slice', Js(1.0), (var.get(u'$0').get(u'length')-Js(1.0))))
        PyJs_anonymous_4_._set_name(u'anonymous')
        return var.get(u'mask').callprop(u'replace', var.get(u'token'), PyJs_anonymous_4_)
    PyJs_anonymous_2_._set_name(u'anonymous')
    return PyJs_anonymous_2_
PyJs_anonymous_0_._set_name(u'anonymous')
var.put(u'dateFormat', PyJs_anonymous_0_())
PyJs_Object_5_ = Js({u'default':Js(u'ddd mmm dd yyyy HH:MM:ss'),u'shortDate':Js(u'm/d/yy'),u'mediumDate':Js(u'mmm d, yyyy'),u'longDate':Js(u'mmmm d, yyyy'),u'fullDate':Js(u'dddd, mmmm d, yyyy'),u'shortTime':Js(u'h:MM TT'),u'mediumTime':Js(u'h:MM:ss TT'),u'longTime':Js(u'h:MM:ss TT Z'),u'isoDate':Js(u'yyyy-mm-dd'),u'isoTime':Js(u'HH:MM:ss'),u'isoDateTime':Js(u"yyyy-mm-dd'T'HH:MM:ss"),u'isoUtcDateTime':Js(u"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'")})
var.get(u'dateFormat').put(u'masks', PyJs_Object_5_)
PyJs_Object_6_ = Js({u'dayNames':Js([Js(u'Sun'), Js(u'Mon'), Js(u'Tue'), Js(u'Wed'), Js(u'Thu'), Js(u'Fri'), Js(u'Sat'), Js(u'Sunday'), Js(u'Monday'), Js(u'Tuesday'), Js(u'Wednesday'), Js(u'Thursday'), Js(u'Friday'), Js(u'Saturday')]),u'monthNames':Js([Js(u'Jan'), Js(u'Feb'), Js(u'Mar'), Js(u'Apr'), Js(u'May'), Js(u'Jun'), Js(u'Jul'), Js(u'Aug'), Js(u'Sep'), Js(u'Oct'), Js(u'Nov'), Js(u'Dec'), Js(u'January'), Js(u'February'), Js(u'March'), Js(u'April'), Js(u'May'), Js(u'June'), Js(u'July'), Js(u'August'), Js(u'September'), Js(u'October'), Js(u'November'), Js(u'December')])})
var.get(u'dateFormat').put(u'i18n', PyJs_Object_6_)
@Js
def PyJs_anonymous_7_(mask, utc, this, arguments, var=var):
    var = Scope({u'this':this, u'utc':utc, u'mask':mask, u'arguments':arguments}, var)
    var.registers([u'utc', u'mask'])
    return var.get(u'dateFormat')(var.get(u"this"), var.get(u'mask'), var.get(u'utc'))
PyJs_anonymous_7_._set_name(u'anonymous')
var.get(u'Date').get(u'prototype').put(u'format', PyJs_anonymous_7_)
var.put(u'today', var.get(u'Date').create(Js(4393494334343434.0)))
var.get(u'today').get(u'toISOString')
