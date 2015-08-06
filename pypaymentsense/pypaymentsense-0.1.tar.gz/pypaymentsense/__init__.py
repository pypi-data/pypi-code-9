# coding: utf-8
import re
import hashlib
import datetime
import pytz
import requests

# Function to test whether a variable is a number or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# All variables with None are obviously not required by the API, but must
# be passed as None in order for the hashing to work as expected.
def build_hash(PreSharedKey, MerchantID, Password, Amount,
	CurrencyCode, EchoAVSCheckResult, EchoCV2CheckResult, 
	EchoThreeDSecureAuthenticationCheckResult, EchoCardType, 
	OrderID, TransactionType, CallbackURL, EmailAddressEditable, 
	PhoneNumberEditable, CV2Mandatory, Address1Mandatory, CityMandatory, 
	PostCodeMandatory, StateMandatory, CountryMandatory, ResultDeliveryMethod,
	PaymentFormDisplaysResult, TransactionDateTime,	 
	OrderDescription, CustomerName, Address1, Address2, 
	Address3, Address4, City, State, PostCode, 
	CountryCode, EmailAddress, PhoneNumber,
	ServerResultURL):

	# This is the order the variables must be passed to payment sense,
	# where None has been defined, these are the non required variables

	# PreSharedKey needs to validation

	if len(MerchantID) > 15:
		raise Exception("MerchantID must be no more than 15 characters")

	# Password needs to validation

	amount_test = is_number(Amount)
	if amount_test == False:
		raise Exception("Amount need to be a numerical value")

	# We hard code CurrencyCode to 826/GBP
	CurrencyCode = 826

	echo_avs_check = isinstance(EchoAVSCheckResult, bool)
	if echo_avs_check == False:
		raise Exception("EchoAVSCheckResult accepts True or False")

	echo_cv2_check = isinstance(EchoCV2CheckResult, bool)
	if echo_cv2_check == False:
		raise Exception("EchoCV2CheckResult accepts True or False")

	echo_3dcheck = isinstance(EchoThreeDSecureAuthenticationCheckResult, bool)
	if echo_3dcheck == False:
		raise Exception(
			"EchoThreeDSecureAuthenticationCheckResult accepts True or False")

	echo_card_type_check = isinstance(EchoCardType, bool)
	if echo_card_type_check == False:
		raise Exception("EchoCardType accepts True or False")


	if len(OrderID) > 50:
		raise Exception("OrderID must be no more than 15 characters")
	

	if TransactionType == "SALE" or "PREAUTH":
		pass
	else:
		raise Exception("TransactionType accepts 'SALE' or 'PREAUTH'")	

	# CallbackURL doesn't really need any validation

	if ServerResultURL == None:
		ServerResultURL = ""

	if OrderDescription == None:
		OrderDescription = ""
	elif len(OrderDescription) > 256:
		raise Exception(
			"OrderDescription must be no more than 256 characters")

	if CustomerName == None:
		CustomerName = ""
	elif len(CustomerName) > 100:
		raise Exception(
			"CustomerName must be no more than 100 characters")

	if Address1 == None:
		Address1 = ""
	elif len(Address1) > 100:
		raise Exception(
			"Address1 must be no more than 100 characters")

	if Address2 == None:
		Address2 = ""
	elif len(Address2) > 50:
		raise Exception(
			"Address1 must be no more than 50 characters")

	if Address3 == None:
		Address3 = ""
	elif len(Address3) > 50:
		raise Exception(
			"Address3 must be no more than 50 characters")

	if Address4 == None:
		Address4 = ""
	elif len(Address4) > 50:
		raise Exception(
			"Address4 must be no more than 50 characters")

	if City == None:
		City = ""
	elif len(City) > 50:
		raise Exception(
			"City must be no more than 50 characters")

	if State == None:
		State = ""
	elif len(State) > 50:
		raise Exception(
			"State must be no more than 50 characters")

	if PostCode == None:
		PostCode = ""
	elif len(PostCode) > 50:
		raise Exception(
			"PostCode must be no more than 50 characters")

	if CountryCode == None:
		CountryCode = ""
	elif len(CountryCode) > 3:
		raise Exception(
			"CountryCode must be no more than 50 characters")
	else:
		cc_test = is_number(CountryCode)
		if cc_test == False:
			raise Exception("CountryCode need to be a numerical value")

	if EmailAddress == None:
		EmailAddress = ""
	elif len(EmailAddress) > 100:
		raise Exception(
			"EmailAddress must be no more than 100 characters")
	else:
		email_test = re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b',
					 EmailAddress)
		# if email is invalid, send to luke and he can investigate
		if email_test == None:
			raise Exception("EmailAddress is an invalid format")

	if PhoneNumber == None:
		PhoneNumber = ""
	elif len(PhoneNumber) > 30:
		raise Exception(
			"PostCode must be no more than 30 characters")

	email_edit_check = isinstance(EmailAddressEditable, bool)
	if email_edit_check == False:
		raise Exception("EmailAddressEditable accepts True or False")

	phone_edit_check = isinstance(PhoneNumberEditable, bool)
	if phone_edit_check == False:
		raise Exception("PhoneNumberEditable accepts True or False")

	cv2_man_check = isinstance(CV2Mandatory, bool)
	if cv2_man_check == False:
		raise Exception("CV2Mandatory accepts True or False")

	addr1_man_check = isinstance(Address1Mandatory, bool)
	if addr1_man_check == False:
		raise Exception("Address1Mandatory accepts True or False")

	city_man_check = isinstance(CityMandatory, bool)
	if city_man_check == False:
		raise Exception("CityMandatory accepts True or False")

	postc_man_check = isinstance(PostCodeMandatory, bool)
	if postc_man_check == False:
		raise Exception("PostCodeMandatory accepts True or False")

	state_man_check = isinstance(StateMandatory, bool)
	if state_man_check == False:
		raise Exception("StateMandatory accepts True or False")

	country_man_check = isinstance(CountryMandatory, bool)
	if country_man_check == False:
		raise Exception("CountryMandatory accepts True or False")

	if ResultDeliveryMethod == "POST" or "SERVER" or "SERVER_PULL":
		pass
	else:
		raise Exception(
			"ResultDeliveryMethod accepts 'POST', 'SERVER' or 'SERVER_PULL'")

	# ServerResultURL requires no validation

	pay_form_check = isinstance(PaymentFormDisplaysResult, bool)
	if pay_form_check == False:
		raise Exception("PaymentFormDisplaysResult accepts True or False")

	# Pre hash must be in this order
	# Can't split, no PEP8 awards to be won here
	prehash_skeleton = """PreSharedKey={PreSharedKey}&MerchantID={MerchantID}&Password={Password}&Amount={Amount}&CurrencyCode={CurrencyCode}&EchoAVSCheckResult={EchoAVSCheckResult}&EchoCV2CheckResult={EchoCV2CheckResult}&EchoThreeDSecureAuthenticationCheckResult={EchoThreeDSecureAuthenticationCheckResult}&EchoCardType={EchoCardType}&OrderID={OrderID}&TransactionType={TransactionType}&TransactionDateTime={TransactionDateTime}&CallbackURL={CallbackURL}&OrderDescription={OrderDescription}&CustomerName={CustomerName}&Address1={Address1}&Address2={Address2}&Address3={Address3}&Address4={Address4}&City={City}&State={State}&PostCode={PostCode}&CountryCode={CountryCode}&EmailAddress={EmailAddress}&PhoneNumber={PhoneNumber}&EmailAddressEditable={EmailAddressEditable}&PhoneNumberEditable={PhoneNumberEditable}&CV2Mandatory={CV2Mandatory}&Address1Mandatory={Address1Mandatory}&CityMandatory={CityMandatory}&PostCodeMandatory={PostCodeMandatory}&StateMandatory={StateMandatory}&CountryMandatory={CountryMandatory}&ResultDeliveryMethod={ResultDeliveryMethod}&ServerResultURL={ServerResultURL}&PaymentFormDisplaysResult={PaymentFormDisplaysResult}"""

	# Format the string
	prehash = prehash_skeleton.format(
		PreSharedKey=PreSharedKey,
		MerchantID=MerchantID,
		Password=Password,
		Amount=Amount,
		CurrencyCode=CurrencyCode,
		EchoAVSCheckResult=EchoAVSCheckResult,
		EchoCV2CheckResult=EchoCV2CheckResult,
		EchoThreeDSecureAuthenticationCheckResult=
			EchoThreeDSecureAuthenticationCheckResult,
		EchoCardType=EchoCardType,
		OrderID=OrderID,
		TransactionType=TransactionType,
		TransactionDateTime=TransactionDateTime,
		CallbackURL=CallbackURL,
		OrderDescription=OrderDescription,
		CustomerName=CustomerName,
		Address1=Address1,
		Address2=Address2,
		Address3=Address3,
		Address4=Address4,
		City=City,
		State=State,
		PostCode=PostCode,
		CountryCode=CountryCode,
		EmailAddress=EmailAddress,
		PhoneNumber=PhoneNumber,
		EmailAddressEditable=EmailAddressEditable,
		PhoneNumberEditable=PhoneNumberEditable,
		CV2Mandatory=CV2Mandatory,
		Address1Mandatory=Address1Mandatory,
		CityMandatory=CityMandatory,
		PostCodeMandatory=PostCodeMandatory,
		StateMandatory=StateMandatory,
		CountryMandatory=CountryMandatory,
		ResultDeliveryMethod=ResultDeliveryMethod,
		ServerResultURL=ServerResultURL,
		PaymentFormDisplaysResult=PaymentFormDisplaysResult
		)
	# Format the hash to what payment sense expects
	prehash_remove_none = prehash.replace("None","")
	# Replace None with empty string, then remove any \n instances
	prehash_clean = prehash_remove_none.replace("\n","")
	# lastly generate the sha1 string to pass to the URL
	sha1_string = hashlib.sha1(prehash_clean).hexdigest()

	# In the PaymentSense admin console you can change the default hash method
	# to MD5, HMACMD5 or HMACSHA1, please adjust the hash line accordingly.

	# Return sha1 hash of all values
	return dict(
		sha1_string=sha1_string,
		PreSharedKey=PreSharedKey,
		MerchantID=MerchantID,
		Password=Password,
		Amount=Amount,
		CurrencyCode=CurrencyCode,
		EchoAVSCheckResult=EchoAVSCheckResult,
		EchoCV2CheckResult=EchoCV2CheckResult,
		EchoThreeDSecureAuthenticationCheckResult=
			EchoThreeDSecureAuthenticationCheckResult,
		EchoCardType=EchoCardType,
		OrderID=OrderID,
		TransactionType=TransactionType,
		TransactionDateTime=TransactionDateTime,
		CallbackURL=CallbackURL,
		OrderDescription=OrderDescription,
		CustomerName=CustomerName,
		Address1=Address1,
		Address2=Address2,
		Address3=Address3,
		Address4=Address4,
		City=City,
		State=State,
		PostCode=PostCode,
		CountryCode=CountryCode,
		EmailAddress=EmailAddress,
		PhoneNumber=PhoneNumber,
		EmailAddressEditable=EmailAddressEditable,
		PhoneNumberEditable=PhoneNumberEditable,
		CV2Mandatory=CV2Mandatory,
		Address1Mandatory=Address1Mandatory,
		CityMandatory=CityMandatory,
		PostCodeMandatory=PostCodeMandatory,
		StateMandatory=StateMandatory,
		CountryMandatory=CountryMandatory,
		ResultDeliveryMethod=ResultDeliveryMethod,
		ServerResultURL=ServerResultURL,
		PaymentFormDisplaysResult=PaymentFormDisplaysResult
		)

