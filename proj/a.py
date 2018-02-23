# ----- receiver.py -----
from socket import *
import sys
import select
import thread
import threading
from apscheduler.scheduler import Scheduler
from shutil import copyfile
from socket import error as socket_error	
import logging
logging.basicConfig()
import time
	
def handler(conn, address):
	t0 = time.time() #It is similar to receiver which handles the host and address,port
	excep_error=0
	while True:
		try:
			#print("*****************************************"+str(address)+"*********************************")
			data= conn.recv(buf) #The data in buffer is received and stored in data
			if(data):
				if(".dat" in data):
					received_from_node=data.split(".dat")[0].strip() #retreiving the file name without tags
					###print("RECEIVED FROM NODE: "+str(received_from_node))
					###print neigh
					try:
						b=neigh.index(received_from_node)
					except ValueError:
						neighbor=False
						#print("cant find")
					else:
						neighbor=True
						distance_from_node=neighCost[b]
						###print("INDEX==="+str(b))
						print("distance_from_node==="+str(distance_from_node))##here we are calculating the distance
						print("RECEIVED FROM NODE: "+str(received_from_node))
					###print("----------------------------------"+str(address))
				
				if(neighbor):
					data=data.split("\r\n")
					###print(data)
					directly_connected_nodes=int(data[1].strip())# Here we are finding the directly connected nodes i.e, neighbors and running the loop over that number
					for c in range(2,directly_connected_nodes+2):
						#print(data[c].strip())
						if(str( data[c].strip().split(" ")[0] )==name_of_the_file.split(".")[0]): #If node is receiveing from itself then go to next line in data file
							continue
						try:
							b=known.index(str( data[c].strip().split(" ")[0] ))
						except ValueError:
							known.append(str( data[c].strip().split(" ")[0] )) # If value error occurs then find cost and add to dist_cost array
							dist_cost.append(distance_from_node+float( data[c].strip().split(" ")[1] ))
							hop_next.append(received_from_node)
							learned_from_node.append(received_from_node)
							#print("cant find")
						else: # Here we are finding the shortest path to the all the nodes in the network
							if(  dist_cost[b]>(distance_from_node+(float( data[c].strip().split(" ")[1] )))  ):
								dist_cost[b]=distance_from_node+(float( data[c].strip().split(" ")[1] ))
								hop_next[b]=received_from_node
								learned_from_node[b]=received_from_node
							if(hop_next[b]==received_from_node):
								dist_cost[b]=distance_from_node+(float( data[c].strip().split(" ")[1] ))
					#print("----------------------------------"+str(address))
					#f=open(str(name_of_the_file.split(".")[0])+"_up.dat",'w')
					#f.write(str(len(known)-1)+"\n")
					#for i in range(1,len(known)-1):
					#	f.write(str(known[i])+" "+str(dist_cost[i])+" "+str(learned_from_node[i])+"\n")
					#f.write(str(known[len(known)-1])+" "+str(dist_cost[len(known)-1])+" "+str(learned_from_node[len(known)-1]))
					#f.close()
		except socket_error as serr:
			###print(str(serr.errno))
			excep_error=int(serr.errno)
		if excep_error==10054: # Checking whether error value is 10054 and closing the connection handling the error cases
			conn.close();
			break

