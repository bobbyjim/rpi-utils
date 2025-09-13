#!/usr/bin/env python3
import sys
import time
import string
import json
import yaml          # sudo pip3 install simple-yaml
from cmd2 import Cmd # sudo pip3 install cmd2
import requests      # see http://docs.python-requests.org/en/master/
###############################################################################
#
#  KnowThings Robot
#
###############################################################################


###############################################################################
#
#  Load the Session
#
###############################################################################
try:
   with open('ktr.yaml', 'r') as yaml_file:
      session = yaml.load(yaml_file)
      print("Loaded: session ktr.yaml")
except EnvironmentError:
   session = { 'created': int(time.time()) }
   print("Created session")

###############################################################################
#
#  Main Class (extends Cmd)
#
###############################################################################   
class KTRobot(Cmd):
   prompt = 'ktrsh% '

   def dumpit(self,msg,stream):
      yaml.safe_dump(msg, stream, default_flow_style = False)

   def preloop(self):
      self.do_session(None)

   def precmd(self, line):                      # Freshen the default URLs
      host  = session.get('host.facade', 'localhost')
      host2 = session.get('host.model',  'localhost')
      port  = session.get('port.facade', '8000')
      port2 = session.get('port.model',  '8002')
      loc   = 'http://' + host  + ":" + str(port)
      loc2  = 'http://' + host2 + ":" + str(port2)
      
      session['header.origin'] = loc
      session['facade.capture.url'] = loc + '/networkcaptures'
      session['facade.avd.url'] = loc + '/avds'
      session['facade.instance.url'] = loc + '/avdinstances'
      session['model.avd.url'] = loc2
      return line

   def postcmd(self, stop, line):               # Save the Session
      with open('ktr.yaml', 'w') as outfile:
         self.dumpit(session, outfile)
         outfile.close()
      return stop

   ############################################################################
   #
   #  Create:
   #  - an AVD
   #  - an instance of an AVD 
   #  - a bunch of instances of an AVD
   #
   #############################################################################
   def do_create(self, arg):
      'Create instance | instances | avd'
      if arg == 'instances':
         self.do_create_instances(arg)
      elif arg == 'instance':
         self.do_create_instance( arg )
      elif arg == 'avd':
         self.do_create_avd( arg )
      else:
         print("Unknown argument '%s'" % arg)

   def do_create_avd(self, arg):
      'Create a bare AVD using ModelService.  REQUIRES: model.avd.url. SETS: avd.id.'
      print("Create AVD")
      url = session.get('model.avd.url')
      
      if self.check_ok( ['model.avd.url'] ) == True:
         avdname = session.get('avd.name', 'testavd') + "-" + str(int(time.time()))
         headers = { 'Content-type': 'application/json', 'accept': '*/*' }
         payload = '{ "avd_name": "%s" }' % avdname

         try:
            r = requests.post(url + "/avds", data=payload, headers=headers, timeout=5.0)
            data = self.handleResponse(r)
            avd_id = data.get( 'avd_id', 'ERROR' )
            session[ 'avd.id' ] = avd_id
         except requests.exceptions.ConnectionError as e:
            print("Error retrieving AVD ID.")

   def do_create_instance(self, arg):
      'Create an instance from the current AVD. REQUIRES: avd.id, target.ip, target.port, facade.avd.url. SETS: instance.id.'
      print("Create Instance")
      
      avd_id = session.get( 'avd.id', 'NONE' )
      target_ip = session.get( 'target.ip', '127.0.0.1' )
      target_port = int(session.get( 'target.port', '8080' ))
      url = session.get( 'facade.avd.url', 'localhost:8000' )
      ds_repl_id = session.get('datastream.id.replacement', '')
      payload = '{ "ip": "%s", "port": %d, "data_stream_id": "%s" }' % (target_ip, target_port, ds_repl_id)

      headers = { "accept": 'application/json', "Content-Type": 'application/json' }
      
      if self.check_ok( ( 'avd.id', 'target.ip', 'target.port', 'facade.avd.url' ) ) == True:
         url += "/" + avd_id + "/avdinstances"
         r = requests.post( url, data=payload, headers=headers )
         data = self.handleResponse(r)         
         session[ 'instance.id' ] = str(data.get( 'ins_id', 'ERROR' ))
   
   def do_create_instances(self, arg):
      'Create multiple instances, driven by the datastream.id.csv list. REQUIRES: datastream.id.csv. SETS: instance.id.csv'
      print("Create multiple instances")
     
      replacement_ids = session.get( 'datastream.id.csv', 'NONE' ).split( ',' )
      instanceList = []
      for rid in replacement_ids:
         session[ 'datastream.id.replacement' ] = rid
         self.do_create_instance(arg)
         instanceList.append(session.get('instance.id', 'ERROR'))
      session[ 'instance.id.csv' ] = ','.join(instanceList)
               
   ############################################################################
   #
   #  Upload:
   #  - an AVD file (and create the AVD)
   #  - a PCAP file (and create the capture)
   #
   #############################################################################
   def do_upload(self, arg):
      'Upload avd | pcap file.'
      if arg == 'pcap':
         self.do_upload_pcap(arg)
      else:
         self.do_upload_avd(arg)

   def do_upload_avd(self, arg):
      'Create an AVD by upload. REQUIRES: avd.file, facade.avd.url, header.origin. SETS: avd.id.'      
      print("Upload AVD")      
      filename = session.get('avd.file')
      url      = session.get('facade.avd.url') + "/upload"
      origin   = session.get('header.origin')
      
      if self.check_ok( ('avd.file', 'facade.avd.url', 'header.origin') ) == True:
         avdname = session.get('avd.name', 'testavd') + "-" + str(int(time.time()))
         
         headers = { 'Origin': origin, 'accept': 'application/json' }
         avdfile = { 'file': open(filename, 'rb') } # , 'application/x-zip-compressed' ) }
         payload = { 'avd_name': avdname }
         
         try:
            r = requests.post(url, files=avdfile, data=payload, headers=headers, timeout=5.0)
            data = self.handleResponse(r)
            session[ 'avd.id' ] = str(data.get( 'avd_id', 'ERROR' ))
         except requests.exceptions.ConnectionError as e:
            print("Error retrieving AVD ID.")
	 
   def do_upload_pcap(self,arg):
      'Create a capture by upload. REQUIRES: pcap.file, facade.capture.url, header.origin. SETS: capture.id.'

      print("Upload PCAP")
      filename = session.get('pcap.file')
      url      = session.get('facade.capture.url') + "/upload"
      origin   = session.get('header.origin')
      
      if self.check_ok( ('pcap.file', 'facade.capture.url', 'header.origin') ) == True:
         pcapfile = { 'file': open(filename, 'rb') }
         headers = { 'Origin': origin } # , 'accept': 'application/json' }
         try: 
            r = requests.post(url, files=pcapfile, headers=headers, timeout=5.0 )
            data = self.handleResponse(r)
            session['capture.id'] = str(data.get( 'capture_id', 'ERROR' ))
         except requests.exceptions.ConnectionError as e:
            print("Error retrieving PCAP ID.")

   ############################################################################
   #
   #  Update AVD
   #  - update metadata (e.g. name and datastream id)
   #  - optionally update the AVD ZIPfile as well
   #
   #############################################################################
   def do_update(self,arg):
      'Update an AVD.  REQUIRES: avd.id, facade.avd.url. OPTIONAL: avd.file.replace, datastream.id. SETS: avd.name'
      print("Update AVD")
      avd_id   = session.get('avd.id')
      filename = session.get('avd.file.replace', None)
      base_url = session.get('facade.avd.url') + "/" + avd_id

      headers = { 'accept': 'application/json', 'Content-Type': 'application/json' }
      avdname = session.get('avd.name', 'testavd') + "-" + str(int(time.time()))
      ds_id  = session.get( 'datastream.id', '' )
      params = '{ "avd_name": "%s", "data_stream_id": "%s" }' % (avdname, ds_id)
      #params = { "avd_name": avdname, "data_stream_id": ds_id }

      if self.check_ok( ('avd.id', 'facade.avd.url') ) == True:         
         try:
            if filename is not None:
               print("Updating zipfile and metadata. This may take some time.")
               zip_url = base_url + "/avdzipfile"
               avdfile = { 'file': open(filename, 'rb') } # , 'application/x-zip-compressed' ) }
               r = requests.put(zip_url, files=avdfile, data=params, headers=headers)
            else:
               print("Updating metadata only. This may take some time.")
               r = requests.put(base_url, data=params, headers=headers)
            data = self.handleResponse(r)
            session[ 'avd.name' ] = data.get( 'avd_name', 'ERROR' )
            
         except requests.exceptions.ConnectionError as e:
            print("Error updating AVD.")

   ############################################################################
   #
   #  Show:
   #  - avd metadata
   #  - avd model data
   #  - list of avds
   #  - list of avd IDs
   #  - list of instances
   #
   #############################################################################            
   def do_show(self,arg):
      'Show avd | avds | instances | model | avdids'
      if arg == 'instances':
         self.do_show_instances(arg)
      elif arg == 'model': 
         self.do_show_model(arg)
      elif arg == 'avdids':
         self.do_show_avdids(arg)
      elif arg == 'avd':
         self.do_show_avd(arg)
      else: # avds
         self.do_show_avds(arg)
   
   def do_show_avd(self,arg):
      'Show metadata for this AVD.'
      avd_id = session.get('avd.id')
      url = session.get('model.avd.url') + "/avds/" + avd_id
      r = requests.get( url )
      self.handleResponse(r)
      
   def do_show_avds(self, arg):
      'List AVDs in the system.'
      request = session.get('facade.avd.url', 'http://localhost:8000/avds')
      r = requests.get( request )
      self.handleResponse( r )

   def do_show_avdids(self, arg):
      'List AVDs in the system.'
      request = session.get('facade.avd.url', 'http://localhost:8000/avds')
      r = requests.get( request )
      msg = json.loads( r.text )
      print("[")
      for avd in msg:
         print(" %16s : %s" % (avd.get("avd_id", "ID not found in model"), avd.get('avd_name')))
      print("]")

   def do_show_model(self, arg):
      'Show AVD model data. REQUIRES: avd.id.'
      avdid = session.get( 'avd.id' )
      url = session.get('facade.avd.url', 'http://localhost:8000/avds') + "/" + avdid + "/data"
      headers = { "accept": "application/json" }
      r = requests.get( url, headers=headers )
      self.handleResponse( r )
      
   def do_show_instances(self, arg):
      'Show instances. REQUIRES: avd.id.'
      url = session.get('facade.instance.url', 'http://localhost:8000/instances')
      avdid = session.get( 'avd.id' )
      queryparams = { 'avd_id': avdid }
      r = requests.get( url, params=queryparams )
      self.handleResponse( r )

   ############################################################################
   #
   #  Starting and Stopping instances
   #  - start current instance
   #  - start up a list of instances (possibly created by 'create instances')
   #  - stop current instance
   #  - stop a list of instances (possibly created by 'create instances')
   #
   #############################################################################      
   def do_startlist(self,arg):
      'Start instances in instance.id.csv. REQUIRES: instance.id.csv. USES: instance.id.'
      print("Start instances")
      for ins_id in session.get( 'instance.id.csv', 'NONE' ).split(","):
         session[ 'instance.id' ] = ins_id
         self.do_start(arg)
      
   def do_start(self, arg):
      'Start the current instance. REQUIRES: instance.id, facade.instance.url.'
      print("Start instance")
      
      ins_id = session.get( 'instance.id', 'NONE' )
      if self.check_ok( ['instance.id'] ) == True:
         print("Starting %s", ins_id)
         url = session.get( 'facade.instance.url', 'localhost:8000' ) + "/" + ins_id + "/start"
         headers = { "accept": 'application/json' }
         r = requests.post( url, headers=headers, timeout=5.0)
         data = self.handleResponse(r)         
	  
   def do_stoplist(self,arg):
      'Stop instances in instance.id.csv. REQUIRES: instance.id.csv. USES: instance.id.'
      print("Stop instances")
      for ins_id in session.get( 'instance.id.csv', 'NONE' ).split(","):
         session[ 'instance.id' ] = ins_id
         self.do_stop(arg)
      
   def do_stop(self, arg):
      'Stop the current instance. REQUIRES: instance.id, facade.instance.url.'
      print("Stop instance")
      
      ins_id = session.get( 'instance.id', 'NONE' )
      if self.check_ok( ['instance.id'] ) == True:
         print("Stopping %s", ins_id)
         url = session.get( 'facade.instance.url', 'localhost:8000' ) + "/" + ins_id + "/stop"
         headers = { "accept": 'application/json' }
         r = requests.post( url, headers=headers, timeout=5.0)
         data = self.handleResponse(r)         

   ############################################################################
   #
   #  Assertions
   #
   ############################################################################
   def do_has(self, arg):
      'Search the first session value for the second.'
      args = arg.split()
      if len(args) != 2:
         print("ERROR: assertion 'has' requires two parameters")
      else:
         key1 = args[0]
         key2 = args[1]
         source = session.get( key1, "NULL" )
         find   = session.get( key2, "NONE" )
         res    = find in source
         msg    = "%s [%s =~ %s]" % (res, source, find)
         print(msg)
         session[ 'test.status' ] = 'OK' if res else 'FAIL'
    
   def do_hasv(self, arg):
      'Search the session value for the specified #value.'
      args = arg.split()
      if len(args) != 2:
         print("ERROR: assertion 'hasv' requires two parameters")
      else:
         key = args[0]
         source = session.get( key, "NULL" )
         find = args[1]
         res = find in source
         msg    = "%s [%s =~ %s]" % (res, source, find)
         print(msg)
         session[ 'test.status' ] = 'OK' if res else 'FAIL'

   ############################################################################
   #
   #  Utils
   #
   ############################################################################
   def handleResponse( self, response ):
      print("\n------- Response: %s ------" % response.status_code)
      print("Headers:")
      print(response.headers)
      print("\n-------- Message: ---------\n")
      session[ 'command.rsp' ] = response.text
      if response.text:
         msg = json.loads( response.text )
         self.dumpit(msg, sys.stdout)
         print
         return msg

   def do_sv(self, arg):
      'Set a session value.  SYNOPSIS: sv rvalue lvalue'
      args = arg.split()
      a = str(args[0])
      b = ' '.join(args[1:])
      session[a] = b
      print("[" + a + "]: [" + session[a] + "]")

   def do_setv(self, arg):
      self.do_sv(arg)
      
   def do_status(self, arg):
      'Set the status'
      self.do_sv( 'test.status ' + arg )

   def check_ok(self, list):
      ok = True
      for item in list:
         value = session.get(item,None)
         if value is None:
            self.do_abort( item + ' not defined' )
            ok = False
         else:
            print("%s: %s" % (item, value))
      return ok

   def do_abort(self, msg):
      'Set the ABORT flag and print a message.'
      print("ABORT: %s" % msg)
      self.do_status( 'ABORT' )
      session[ 'message' ] = msg
      
   def do_pass(self, arg):
      self.do_status( 'PASS' )
      
   def do_fail(self, arg):
      self.do_status( 'FAIL' )
       
   def do_clear(self, key):
      'Clear a session value.  Or all of them.  USAGE: clear key_name OR clear ALL'
      if key == 'ALL':
         session.clear()
         print("Session cleared.")
      else:
         session.pop(key, None)
         print("Removed [" + key + "]")

   def do_sleep(self, secs):
       time.sleep(int(secs))

   ############################################################################
   #
   #  Administrative Bits
   #
   ############################################################################   
   def do_session(self, arg):
      'Dump session values'
      print('------------------------------------------------------------')
      print('                        SESSION')
      print('------------------------------------------------------------')
      for key in sorted(session.keys()):
         print("%-25s: %s" % (key, str(session[key])))
      print('')

   def do_bye(self, arg):
      return True
	  
   def do_exit(self, arg):
      return True

   def do_quit(self, arg):
      return True

   def default(self, line):
      print('?Syntax Error: unknown command {0}'.format(line))

robot = KTRobot()
robot.cmdloop()

print("Test Status: %s" % session.get( 'test.status', 'UNKNOWN' ))
