import docker
import time
import json
client = docker.from_env()

# #Reinitialize the swarm To make sure the swarm is empty and new
# client.swarm.leave(force=True)
# client.swarm.init()
# #Creating the network with the name se443_test_net and the subnet and driver and scope
# client.networks.create("se443_test_net", driver="overlay", scope="global", ipam=docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet='10.10.10.0/24')]))

#Printing the network details required
for net in client.networks.list():
    if net.name == "se443_test_net":
        print("Network ID: ", net.id)
        print("Network Name: ", net.name)
        print("Network Creation Date: ", net.attrs['Created'])

print("----------------------------------------------------------------------------------------------------------------------")    

#Creating subscriber service with scale of 3 (replicas) with the name Subscriber and the restart policy of 'any' (which is always) with the image efrecon/mqtt-client                
client.services.create("efrecon/mqtt-client", name="Subscriber",  restart_policy=docker.types.RestartPolicy(condition="any"), networks=["se443_test_net"], 
                       command='sub -h host.docker.internal -t alfaisal_uni -v').scale(3)
print("Susbcriber's ID:" , client.services.list()[0].id)
print("Susbcriber's Name:" , client.services.list()[0].name)
print("Susbcriber's Creation Date:" , client.services.list()[0].attrs['CreatedAt'])
print("Susbcriber's Number Of Replicas:" , client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

print("----------------------------------------------------------------------------------------------------------------------")   

#Creating publisher service with scale of 3 (replicas) with the name Publisher and the restart policy of 'any' (which is always) with the image efrecon/mqtt-client
client.services.create("efrecon/mqtt-client", name="Publisher",  restart_policy=docker.types.RestartPolicy(condition="any"), networks=["se443_test_net"], 
                       command='pub -h host.docker.internal -t alfaisal_uni -m "<200304 - Meteb - Almadi - 0554271113>"').scale(3)
print("Publisher's  ID:" , client.services.list()[0].id)
print("Publisher's  Name:" , client.services.list()[0].name)
print("Publisher's  Creation Date:" , client.services.list()[0].attrs['CreatedAt'])
print("Publisher's  Number Of Replicas:" , client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

print("----------------------------------------------------------------------------------------------------------------------")   
print("Leave it running for 5 minutes...")
time.sleep(300)
print("----------------------------------------------------------------------------------------------------------------------\n")

#Cleanup and termination

print("Terminating Publisher, Subscriber, and Network services and finally leaving the swarm")

client.services.get("Publisher").remove()
print("Publisher Terminated....")

client.services.get("Subscriber").remove()
print("Subscriber Terminated....")

client.networks.get("se443_test_net").remove()
print("Network Terminated....")

client.swarm.leave(force=True)
print("Swarm Left Forcefully....")
