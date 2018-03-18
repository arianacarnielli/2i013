from soccersimulator import Vector2D, SoccerState, SoccerAction, Ball
from soccersimulator import Strategy
from soccersimulator.settings import *
from .tools import ToolBox, Comportement, ProxyObj

class Comportements(Comportement):

    RUN_COEF = maxPlayerAcceleration
    GO_COEF = maxPlayerAcceleration/3.
    COEF_DRIBLE= 0.5
    BIG_SHOOT_COEF = 2
    SHOOT_COEF = maxPlayerShoot/3.
    THROW_COEF = maxPlayerShoot

    def __init__(self,state):
        super(Comportements,self).__init__(state)
    
    def run(self,p):
        return SoccerAction(acceleration=(p-self.playerPos).normalize()*self.RUN_COEF)
    
    def go(self,p):
        return SoccerAction(acceleration=(p-self.playerPos).normalize()*self.GO_COEF)
    
    def shoot(self, acc):
        if self.canShoot:
            return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*acc)
        return SoccerAction()
    
    def bigshoot(self):
    	if self.canShoot:
    		return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*self.BIG_SHOOT_COEF)
    	return SoccerAction()
        
    def degage(self):
        if self.canShoot:
            return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos)*self.THROW_COEF)
        return SoccerAction()

    def drible (self):
        if self.canShoot:
            return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*self.COEF_DRIBLE)
        return SoccerAction()

    def returnToGoal(self):
        return SoccerAction(self.vecMyGoal - self.playerPos) 

    def goCorner(self):
        COEF_CORNERX=0.2
        COEF_CORNERY=0.2
        if (self.myTeam==1):
            if (self.ballPos.y < self.height/2):
                return SoccerAction(shoot=Vector2D(self.width*(1-COEF_GOCORNERX), self.height*COEF_CORNERY-self.playerPos))
            else:
                return SoccerAction(shoot=Vector2D(self.width*(1-COEF_GOCORNERX), self.height*(1-COEF_CORNERY)-self.playerPos))
        else:
            if(self.ballPos.y<self.height/2):
                return SoccerAction(shoot=Vector2D(self.width*(COEF_GOCORNERXERX), self.height*COEF_CORNERY-self.playerPos))
            else:
                return SoccerAction(shoot=Vector2D(self.width*(COEF_GOCORNERXERX), self.height*(1-COEF_CORNERY)-self.playerPos))

    def returnToCamp(self):
        mates = self.get_mate
        nbup=0
        nbdown=0
        
        for mate in mates:
            if mate!=self.playerPos:

                if mate.y > self.height/2:
                    nbup=nbup+1
                
                if mate.y < self.height/2:
                    nbdown=nbdown+1

        if nbup>nbdown:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/4, (self.height*2)/5)
                - self.playerPos).normalize()*self.RUN_COEF)
        if nbdown>nbup:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/4, (self.height*3)/5)
                - self.playerPos).normalize()*self.RUN_COEF)
        else:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/5, (self.height)/2)
                - self.playerPos).normalize()*self.RUN_COEF)


    def runBallPredicted(self, n=0):
        pos_ballspeed = self.ballSpeed
        pos_ballspeed.scale(n)
        pos_ball= self.ballPos + pos_ballspeed

        return SoccerAction(pos_ball - self.playerPos)

    def playerPosPredicted(self, player, n=0):
        pos_playerspeed = player.playerSpeed
        pos_playerspeed.scale(n)
        pos_player= player.playerPos + pos_playerspeed

        return SoccerAction(shoot=(pos_player - self.playerPos))

    def passToMostCloseMate(self, coop):
 
        mate = self.mostCloseMate(coop)
        #[self.playerPos.distance(m)for m in mates if m!=self.playerPos]
        print ("....pass....",self.playerPos,mate,(self.playerPos-mate.normalize)()*5)
        return SoccerAction(shoot=(mate-self.playerPos).normalize()*5)

    
class ConditionGoal(ProxyObj):
    def __init__(self,state):
        super(ConditionGoal,self).__init__(state)

    def inGoalZone(self):
        return (self.myGoalBall_distance<40)

    def inGoal(self):
        coordx= self.playerPos.x
        coordy= self.playerPos.y
        target = 0 if self.id_team == 1 else 1

        return ((((target == 0)and (coordx<=10))|
                ((target == 1) and(coordx>140))) 
                and (coordy<=50 and coordy>=40))

