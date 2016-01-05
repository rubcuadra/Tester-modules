import constants as c
from boto.ec2 import connect_to_region #instancestatus
from boto.s3.lifecycle import Lifecycle, Transition, Rule
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.sqs
import boto.sqs.message
from boto.sqs.message import RawMessage
from collections import Counter
import os
class ec2Connector:
	def __init__(self,instancesId,region=c.region,access_key=c.accessKey,secret_access_key=c.secretKey):
		self.cnxn = connect_to_region(region,aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
		self.instanceId = instancesId
		self.instance = self._getInstance()
	def _getInstance(self):
		return self.cnxn.get_all_instances(self.instanceId)[0].instances[0]
	def getInstanceId(self):
		return self.instanceId
	def getStatus(self): #Returns a Dictionary where Running=16, Stopped=80
		return {'code':self.instance.state_code,'state':self.instance.state} 
	def getIP(self):
		return {'private':self.instance.private_ip_address,'public':self.instance.ip_address}
	def getUrl(self,_type='public_dns'):#'https://%s/status/'%self.instance.ip_address if self.instance.public_dns_name else False
		idu={'public_dns':self.instance.public_dns_name,'private_dns':self.instance.private_dns_name,'public_ip':self.instance.ip_address,'private_ip':self.instance.private_ip_address}
		return 'http://%s/status/Default.aspx'%idu[_type]		
	def updateInstance(self):
		self.instance = self._getInstance()
	def startInstance(self):
		if self.instance.state_code != 16:
			print 'Starting %s...'%self.instanceId
			self.instance.start()
			self.updateInstance()
		else:
			print 'Instance already Running'
	def stopInstance(self):
		if self.instance.state_code == 16:
			print 'Stopping %s...'%self.instanceId
			self.instance.stop()
			self.updateInstance()
		else:
			print 'Instance already stopped'
	def isReady(s):
		status = s.cnxn.get_all_instance_status(instance_ids=s.instanceId)
		if status:  #passed  ,   initializing    ,
			return status[0].instance_status.details['reachability']==status[0].system_status.details['reachability']=='passed' 
		return False
		 
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_value, traceback):
		pass
	def __del__(self):
		pass
class s3Connector:
	def __init__(self, storage,accessKey=c.accessKey,secretKey=c.secretKey):
		self.cnxn = S3Connection(accessKey,secretKey)
		self.storageName = storage
		self.bucket = self.cnxn.get_bucket(self.storageName)
	def getAllFiles(self):
		return (f for f in self.bucket)
	def getFile(self,key):
		return self.bucket.get_key(key)
	def downloadFile(self,filename):
		f = self.getFile(filename)
		if f==None or f.name=='':
			print 'File %s not found'%filename
			return False
		f.get_contents_to_filename(filename)
		return True
	def downloadAllFiles(self):
		for f in self.getAllFiles():
			f.get_contents_to_filename(f.name)
	def uploadFile(self,filename):
		k = Key(self.bucket)
		k.key = filename
		k.set_contents_from_filename(os.getcwd()+c.div+filename)
class sqsConnector:
	def __init__(self,queueName,region=c.region,accessKey=c.accessKey,secretKey=c.secretKey):
		self.queueAslist=[]
		self.sqs = boto.sqs.connect_to_region(region,aws_access_key_id=accessKey,aws_secret_access_key=secretKey)
		self.queueName = queueName
		self.queue = self.sqs.get_queue(queueName)
		self.queue.set_message_class(RawMessage)
		self.fillQueueAsList()
	def getCount(self,function,*args): #This function accepts lambdas as well args to obtain the number of msgs
		return Counter([function(message,*args) for message in self.queueAslist])
	def fillQueueAsList(self):
		while self.queue.count():
			response = self.queue.get_messages(num_messages=10,visibility_timeout=60) 
			for message in response:
				self.queueAslist.append(message.get_body())
	def printQueue(self):
		for message in self.queueAslist:
			print message
	def getQueueAsList(self):
		return self.queueAslist
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_value, traceback):
		pass
	def __del__(self):
		pass