def create_initial_routes(): # Here we are creating the table with initial routes with costs and neighbors names 
	a = open(name_of_the_file,'rb')
	#known.append(str(name_of_the_file.split(".")[0]))
	#dist_cost.append(-1.0)
	#hop_next.append("-")
	#learned_from_node.append(str(name_of_the_file.split(".")[0]))
	content_in_the_file = a.readlines()
	directly_connected_nodes=int(content_in_the_file[0].strip())
	for c in range(1,directly_connected_nodes+1):
		neigh.append(content_in_the_file[c].strip().split(" ")[0]) # Appending the adjacent nodes
		neighCost.append(float(content_in_the_file[c].strip().split(" ")[1]))# Appending the adjacent nodes cost
		known.append(content_in_the_file[c].strip().split(" ")[0])# Initially just appending the adjacent neigbors
		neighbors.append(content_in_the_file[c].strip().split(" ")[0])#Initially just appending the adjacent neigbors 
		dist_cost.append(float(content_in_the_file[c].strip().split(" ")[1]))#Initially just appending the adjacent neigbors costs
		hop_next.append(content_in_the_file[c].strip().split(" ")[0])# Set with the next hop nodes in the shortest path
		learned_from_node.append(str(name_of_the_file.split(".")[0]))#Set with the node name from which it is learned 
		send.append(socket(AF_INET,SOCK_STREAM))
	#print(known)
	#print(dist_cost)
	#print(hop_next)
	a.close()
	
	f=open(str(name_of_the_file.split(".")[0])+"_up.dat",'w') # opening a new file with name appending with _up.dat in the writing mode
	f.write(str(len(known)-1)+"\n")
	for i in range(1,len(known)-1):
		f.write(str(known[i])+" "+str(dist_cost[i])+" "+str(learned_from_node[i])+"\n")
	f.write(str(known[len(known)-1])+" "+str(dist_cost[len(known)-1])+" "+str(learned_from_node[len(known)-1])) # writing the known nodes and their costs along with learned from nodes in the _up.dat files
	f.close() #closing the opened file

"""
def job_send():
	#content_in_the_file==a.dat
	#lines=a_up.dat=y
	print("!@#$%^&*()!@#$%^&*()!@#$%^&*()       SENDING      !@#$%^&*()!@#$%^&*()")
	a = open(name_of_the_file,'rb')												#open data file
	content_in_the_file = a.readlines()											#store lines in data file
	directly_connected_nodes=int(content_in_the_file[0].strip())									#number of neighbors
	a.close()																#close file
	neigh=[]
	neighCost=[]
	for a in range(1,directly_connected_nodes+1):
		neigh.append(str(content_in_the_file[a].split(" ")[0]))					#store neigbors in array
		neighCost.append(int(content_in_the_file[a].split(" ")[1]))				#store dist_cost in array
	print("########## PRINT NEIGHBORS AND COSTS")
	for a in range(len(neigh)):
		print(str(neigh[a])+"\t"+str(neighCost[a]))							
		
		
	b=open(str(name_of_the_file.split(".")[0])+"_up.dat","rb")						#new file which store updated information
	lines=b.readlines()
	b.close()
	f=open(str(name_of_the_file.split(".")[0])+"_up.dat","rb")
	data=str(name_of_the_file)+"\r\n"+f.read(buf)
	while (data):
		for c in range(1,directly_connected_nodes+1):
			excep_error=0;
			try:
				send[c-1].connect((host,9000+ord(content_in_the_file[c].strip().split(" ")[0])))
			except socket_error as serr:
				print(str(serr.errno))
				excep_error=int(serr.errno)
			except IndexError:
				send.append(socket(AF_INET,SOCK_STREAM))
				neighbors.append(content_in_the_file[c].split(" ")[0].strip())
				try:
					send[c-1].connect((host,9000+ord(content_in_the_file[c].strip().split(" ")[0])))
				except socket_error as serr:
					print(str(serr.errno))
					excep_error=int(serr.errno)
			if(excep_error!=10061):
				data=str(name_of_the_file)+"\r\n"
				for up in lines:
					try:
						up.split(" ")[2]
					except IndexError:
						data=data+str(up)
					else:
						if (    str(up.split(" ")[2].strip()) == str((content_in_the_file[c].strip().split(" ")[0]))  ):
							continue
						else:
							try:
								b=neigh.index(   str(up.split(" ")[0].strip())  )
							except:
								print("ooooooooooooooo\nooooooooooooooo")
								print("INDEX ERROR")
								print("ooooooooooooooo\nooooooooooooooo")
							else:
								try:
									c=known.index(   str(up.split(" ")[0].strip())  )
								except:
									print("INDEX ERROR")
								else:
									if dist_cost[c]>neighCost[b]:
										dist_cost[c]=neighCost[b]
										learned_from_node[c]=neigh[b]
										data=data+str(known[c])+" "+str(dist_cost[c])+" "+str(learned_from_node[c])+"\r\n"
										continue
									elif(dist_cost[c]!=-1.0):
										if (   str(learned_from_node[c])==str(name_of_the_file.split(".")[0])   ):
											dist_cost[c]=neighCost[b]
											data=data+str(known[c])+" "+str(dist_cost[c])+" "+str(learned_from_node[c])+"\r\n"
											continue								
							data=data+str(up)
				if(send[c-1].send(data)):
					print "sending to ..."+str(c-1)
					print("+++++++++++++++++++++++++++++++++++++++++\n+++++++++++++++++++++++++++++++++++")
					print(data)
					print("+++++++++++++++++++++++++++++++++++++++++\n+++++++++++++++++++++++++++++++++++")
		data = f.read(buf)
	f.close()
	f=open(str(name_of_the_file.split(".")[0])+"_up.dat",'w')
	f.write(str(len(known)-1)+"\n")
	for i in range(1,len(known)-1):
		f.write(str(known[i])+" "+str(dist_cost[i])+" "+str(learned_from_node[i])+"\n")
	f.write(str(known[len(known)-1])+" "+str(dist_cost[len(known)-1])+" "+str(learned_from_node[len(known)-1]))
	f.close()
	for i in range(1,len(known)):
		print (str(name_of_the_file.split(".")[0])+"------"+str(known[i])+">>>>>>>"+str(dist_cost[i]))
	#print(known)
	#print(dist_cost)
	#print(hop_next)
"""  
  