class ConditionDribleur(ProxyObj):
    COEF_DISTMIN=45
    COEF_BALL = 0.1
    def __init__(self,state):
        super(ConditionDribleur,self).__init__(state)

    def close_opp(self):
        opp = self.get_opponent
        for players in opp:
            if (self.playerPos.distance(players)<30):
                return True
        return False

    def close_ball(self):
        return self.playerPos.distance(self.ballPos)<self.COEF_BALL*self.width

    def close_goal(self):
        return self.playerPos.distance(self.vecTheirGoal)<self.COEF_DISTMIN

class ConditionAttaque(ProxyObj):
    def __init__(self, state, COEF_DIST=1):
        super(ConditionAttaque,self).__init__(state)
        self.COEF_DIST = COEF_DIST	
    def close_goal(self):
        return self.playerPos.distance(self.vecTheirGoal) < self.COEF_DIST*self.width

class ConditionPoly(ProxyObj):
    COEF_SHOOT = 0.25

    def inCamp(self):
        return (((self.myTeam==1) and (self.ballPos.x <= self.width/2))
            | ((self.myTeam==2) and (self.ballPos.x >= self.width/2)))

    def oppCloseBall(self):
        opps= self.get_opponent
        for opp in opps:
            if self.ballPos.distance(opp)<5:
                return True
        return False 

    def close_goal(self):
        print(self.playerPos.distance(self.vecTheirGoal))
        return self.playerPos.distance(self.vecTheirGoal)<self.COEF_SHOOT*self.width
        
    def mateHaveBall(self, coop):
        mates=coop
        for mate in mates:
            if mate.distance(self.ballPos)< 50:
                return True
        return False

    def canPass(self):
        if self.mateMostCloseDistance < 150:
            return True
        else:
            return False


class ConditionAilier(ProxyObj):
    COEF_CORNER=0.2
    COEF_ATTAC =0.3

    def inCamp(self):
        return (((self.myTeam==1) and (self.ballPos.x <= self.width/2))
            | ((self.myTeam==2) and (self.ballPos.x >= self.width/2)))

    def inCorner(self):
        return (((self.myTeam==1) and (self.playerPos.x>=self.width*(1-self.COEF_CORNER)))
            | (self.myTeam==2) and (self.playerPos.x<= self.width*self.COEF_CORNER))

    def mateHaveBall(self, coop):
        mates=coop
        for mate in mates:
            if mate.distance(self.ballPos)< 40:
                return True
        return False

    def canPass(self,coop):
        return (((self.myTeam==1) and (self.mostCloseMate(coop).x>=self.width*(1-self.COEF_ATTAC)))
            | (self.myTeam==2) and (self.mostCloseMate(coop).x<= self.width*self.COEF_ATTAC))


def fonceur(I):
    if not I.canShoot:
        return I.run(I.ballPos)
    else:
        if I.close_goal():
            return I.bigshoot()
        else:
        	return I.shoot(0.5)

def versatile (I):
    mates= I.get_mate
    if I.inCamp():
        if not I.canShoot:
            return I.runBallPredicted(2)
        else:
            return I.shoot(2)
    else:
        if not I.mateHaveBall(mates):
            if I.oppCloseBall():
                return I.returnToCamp()
            else:
                if not I.canShoot:
                    return I.run(I.ballPos)
                else:
                    if I.canPass():
                        print("jes suis ici")
                        return I.passToMostCloseMate(mates)

                    else:
                        if I.close_goal():
                            return I.shoot(4)
                        else:
                            print("nope")
                            return I.shoot(0.64)
        else:
            return I.returnToCamp()

def ailier(I):
    mates= I.get_mate
    if I.inCamp():
        if I.mateHaveBall(mates):
            return I.returnToCamp()
        else:
            if not I.canShoot:
                return I.runBallPredicted(2)
            else:
                return I.goCorner()
    else:
        if not I.inCorner():
            if I.canShoot:
                return I.goCorner()
            else:
                I.runBallPredicted(2)
        else:
            if I.canShoot:
                if I.canPass(mates):
                    mate=mostCloseMate()
                    return I.playerPosPredicted(mate)
            else:
                return I.goCorner()

def dribleur(I):

    if  I.close_opp():
        if I.canShoot:
            return I.shoot(2)
        else: 
            return I.runBallPredicted(2)
    else:
        if I.canShoot:
            if I.close_goal():
                return I.shoot(8)
            else:
                return I.drible() 

        else:
            return I.runBallPredicted(2)


def goal(I):
    if I.inGoalZone():
        if I.canShoot:
            return I.degage()
        else:
            return I.runBallPredicted(5)
    else:
        if not I.inGoal():
            return I.returnToGoal()
        else:
            return None