def get_paymenturl(PreSharedKey, MerchantID, Password, Amount, CurrencyCode,
				EchoAVSCheckResult, EchoCardType, OrderID, TransactionType,
				CallbackURL, EmailAddressEditable, PhoneNumberEditable,
				CV2Mandatory, Address1Mandatory, CityMandatory, 
				PostCodeMandatory, StateMandatory, 	CountryMandatory,
				ResultDeliveryMethod, PaymentFormDisplaysResult,
				EchoCV2CheckResult, EchoThreeDSecureAuthenticationCheckResult,
				ServerResultURL, OrderDescription, CustomerName, Address1,
				Address2, Address3, Address4, City, State, PostCode, 
				CountryCode, EmailAddress, PhoneNumber, datetime_tz,
				post_addr):

	# Datetime check, we set this manually, it is not passed to the function
	# TransactionDateTime needs to be in the format of 
	# “YYYY-MM-DD HH:MM:SS +00:00”, with the time in 24hr format, 
	# where 00:00 is the offset from UTC - e.g. “2013-07-22 13:46 +01:00”

	# Define the output format
	fmt = '%Y-%m-%d %H:%M:%S %z'

	# Add your own timezone here
	TransactionDateTime_unclean = datetime_tz.strftime(fmt)

	# Now the python datetime method doesnt include a colon in the UTC offset
	# which means we need this lovely messy code below
	last_c1 = TransactionDateTime_unclean[-1]
	last_c2 = TransactionDateTime_unclean[-2]
	end_str = ":" + last_c2 + last_c1
	TransactionDateTime_remove = TransactionDateTime_unclean[:-2]
	TransactionDateTime = TransactionDateTime_remove + end_str

	# Now build call the hash build function, this variable will become a 
	# dict with all cleaned variables
	sha1_hash = build_hash(
		PreSharedKey = PreSharedKey,
		MerchantID = MerchantID,
		Password = Password,
		Amount = Amount,
		CurrencyCode = CurrencyCode,
		EchoAVSCheckResult = EchoAVSCheckResult, 
		EchoCV2CheckResult = EchoCV2CheckResult,
		EchoThreeDSecureAuthenticationCheckResult =\
			EchoThreeDSecureAuthenticationCheckResult,
		EchoCardType = EchoCardType, 
		OrderID = OrderID,
		TransactionType = TransactionType,
		TransactionDateTime=TransactionDateTime,
		CallbackURL = CallbackURL,
		EmailAddressEditable = EmailAddressEditable, 
		PhoneNumberEditable = PhoneNumberEditable,
		CV2Mandatory = CV2Mandatory,
		Address1Mandatory = Address1Mandatory,
		CityMandatory = CityMandatory,
		PostCodeMandatory = PostCodeMandatory,
		StateMandatory = StateMandatory,
		CountryMandatory = CountryMandatory,
		ResultDeliveryMethod=ResultDeliveryMethod,
		PaymentFormDisplaysResult = PaymentFormDisplaysResult,
		ServerResultURL=ServerResultURL,
		OrderDescription=OrderDescription,
		CustomerName=CustomerName,
		Address1=Address1,
		Address2=Address2,
		Address3=Address3,
		Address4=Address4,
		City=City,
		State=State,
		PostCode=PostCode,
		CountryCode=CountryCode,
		EmailAddress=EmailAddress,
		PhoneNumber=PhoneNumber)

	# Now we have the hash, build the request data pairs with the clean
	# variables we have received from the build_hash() function
	data = {
	'HashDigest': sha1_hash['sha1_string'],
	'MerchantID': sha1_hash['MerchantID'],
	'Amount': sha1_hash['Amount'],
	'CurrencyCode': sha1_hash['CurrencyCode'],
	'EchoAVSCheckResult': sha1_hash['EchoAVSCheckResult'],
	'EchoCV2CheckResult': sha1_hash['EchoCV2CheckResult'],
	'EchoThreeDSecureAuthenticationCheckResult': 
		sha1_hash['EchoThreeDSecureAuthenticationCheckResult'],
	'EchoCardType': sha1_hash['EchoCardType'],
	'OrderID': sha1_hash['OrderID'],
	'TransactionType': sha1_hash['TransactionType'],
	'TransactionDateTime': sha1_hash['TransactionDateTime'],
	'CallbackURL': sha1_hash['CallbackURL'],
	'OrderDescription': sha1_hash['OrderDescription'],
	'CustomerName': sha1_hash['CustomerName'],
	'Address1': sha1_hash['Address1'],
	'Address2': sha1_hash['Address2'],
	'Address3': sha1_hash['Address3'],
	'Address4': sha1_hash['Address4'],
	'City': sha1_hash['City'],
	'State': sha1_hash['State'],
	'PostCode': sha1_hash['PostCode'],
	'CountryCode': sha1_hash['CountryCode'],
	'EmailAddress': sha1_hash['EmailAddress'],
	'PhoneNumber': sha1_hash['PhoneNumber'],
	'EmailAddressEditable': sha1_hash['EmailAddressEditable'],
	'PhoneNumberEditable': sha1_hash['PhoneNumberEditable'],
	'CV2Mandatory': sha1_hash['CV2Mandatory'],
	'Address1Mandatory': sha1_hash['Address1Mandatory'],
	'CityMandatory': sha1_hash['CityMandatory'],
	'PostCodeMandatory': sha1_hash['PostCodeMandatory'],
	'StateMandatory': sha1_hash['StateMandatory'],
	'CountryMandatory': sha1_hash['CountryMandatory'],
	'ResultDeliveryMethod': sha1_hash['ResultDeliveryMethod'],
	'ServerResultURL': sha1_hash['ServerResultURL'],
	'PaymentFormDisplaysResult':sha1_hash['PaymentFormDisplaysResult'],
	}

	r = requests.post(post_addr, params=data)
	url = r.url
	url_clean =  url.replace("None","")
	
	# Return the clean url, your application can then direct the user
	# to this url, once payment is completed the user will be sent to the 
	# 'CallbackURL' given to the function

	return r.url
