from flask import Flask, request
from flask import Response
import flask
import json
import boto
import boto.sqs
from boto.sqs.message import RawMessage

from boto.dynamodb2.table import Table,Item
import boto.dynamodb2.exceptions
import uuid
import datetime
from datetime import timedelta
from decimal import *
application = flask.Flask(__name__)
#Set application.debug=true to enable tracebacks on Beanstalk log output.
#Make sure to remove this line before deploying to production.
application.debug=False
@application.route('/', methods=['Get'])
def introhtml():
    #TODO : Implament Welcome Page
    return "IEP V.1 API"

@application.route('/v1/session', methods=['Post'])
def session():
    #TODO : Implament Get Welcome Page
    #TODO : Switch Method based on input method
    #TODO : Method Reponse Optimization

    currenttimestamp = datetime.datetime.now()
    #currenttimestamp = currenttimestamp - timedelta(hours=4)
    #Input Validation and Error Checking
    try:
        if request.json['deviceid'] == '':
            errormessage = {}
            errormessage['errorcode'] = '101'
            errormessage['errormessage'] = 'Device ID not supplied'
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp
    except Exception:
        errormessage = {}
        errormessage['errorcode'] = '201'
        errormessage['errormessage'] = 'Device ID Error'
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    try:
        if request.json['appid'] == '':
            errormessage = {}
            errormessage['errorcode'] = '102'
            errormessage['errormessage'] = 'App Id not supplied'
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp
    except Exception:
        errormessage = {}
        errormessage['errorcode'] = '202'
        errormessage['errormessage'] = 'App ID Error'
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    try:
        if request.json['lat'] == '':
            errormessage = {}
            errormessage['errorcode'] = '103'
            errormessage['errormessage'] = 'Lat not supplied'
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp
        decvalue =  Decimal(request.json['lat'])
    except Exception:
        errormessage = {}
        errormessage['errorcode'] = '203'
        errormessage['errormessage'] = 'Lat Error'
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    try:
        if request.json['long'] == '':
            errormessage = {}
            errormessage['errorcode'] = '104'
            errormessage['errormessage'] = 'Long not supplied'
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp
        decvalue = Decimal(request.json['long'])
    except Exception:
        errormessage = {}
        errormessage['errorcode'] = '204'
        errormessage['errormessage'] = 'Long Error'
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    #Table Connections to Dynamo
    active_sessions = Table('active_sessions')
    app_parameters = Table('app_parameters')
    #With The Inputs good, try and build the reponse
    sessionresponse = {}
    parameter_dict = {}
    uuid_catalog={}
    #TODO : Implament UUID Look Up Method

    uuid_catalog['uuid4'] = '8492E75F-4FD6-469D-B132-043FE94921D8'
    uuid_catalog['uuid5'] = 'B9407F30-F5F8-466E-AFF9-25556B57FE6D'
    uuid_catalog['uuid3']='C1D0E2DC-A305-436B-A49E-3E62C6D48777'
    uuid_catalog['uuid2']= '8492E75F-4FD6-469D-B132-043FE94921D8'
    uuid_catalog['uuid1']='5ECD88CB-08FB-4557-9788-4BBDFFD9B180'

    #Build the session reponse

    #Build the Parameters Dict
    try:
        parameters = app_parameters.query_2(app_id__eq=request.json['appid'],index='app_id-index')
        for parameter in parameters:
            parameter_dict[parameter['key']] = parameter['value']
        if not parameter_dict.has_key('service_url'):
            errormessage = {}
            errormessage['errorcode'] = '603'
            errormessage['errormessage'] = 'Unauthorized App ID3'
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp
    except Exception :
        errormessage = {}
        errormessage['errorcode'] = '301'
        print "Database Error on Parameter Lookup"
        errormessage['errormessage'] = 'Database error on app parameter lookup'
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    try:
        session = active_sessions.get_item(device_id = request.json['deviceid'])
        sessionID = session['session_id']
        session['timestamp'] = str(currenttimestamp)
        session.partial_save()
    except Exception :
        sessionID = uuid.uuid4()
        try:
            if request.json['appid'] <> 'Test':
                active_sessions.put_item(data={
                'session_id' : str(sessionID),
                'timestamp' : str(datetime.datetime.now()),
                'device_id' : request.json['deviceid'],
                'app_id' : request.json['appid'],
                'latitude' : request.json['lat'],
                'longitude' : request.json['long']})
        except Exception as e:
            errormessage = {}
            errormessage['errorcode'] = '301'
            print "Database Error on Session Write"
            errormessage['errormessage'] = 'Database Error on session put : ' "appid = " + request.json['appid'] + "deviceid=" + request.json['deviceid']
            resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
            return resp

    sessionresponse['sessionid'] = str(sessionID)
    sessionresponse['ping'] = str(10)
    sessionresponse['timestamp'] = str(currenttimestamp)
    sessionresponse['configuration'] = parameter_dict
    sessionresponse['uuid'] = uuid_catalog


    #Format the response
    resp = Response(response=json.dumps(sessionresponse),
                    status=200,
                    mimetype="application/json")


    #Actually send the Reponse
    return resp

@application.route('/gimbalsighting', methods=['Post'])
def hello_world():
    #TODO : Spell Gimbal Method out further
    table = Table('gimbal')
    jsondata = request.json


    try:
        sighting = Item(table,data=jsondata)
        sighting.save()
    except Exception:
        return 'Error'
    return 'Hello World!'

