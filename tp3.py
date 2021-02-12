# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 20:01:46 2021

@author: Hajar
"""

import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import random
from spade.message import Message
from spade.template import Template


# ------------------- RandomWalkerAgent -------------------

class RandomWalker(Agent):
    class RandomWalkerBehav(CyclicBehaviour):
        async def on_start(self):
            print("Comportement démarrer RandomWalker ! \n")
            self.prix_max = 3000
            self.prix__min = 1500
            self.propostion = random.randrange(self.prix__min, self.prix_max)

        async def run(self):
            msg = Message(to="Careful@jabber.lqdn.fr")  # Instantiate the message
            msg.body = str(self.propostion)
            await self.send(msg)
            
            if msg:
                msg = await self.receive(timeout=20)  # wait for a message for 10 seconds
                recv_proposition= int(msg.body)
                print("RandomWalker : "+str(self.propostion)+" C'est trop petite")
                self.propostion = random.randrange(recv_proposition, self.prix_max)
                print("RandomWalker : Si vous pouvez me donner "+str(self.propostion)+" \n")
                msg = Message(to="Careful@jabber.lqdn.fr")  # Instantiate the message
                msg.body = str(self.propostion)
                await asyncio.sleep(10)
                await self.send(msg)
                
            else:
                print("J'ai rien recu")
                    
        async def on_end(self):
            await self.agent.stop()
                    
    async def setup(self):
        #print("RandomWalker : Agent démarrer !")
        b = self.RandomWalkerBehav()
        self.add_behaviour(b)
            
            
# -------------------- CarefulAgent -------------------
class CarefulAgent(Agent):
    class CarefulBehav(CyclicBehaviour):
        async def on_start(self):
            print("Comportement démarrer Careful ! \n")
            self.prix_max = 3000
            self.prix__min = 1500
            self.propostion = random.randrange(self.prix__min, self.prix_max)

        async def run(self):
            msg = await self.receive(timeout=20)  # wait for a message for 10 seconds
            
            if msg:
                print("CarefulAgent : C'est trop "+str(self.propostion)+" ! !")
                self.propostion = random.randrange(self.prix__min, self.prix_max)
                print("CarefulAgent : Je vous donne "+str(self.propostion)+"\n")
                msg = Message(to="RandomWalker1@jabber.lqdn.fr")  # Instantiate the message
                msg.body = str(self.propostion)
                await asyncio.sleep(10)
                await self.send(msg)
            else:
                print("J'ai rien recu")
                    
        async def on_end(self):
            pass
        
    async def setup(self):
       #print("CarefulAgent : Agent démarrer !")
       b = self.CarefulBehav()
       self.add_behaviour(b)
            
# ---------------MAIN---------------
if __name__ == "__main__":
    Careful = CarefulAgent("Careful@jabber.lqdn.fr", "123456789")
    future = Careful.start()
    future.result()  # wait for receiver agent to be prepared.

    RandomWalker = RandomWalker("RandomWalker1@jabber.lqdn.fr", "123456789")
    future = RandomWalker.start()
    future.result()
    
    while RandomWalker.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            RandomWalker.stop()
            Careful.stop()
            break
    print("Agents finished")
        