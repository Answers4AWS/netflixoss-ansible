#!/usr/bin/python -u
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
import sys
import urllib2
import socket
import urlparse
if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
import requests
import json
if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
import hashlib
if 46 - 46: ooOoO0o * I11i - OoooooooOO
import hmac
import base64
from hashlib import sha256
import datetime
if 30 - 30: o0oOOo0O0Ooo - O0 % o0oOOo0O0Ooo - OoooooooOO * O0 * OoooooooOO
try :
 from urllib . parse import quote
except ImportError :
 from urllib import quote
 if 60 - 60: iIii1I11I1II1 / i1IIi * oO0o - I1ii11iIi11i + o0oOOo0O0Ooo
 if 94 - 94: i1IIi % Oo0Ooo
 if 68 - 68: Ii1I / O0
Iiii111Ii11I1 = "169.254.169.254"
ooO0oooOoO0 = "2009-04-04"
II11i = "http://%s/%s" % ( Iiii111Ii11I1 , ooO0oooOoO0 )
if 43 - 43: Ii1I . oO0o
def IIii11I1 ( uri ) :
 oo0 = "%s/%s" % ( II11i , uri )
 try :
  Oooo00OOo000 = urllib2 . urlopen ( urllib2 . Request ( oo0 ) , timeout = 3 )
  O0I11i1i11i1I = Oooo00OOo000 . read ( )
 except urllib2 . URLError as Iiii :
  if isinstance ( Iiii . reason , socket . timeout ) :
   return None
  if Iiii . reason . errno == 64 :
   return None
  raise
 except urllib2 . HTTPError as Iiii :
  if Iiii . code == 404 :
   return None
   if 87 - 87: oO0o / ooOoO0o + I1Ii111 - ooOoO0o . ooOoO0o / II111iiii
  if Iiii . code == 500 :
   return None
  raise
  if 11 - 11: I1IiiI % o0oOOo0O0Ooo - Oo0Ooo
 return O0I11i1i11i1I
 if 58 - 58: i11iIiiIii % I1Ii111
 if 54 - 54: OOooOOo % O0 + I1IiiI - iII111i / I11i
def iIiiI1 ( metaopt ) :
 if 68 - 68: I1IiiI - i11iIiiIii - OoO0O00 / OOooOOo - OoO0O00 + i1IIi
 if metaopt == 'availability-zone' :
  if 48 - 48: OoooooooOO % o0oOOo0O0Ooo . I1IiiI - Ii1I % i1IIi % OoooooooOO
  return IIii11I1 ( 'meta-data/placement/availability-zone' )
  if 3 - 3: iII111i + O0
 if metaopt == 'public-keys' :
  I1Ii = IIii11I1 ( 'meta-data/public-keys' )
  if I1Ii == None :
   return None
   if 66 - 66: Ii1I
  oo0Ooo0 = [ I1I11I1I1I . split ( '=' ) [ 0 ] for I1I11I1I1I in I1Ii . splitlines ( ) ]
  if 90 - 90: II111iiii + oO0o / o0oOOo0O0Ooo % II111iiii - O0
  iIii1 = [ ]
  for oOOoO0 in oo0Ooo0 :
   O0OoO000O0OO = 'meta-data/public-keys/%d/openssh-key' % int ( oOOoO0 )
   iIii1 . append ( IIii11I1 ( O0OoO000O0OO ) . rstrip ( ) )
   if 23 - 23: i11iIiiIii + I1IiiI
  return iIii1
  if 68 - 68: OoOoOO00 . oO0o . i11iIiiIii
 if metaopt == 'user-data' :
  return IIii11I1 ( 'user-data' )
  if 40 - 40: oO0o . OoOoOO00 . Oo0Ooo . i1IIi
 return IIii11I1 ( 'meta-data/' + metaopt )
 if 33 - 33: Ii1I + II111iiii % i11iIiiIii . ooOoO0o - I1IiiI
 if 66 - 66: Ii1I - OoooooooOO * OoooooooOO . OOooOOo . I1ii11iIi11i