@application.route('/v1/te2/bievent',methods=['Post'])
def te2bievent():
    resp = Response(response=json.dumps('not implamented'),status=200,mimetype='application/json')

    return resp

@application.route('/v1/sighting',methods=['Post'])
def sighting2():

    try:
        r_sessionid = request.json['SessionID']
        r_uuid = request.json['UUID']
        r_major = request.json['Major']
        r_minor = request.json['Minor']
        r_rssi = request.json['RSSI']
        r_lat = request.json['lat']
        r_long = request.json['long']
    except Exception as e:
        print e
        errormessage = {}
        errormessage['errorcode'] = '501'
        errormessage['errormessage'] = e.message
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp

    #log it
    ibeaconsighiting = Table('ibeacon_sighting')
    currenttime = datetime.datetime.now()
    #currenttime = currenttime - timedelta(hours=4)




    try:
       # ibeaconsighiting.put_item(data={
       #     'uuid_set' : str(r_uuid) + str(r_major) + str(r_minor),
       #     'session_id' : str(r_sessionid),
       #     'timestamp' : str(currenttime),
       #     'uuid' : str(r_uuid),
       #     'major' : str(r_major),
       #     'minor' : str(r_minor),
       #     'RSSI' : str(r_rssi),
       #     'latitude' : str(r_lat),
       #     'longitude' : str(r_long),
       #     'eventtype' : 'Sighting'})

        sqslink = boto.sqs.connect_to_region('us-east-1')
        sightingq = sqslink.get_queue('sighting')
        smsg = RawMessage()
        smsg.set_body(request.json)
        sightingq.write(smsg)



    except Exception as e:
        errormessage = {}
        errormessage['errorcode'] = '301'
        errormessage['errormessage'] = e.message
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    #look up offer
    try:
        activeoffers = Table('active_offers')
        q_uuidmm = r_uuid+r_major+r_minor
        offers = activeoffers.query_2(uuidmm__eq=q_uuidmm,index='uuidmm-index', limit=20)
        offerarray = []
        for offer in offers:
            thisoffer={}
            thisoffer['ActionType'] = offer['actiontype']
            thisoffer['ActionToken'] = offer['offer_id']
            thisoffer['PassURL'] = offer['passurl']
            thisoffer['Title'] = offer['title']
            thisoffer['OfferType'] = offer['offer_type']
            thisoffer['Description'] = offer['description']
            thisoffer['VendorName'] = offer['vendor_name']
            thisoffer['ExpireDateTime'] = offer['expiretime']
            thisoffer['ShowLocalNotification'] = True
            thisoffer['ExpireNumberOfMinutes'] = 20
            thisoffer['StreetAddress'] = offer['streetaddress']
            offerarray.append(thisoffer)
    except Exception as e:
        print e
        errormessage = {}
        errormessage['errorcode'] = '301'
        errormessage['errormessage'] = e.message
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp

    fullresponse={}
    fullresponse['sessionID'] = r_sessionid
    fullresponse['timestamp'] = str(currenttime)
    fullresponse['SightingResponse'] = offerarray
    print fullresponse
    resp = Response(response=json.dumps(fullresponse),
                    status=200,
                    mimetype="application/json")


    return resp

    #build response

@application.route('/v1/addoffer', methods=['Post'])
def addoffer():

    offers = Table('active_offers')
    print str(request.json)
    donkey = uuid.uuid4()
    try:
        actiontype = 'Pass'
        _uuid = request.json['uuid']
        major = request.json['major']
        minor = request.json['minor']
        uuidmm = _uuid + major + minor
        offerid = str(uuid.uuid4())
        passurl = request.json['passurl']
        title = request.json['title']
        offertype = request.json['offertype']
        description = request.json['description']
        vendorname = request.json['vendorname']
        expiretime = request.json['expiredatetime']
        streetaddress = request.json['streetaddress']
    except Exception as e:
        print e
        errormessage = {}
        errormessage['errorcode'] = '501'
        errormessage['errormessage'] = e.message
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    try:
        offers.put_item(data={
            'uuidmm' : uuidmm,
            'offer_type' : offertype,
            'vendor_name' : vendorname,
            'offer_id' : offerid,
            'actiontype' : actiontype,
            'passurl' : passurl,
            'title' : title,
            'description' : description,
            'expiretime' : expiretime,
            'streetaddress' : streetaddress
        })
    except Exception as e:
        print e
        errormessage = {}
        errormessage['errorcode'] = '501'
        errormessage['errormessage'] = e.message
        resp = Response(response=json.dumps(errormessage),
                    status=400,
                    mimetype="application/json")
        return resp
    resp = Response(response='',
                    status=204,
                    mimetype="application/json")
    return resp

@application.route('/v1/te2/appuserid/<string:deviceid>', methods=['Get'])
def binddevicetouserid(deviceid):
    resp = Response(response=json.dumps('success'),
                    status=200,
                    mimetype="application/json")
    return resp


@application.route('/v1/passreject/<string:token>',methods=['Get'])
def passrejection(token):
    print token
    resp = Response(response=json.dumps('not implamented'),status=200,mimetype='application/json')

    return resp


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)




