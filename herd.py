from __future__ import print_function
import random
#import simpleplot

class Player():
    def __init__(self, vaccinated, tokens, risk):
        self._vax = vaccinated
        self._infected = False
        self._recovered = False
        self._tokens = tokens
	self._risk = risk
        
    def is_vaccinated(self):
        return self._vax
    
    def is_infected(self):
        return self._infected
    
    def become_patient_zero(self):
        self._infected= True
    
    def is_recovered(self):
        return self._recovered
    
    def get_tokens(self):
        return self._tokens
    
    def use_token(self):
        if self._tokens <= 0:
            print("Something went wrong, token out and infection tried")
            return None
        self._tokens -= 1
        if self._tokens == 0:
            self._recovered = True
        
    def get_risk_contact(self, spreader):
        res = False
        if spreader.get_tokens() >= 1:
            #print "trying to infect!" + str(self)
            if not self._infected and (random.random() <= self._risk):
                    self._infected = True
                    res = True
            spreader.use_token()
        return res
            
    def __str__(self):
        return str(self._vax) + "," + str(self._infected) + "," + str(self._recovered) + "," + str(self._tokens)
            
class Simulation:
    def __init__(self, vax, nvax, tokens, risk_vax, risk_non_vax):
        self._vax = [Player(True, tokens, risk_vax) for x in range(vax)]
        self._nvax = [Player(False, tokens, risk_non_vax) for x in range(nvax)]
        self._players = self._vax + self._nvax
        self._infected = []
        
    def start(self):
        last = self._nvax[-1]
        last.become_patient_zero()
        self._infected.append(last)
        last = self._nvax[-2]
        last.become_patient_zero()
        self._infected.append(last)
        
    def give_other_random_player(self, me):
        me_idx = self._players.index(me)
        rn = random.randrange(0, len(self._players))
        while self._players[rn] == me_idx:
            rn = random.randrange(0, nmax)
        return(self._players[rn])

    def step(self):
        for inf in self._infected:
            other = self.give_other_random_player(inf)
            if other.get_risk_contact(inf):
                self._infected.append(other)
            
    def __str__(self):
        res = "tot infetti: " + str(len(self._infected))
        res += "\ntot: " + str(len(self._players))
        res += "\nvax infetti: " + str(len(self.get_vax_infected()))
        res += "\nnon vax infetti: " + str(len(self.get_nvax_infected()))
        res += "\ntokens: " + str(self.total_tokens())
        return res
    
    def get_vax_infected(self):
        return [x for x in self._vax if x.is_infected()]
    
    def get_nvax_infected(self):
        return [x for x in self._nvax if x.is_infected()]
    
    def get_infected(self):
        return [x for x in self._players if x.is_infected()]
    
    def print_players(self):
        for p in self._players:
            print(p)
            
    def total_tokens(self):
        tokens = 0
        for inf in self._infected:
            tokens += inf.get_tokens()
        return tokens
            

def run_simulation(vax, nvax, risk_vax, risk_nvax, tokens):
    sim = Simulation(vax, nvax, tokens, risk_vax, risk_nvax)
    sim.start()
    while sim.total_tokens() != 0:
        sim.step()
    return [len(sim.get_infected())/float(vax+nvax), len(sim.get_vax_infected()) / float(vax), len(sim.get_nvax_infected()) / float(nvax)]

vax = 20
nvax = 5
combo_vax = [(25,5),(10,15)]
combo_risks=[(0.125,1),(0.125, 0.875)]
i = 0
v = 0
nv = 0
tot = 1000
for vax in combo_vax:
    for risk in combo_risks:
        f1=open('herd'+str(vax)+str(risk)+".tsv", 'w+')
	i = 0
	v = 0
	nv = 0
	for x in range(tot):
	    res = run_simulation(vax[0], vax[1], risk[0], risk[1], 3)
	    i += res[0]
	    v += res[1]
	    nv += res[2]
	    f1.write(str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2]) + "\n")
	print("sim: ", str(vax)+str(risk))
	print("media infetti: ", i / tot)
	print("print media vaccinati infetti: ", v / tot)
	print("print media non vaccinati infetti:", nv / tot)
	f1.close()