def sender_sd():
	t0 = time.time()
	
	a = open(name_of_the_file,'rb')												#Here we are opening the data file
	neighbors = a.readlines()											#store lines in data file into neighbors
	directly_connected_nodes=int(neighbors[0].strip())									# find the number of neighbors directly connected
	a.close()																#close the file opened
	del neigh[:]
	del neighCost[:]
	for a in range(1,directly_connected_nodes+1):
		neigh.append(str(neighbors[a].split(" ")[0]))					#store neighbors in array neigh
		neighCost.append(float(neighbors[a].split(" ")[1]))				#store dist_cost in array neighCost
								
	
	for neighNode in neigh:
		try:
			knownIndex=known.index(  str(neighNode)   )
		except ValueError:
			print ("###################    ROUTE HAS BEEN ADDED    **************") # If the value error occurs then the route is changed
			known.append(  str(neighNode)  )
			costIndex=neigh.index(  str(neighNode)   )
			dist_cost.append(float(neighCost[costIndex]))
			hop_next.append(str(neighNode))
			learned_from_node.append(str(name_of_the_file.split(".")[0]))
	
	for knownNode in known:
		try:
			neighIndex=neigh.index(  str(knownNode)   )
		except ValueError:
			knownIndex=known.index(knownNode)
			if learned_from_node[knownIndex]==str(name_of_the_file.split(".")[0]):
				print ("##############      DELETED ROUTE DETECTEDD    #################")
				node_delete=known[knownIndex]
				del known[knownIndex]
				del dist_cost[knownIndex]
				del learned_from_node[knownIndex]
				del hop_next[knownIndex]
				for lnd in range(len(known)): # If the route is deleted then the least cost is calculated over here
					if learned_from_node[lnd]==node_delete:
						dist_cost[lnd]=9999.0 # we are setting the infinite distance as 9999
			#continue
		else:
			knownIndex=known.index(knownNode)
			if neighCost[neighIndex]<=dist_cost[knownIndex]  or  learned_from_node[knownIndex]==str(name_of_the_file.split(".")[0]):
				print ("##############      ROUTEs HAS BEEN CHANGED    ###############")
				dist_cost[knownIndex]=neighCost[neighIndex]
				learned_from_node[knownIndex]=str(name_of_the_file.split(".")[0])
				hop_next[knownIndex]=str(knownNode)
	print ("##############      FILE IS UPDATING   ###############")	
	f=open(str(name_of_the_file.split(".")[0])+"_up.dat",'w') #Here we are updating the file
	f.write(str(len(known))+"\n")
	for i in range(len(known)-1):
		f.write(str(known[i])+" "+str(dist_cost[i])+" "+str(learned_from_node[i])+"\n")
	f.write(str(known[len(known)-1])+" "+str(dist_cost[len(known)-1])+" "+str(learned_from_node[len(known)-1]))
	f.close()
	
	b=open(str(name_of_the_file.split(".")[0])+"_up.dat","rb")						#new file which store updated information
	known_nodes=b.readlines()
	b.close()
	f=open(str(name_of_the_file.split(".")[0])+"_up.dat","rb")
	data=str(name_of_the_file)+"\r\n"+f.read(buf)
	nodesSent=0
	while (data):
		for c in range(1,directly_connected_nodes+1):
			excep_error=0;
			try:
				send[c-1].connect((host,9000+ord(neighbors[c].strip().split(" ")[0])))
			except socket_error as serr:
				###print(str(serr.errno))
				excep_error=int(serr.errno)
			except IndexError:
				send.append(socket(AF_INET,SOCK_STREAM))
				neighbors.append(neighbors[c].split(" ")[0].strip())
				try:
					send[c-1].connect((host,9000+ord(neighbors[c].strip().split(" ")[0])))
				except socket_error as serr:
					###print(str(serr.errno))
					excep_error=int(serr.errno)
			if excep_error==10054:
				send[c-1].close()
				return
			if(excep_error!=10061):
				data=""
				nodesSent=0
				for up in known_nodes:
					try:
						up.split(" ")[2]
					except IndexError:
						continue
					else:
						if (    str(up.split(" ")[2].strip()) == str((neighbors[c].strip().split(" ")[0]))  ):
							continue
						else:
							nodesSent=nodesSent+1
							data=data+str(up)
				data=str(name_of_the_file)+"\r\n"+str(nodesSent)+"\r\n"+data
				if(send[c-1].send(data)):
					print ("################       SENDING    ##############")
					
		data = f.read(buf)
	f.close()
	op.append(0)
	print("+++++++++++++++++++++++++  OP-"+str(len(op))+"  ++++++++++++++++++++++++++")
	print ("NW_Node\tFINALCost\tNextHop\tNODE_LearnedFrom")
	for i in range(len(known)):
		print (  str(known[i])+"\t"+str(dist_cost[i])+"\t"+"\t"+str(hop_next[i])+"\t"+"\t"+str(learned_from_node[i])    )
		###print (str(name_of_the_file.split(".")[0])+"------"+str(known[i])+">>>>>>>"+str(dist_cost[i]))
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	t1 = time.time()
	print ("???????????????????\n???????????????????\n???????????????????")
	print ("\t\t")+str(t1-t0)
	print ("???????????????????\n???????????????????\n???????????????????")
	
	
name_of_the_file=sys.argv[2]
a = open(name_of_the_file,'rb')
line_in_the_file = a.readlines()
a.close()
op=[]
neigh=[]
neighCost=[]
neighbors=[]
known=[]
dist_cost=[]
hop_next=[]
learned_from_node=[]
send=[]
host=sys.argv[1]
create_initial_routes()
port=9000+ord(name_of_the_file.split(".")[0])
addr = (host,port)
s = socket(AF_INET,SOCK_STREAM)
s.bind((host,port))
s.listen(5)
buf=1024
#Start the scheduler
sched = Scheduler()
sched.start()
sched.add_interval_job(sender_sd, seconds=15,max_instances=100)
#threading.Timer(15.0, sender_sd).start()
while True:
	print 'waiting for connection...'+str(addr)
	conn, address = s.accept()
	print '...connected from:', address
	thread.start_new_thread(handler, (conn, address))