class IiI1i11iii1 ( object ) :
 def __init__ ( self , credentials , api_version = '' ) :
  if 96 - 96: O0 % oO0o % iIii1I11I1II1
  if 78 - 78: iIii1I11I1II1 - Ii1I * OoO0O00 + o0oOOo0O0Ooo + iII111i + iII111i
  if 11 - 11: iII111i - OoO0O00 % ooOoO0o % iII111i / OoOoOO00 - OoO0O00
  self . credentials = credentials
  self . api_version = api_version
  self . hmac = hmac . new ( self . credentials . secret_key . encode ( 'utf-8' ) ,
 digestmod = sha256 )
  if 74 - 74: iII111i * O0
 def calc_signature ( self , params ) :
  oOOo0oo = ''
  hmac = self . hmac . copy ( )
  params [ 'signature_method' ] = 'HmacSHA256'
  o0oo0o0O00OO = sorted ( params )
  o0oO = [ ]
  for I1i1iii in o0oo0o0O00OO :
   O0I11i1i11i1I = params [ I1i1iii ]
   o0oO . append ( quote ( I1i1iii , safe = '' ) + '=' +
 quote ( O0I11i1i11i1I , safe = '_-~' ) )
  i1iiI11I = '&' . join ( o0oO )
  oOOo0oo += i1iiI11I
  hmac . update ( oOOo0oo . encode ( 'utf-8' ) )
  iiii = base64 . b64encode ( hmac . digest ( ) ) . strip ( ) . decode ( 'utf-8' )
  return ( i1iiI11I , iiii )
  if 54 - 54: I1ii11iIi11i * OOooOOo
 def add_auth ( self , params ) :
  params [ 'access_key' ] = self . credentials . access_key
  params [ 'timestamp' ] = datetime . datetime . utcnow ( ) . isoformat ( ) + "+00:00"
  params [ 'api_version' ] = self . api_version
  i1iiI11I , I1IIIii = self . calc_signature ( params )
  return I1IIIii
  if 95 - 95: OoO0O00 % oO0o . O0
  if 15 - 15: ooOoO0o / Ii1I . Ii1I - i1IIi
def o00oOO0 ( ) :
 return '9j43VOYq0rnMrg6oP6YzeA6FZB56elApJe7QPizO' [ : : - 1 ] . decode ( 'rot13' )
 if 95 - 95: OOooOOo / OoooooooOO
class iI ( object ) :
 def __init__ ( self , access_key = None , secret_key = None ) :
  self . access_key = access_key
  self . secret_key = secret_key
  if 60 - 60: I11i / I11i
  if 46 - 46: Ii1I * OOooOOo - OoO0O00 * oO0o - I1Ii111
