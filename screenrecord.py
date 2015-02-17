#!/usr/bin/env python
##
##  Python VNC Screen Recorder API
##
##  This was created to record Python Selenium tests.
##
##  Author : Bharath Yarlagadda
##
import sys, time, socket, os, os.path, subprocess, signal, time, threading
from flv import FLVWriter
from rfb import RFBNetworkClient, RFBError, PWDFile, PWDCache
from video import FLVVideoSink, str2clip, str2size

class ScreenRecorder:

  def __init__(self, host="localhost", port=5900, filepath="recording.flv"):
    self.client = ''
    self.writer = ''
    self.fp = ''
    self.pid = 0
    self.bool = True
    self.host= host
    self.port= port
    self.filename= filepath

  def stoprecording(self):
    self.bool = False

  def recording(self):
    try:
      print >>sys.stderr, 'Started Recording'
      while self.bool:
        self.client.idle()
    except socket.error, e:
      print >>sys.stderr, 'socket error'
      retval = 1
    except RFBError, e:
      print >>sys.stderr, 'rfb error'
      retval = 1
    finally:
      self.client.close()
      self.writer.close()
      self.fp.close()
    print >>sys.stderr, 'Recording Stopped'

  def startrecorder(self, framerate=12, keyframe=120,
                preferred_encoding=(0,), pwdfile=None,
                blocksize=32, clipping=None,
                cmdline=None,debug=0):
    self.fp = file(self.filename, 'wb')
    if pwdfile:
      pwdcache = PWDFile(pwdfile)
    else:
      pwdcache = PWDCache('%s:%d' % (self.host,self.port))
    self.writer = FLVWriter(self.fp, framerate=framerate, debug=debug)
    sink = FLVVideoSink(self.writer, blocksize=blocksize, framerate=framerate, 
                        keyframe=keyframe, clipping=clipping, debug=debug)
    self.client = RFBNetworkClient(self.host, self.port, sink, 
                                   timeout=500/framerate, pwdcache=pwdcache, 
                                   preferred_encoding=preferred_encoding, 
                                   debug=debug)
    try:
      self.client.open()
      threading.Thread(target=self.recording).start()
    except socket.error, e:
      print >>sys.stderr, 'socket error'
      retval = 1
    except RFBError, e:
      print >>sys.stderr, 'rfb error'
      retval = 1
