import docker
import time
import json
client = docker.from_env()

#Reinitialize the swarm To make sure the swarm is empty and new
client.swarm.leave(force = True)
client.swarm.init()

#Print the swarm ID, name, and creation date
print("Swarm's ID: ", client.swarm.attrs['ID'])
print("Swarm's Name: ", client.swarm.attrs['Spec']['Name'])
print("Swarm's Creation Date: ", client.swarm.attrs['CreatedAt'])

print("----------------------------------------------------------------------------------------------------------------------")   
#Creating the network with the name se443_test_net and the subnet and driver and scope
client.networks.create("se443_test_net", driver = "overlay", scope ="global", ipam = docker.types.IPAMConfig(pool_configs = [docker.types.IPAMPool(subnet = "10.10.10.0/24")]))
for net in client.networks.list():
    if net.name == "se443_test_net":
        print("Network's ID: ", net.id)
        print("Network's Name: ", net.name)
        print("Network's Creation Date: ", net.attrs['Created'])

print("----------------------------------------------------------------------------------------------------------------------")

#Creating the broker service with scale of 3 (replicas) with the name broker and the restart policy of 'any' (which is always)
client.services.create("eclipse-mosquitto",name = "broker", restart_policy = docker.types.RestartPolicy(condition = "any")).scale(3) 
  
print("Leave it running for 5 minutes...") 
time.sleep(300)
print("----------------------------------------------------------------------------------------------------------------------") 

#Cleanup and termination
print("\nTermination Broker service...")
client.services.get("broker").remove()
print("Termination is complete")