class oo0o00 ( object ) :
 if 95 - 95: O0 + OoO0O00 . II111iiii / O0
 API_VERSION = 'v1'
 if 97 - 97: ooOoO0o - OOooOOo * i11iIiiIii / OoOoOO00 % I1Ii111 - OoooooooOO
 if 59 - 59: O0 + I1IiiI + IiII % I1IiiI
 def __init__ ( self , endpoint = 'https://api.awsanswers.com' ,
 credentials = None ) :
  if isinstance ( credentials , iI ) :
   self . credentials = credentials
  else :
   self . credentials = get_credentials ( )
  self . auth = IiI1i11iii1 ( self . credentials , api_version = self . API_VERSION )
  self . endpoint = endpoint
  self . was_successful = True
  if 70 - 70: iII111i * I1ii11iIi11i
  if 46 - 46: ooOoO0o / OoO0O00
 def _get_response ( self , path , method , params ) :
  if 52 - 52: o0oOOo0O0Ooo - OoooooooOO + Ii1I + Ii1I - o0oOOo0O0Ooo / I1Ii111
  self . was_successful = True
  if 44 - 44: ooOoO0o . i1IIi - I1ii11iIi11i . O0 - ooOoO0o
  if 92 - 92: iII111i . I11i + o0oOOo0O0Ooo
  if 28 - 28: i1IIi * Oo0Ooo - o0oOOo0O0Ooo * IiII * Ii1I / OoO0O00
  params [ 'path' ] = path
  I1IIIii = self . auth . add_auth ( params )
  OooO0OoOOOO = { }
  OooO0OoOOOO [ 'signature' ] = I1IIIii
  if 46 - 46: OOooOOo / I1ii11iIi11i
  if 24 - 24: I11i . iII111i % OOooOOo + ooOoO0o % OoOoOO00
  if method == 'POST' :
   I11III1II = None
   iI1I111Ii111i = params
  else :
   I11III1II = params
   iI1I111Ii111i = None
   if 7 - 7: ooOoO0o * OoO0O00 % oO0o . IiII
   if 45 - 45: i11iIiiIii * II111iiii % iIii1I11I1II1 + I1ii11iIi11i - Ii1I
  oo0 = self . endpoint + path
  iIi1iIiii111 = requests . request ( method , oo0 , params = I11III1II , data = iI1I111Ii111i ,
 headers = OooO0OoOOOO , timeout = 20 )
  if 16 - 16: I1ii11iIi11i + OoO0O00 - II111iiii
  if 85 - 85: OoOoOO00 + i1IIi
  iIi1iIiii111 . encoding = 'utf-8'
  I1Ii = iIi1iIiii111 . text . encode ( 'utf-8' )
  if iIi1iIiii111 . status_code >= 200 and iIi1iIiii111 . status_code < 300 :
   if I1Ii :
    return json . loads ( I1Ii )
   else :
    return True
  else :
   self . was_successful = False
   if I1Ii :
    try :
     return json . loads ( I1Ii )
    except ValueError as Iiii :
     print 'ERROR: Response was not valid JSON'
     print I1Ii
     return False
     if 58 - 58: II111iiii * OOooOOo * I1ii11iIi11i / OOooOOo
   oO0o0OOOO = { 'status_code' : iIi1iIiii111 . status_code }
   oO0o0OOOO [ 'errors' ] = I1Ii
   return oO0o0OOOO
   if 68 - 68: iII111i - I1Ii111 - I1IiiI - I1ii11iIi11i + I11i
   if 10 - 10: OoooooooOO % iIii1I11I1II1
 def was_last_request_successful ( self ) :
  if 54 - 54: I1Ii111 - II111iiii % OoOoOO00 % I11i % iIii1I11I1II1 + ooOoO0o
  return self . was_successful
  if 15 - 15: I11i * ooOoO0o * Oo0Ooo % i11iIiiIii % OoOoOO00 - OOooOOo
  if 68 - 68: I1Ii111 % i1IIi . IiII . I1ii11iIi11i
  if 92 - 92: iII111i . I1Ii111
  if 31 - 31: I1Ii111 . OoOoOO00 / O0
 def add_ami_boot_log ( self , ami , az , instance_id_hash ) :
  if 89 - 89: OoOoOO00
  return self . _get_response ( '/ami-boot.json' , 'POST' , {
 'ami-boot[ami]' : ami ,
 'ami-boot[az]' : az ,
 'ami-boot[iihash]' : instance_id_hash
 } )
  if 68 - 68: OoO0O00 * OoooooooOO % O0 + OoO0O00 + ooOoO0o
  if 4 - 4: ooOoO0o + O0 * OOooOOo
OOoo0O = iIiiI1 ( 'ami-id' ) or 'ami-00001001'
Oo0ooOo0o = iIiiI1 ( 'availability-zone' ) or 'us-fake-1a'
Ii1i1 = iIiiI1 ( 'instance-id' )
iiIii = hashlib . md5 ( Ii1i1 ) . hexdigest ( )
if 79 - 79: OoooooooOO / O0
OO0OoO0o00 = iI ( access_key = 'AKwZyqr5IJu9zqPKRtoll8B8KlFzzOCJ' , secret_key = o00oOO0 ( ) )
ooOO0O0ooOooO = "http://api.awsanswers.com"
if 55 - 55: o0oOOo0O0Ooo * OoOoOO00
o0O00oOoOO = oo0o00 ( endpoint = ooOO0O0ooOooO , credentials = OO0OoO0o00 )
if 42 - 42: OoO0O00
print o0O00oOoOO . add_ami_boot_log ( OOoo0O , Oo0ooOo0o , iiIii )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
