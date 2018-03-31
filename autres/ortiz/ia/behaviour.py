# -*- coding: utf-8 -*-
from __future__ import print_function
from soccersimulator import SoccerAction, Vector2D
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, maxPlayerShoot, maxPlayerAcceleration, \
        ballBrakeConstant, playerBrackConstant
from .tools import Wrapper, StateFoot, normalise_diff, coeff_friction, is_upside, nearest_defender, \
    nearest_ball, get_empty_strategy, shootPower, passPower, get_oriented_angle, distance_horizontale
from .conditions import profondeurDegagement, largeurDegagement, empty_goal, is_close_goal, free_teammate, must_advance, is_defensive_zone, must_pass_ball, had_ball_control, must_assist
from math import acos, exp, atan2, sin, cos, atan
import random

distMaxFonceurCh1Shoot = GAME_WIDTH/3.
distMaxFonceurNormShoot = GAME_WIDTH/4.
fonceurCh1ApprochePower = 2.65
fonceurCh1HPPower = 4.6
fonceur100Power = 6.
fonceurHPPower = 4.3
controlPower = 1.2

def beh_fonceurNormal(state):
    if is_close_goal(state,distMaxFonceurNormShoot):
        return fonceurHPPower
    return fonceur100Power

def beh_fonceurChallenge1(state):
    if is_close_goal(state,distMaxFonceurCh1Shoot):
        return fonceurCh1HPPower
    return fonceurCh1ApprochePower

def beh_fonceur(state, shooter="normal"):
    if shooter == "ch1":
        return beh_fonceurChallenge1(state)
    return beh_fonceurNormal(state)

def power(dribble):
    CONTROL = 0.98
    DRIBBLE = 0.47#TODO
    if dribble:
        return DRIBBLE
    return CONTROL

def goWith(acceleration):
    """
    Se deplace avec cette acceleration
    """
    return SoccerAction(acceleration)

def goTo(state, dest):
    """
    Se deplacer vers cette destination
    """
    return goWith(normalise_diff(state.my_pos, dest, maxPlayerAcceleration))

def goToBall(state):
    """
    Se deplace vers la balle
    """
    return goTo(state, state.ball_pos)

def goToMyGoal(state):
    """
    Se deplace vers sa cage
    """
    return goTo(state, state.my_goal)

def kickAt(state,dest,powerShoot=maxPlayerShoot):
    """
    Frappe la balle en direction de dest avec
    une puissance de powerShoot
    """
    return SoccerAction(Vector2D(),normalise_diff(state.ball_pos, dest, powerShoot))

def shoot(state, power):
    """
    Fait un tir droit au but
    """
    return kickAt(state,state.opp_goal,power)

def control(state, powerControl=controlPower):
    """
    Avance avec la balle au pied parallelement
    a la ligne de touche
    """
    if is_close_goal(state, 50.):
        return shoot(state, powerControl)
    vect = (state.opp_goal - state.my_goal).normalize()
    return kickAt(state,state.ball_pos + vect*10,powerControl)

def dribble_prec(state, opp, angleDribble, powerDribble, coeffAD):
    """
    Fait un dribble avec une direction aleatoire
    soit vers l'axe, soit vers l'un des deux cotes
    """
    destDribble = Vector2D()
    oPos = opp.position
    angle = atan2(oPos.y-state.my_pos.y,oPos.x-state.my_pos.x)
    try:
        theta = atan((abs(oPos.y-state.my_pos.y) / abs(oPos.x-state.my_pos.x)))/acos(0.)
    except ZeroDivisionError:
        theta = 1.
    rand = exp(-coeffAD*theta)/2.
    quad = state.quadrant
    if random.random() < rand: # mauvais angle (vers l'adversaire)
        if quad == "II" or quad == "IV":
            angleDribble = -angleDribble
    else: # bon angle (vers la cage adverse)
        if quad == "I" or quad == "III":
            angleDribble = -angleDribble
    angle += angleDribble
    destDribble.x = cos(angle)
    destDribble.y = sin(angle)
    return kickAt(state, state.ball_pos + destDribble, powerDribble)

def dribble(state, opp, angleDribble, powerDribble, coeffAD):
    """
    Fait un dribble avec une direction aleatoire
    soit vers l'axe, soit vers l'un des deux cotes
    """
    destDribble = Vector2D()
    me_opp = (opp.position - state.my_pos).normalize()
    #me_goal = (state.opp_goal - state.my_pos).normalize()
    me_goal = (state.opp_goal - state.my_goal).normalize()
    angle = atan2(me_opp.y,me_opp.x)
    theta = get_oriented_angle(me_goal, me_opp)/acos(0.)
    rand = exp(-coeffAD*abs(theta))/2.
    quad = state.quadrant
    if random.random() < rand: # mauvais angle (vers l'adversaire)
        if theta < 0.:
            angleDribble = -angleDribble
    else: # bon angle (vers la cage adverse)
        if theta > 0.:
            angleDribble = -angleDribble
    angle += angleDribble
    destDribble.x = cos(angle)
    destDribble.y = sin(angle)
    return kickAt(state, state.ball_pos + destDribble, powerDribble)

def passBall(state, dest, maxPowerPasse, thetaPass, coeffPushUp):
    """
    Fait une passe vers un coequipier sans
    marquage
    TODO: il faut enlever la recherche du coequipier et plutot
    le passer en parametre => plus de strategie vide
    """
    vectGoal = (state.opp_goal - state.my_goal).normalize()
    destp = dest.position
    #if vectGoal.dot(dest.vitesse.copy().normalize()) >= 0.:
    #    destp += coeffPushUp*dest.vitesse
    vitesse = dest.vitesse.copy().normalize()
    if vectGoal.dot(vitesse) < 0.:
        vitesse = (-1) * vitesse
    destp += coeffPushUp*vitesse
    return kickAt(state, destp, passPower(state, destp, maxPowerPasse, thetaPass))

def passiveSituation(state, dico, decalX, decalY, rayRecept, angleRecept, rayReprise, angleReprise, distMontee, coeffPushUp):
    """
    Quand le joueur n'a pas le controle sur
    la balle:
    - si la balle approche il s'approche pour
    recevoir la balle
    - s'il est le joueur le plus proche de la
    balle ou s'il vient de faire un dribble/controle
    il se dirige de nouveau vers la balle
    - si un coequipier a franchi une distance
    avec la balle, il monte de le terrain
    pour lui proposer des solutions
    - sinon il se decale lateralement
    """
    vectBall = (state.my_pos - state.ball_pos).normalize()
    vectSpeed = state.ball_speed.copy().normalize()
    if state.distance(state.ball_pos) <= rayRecept and vectSpeed.dot(vectBall) >= angleRecept:
        return goToBall(state)
        #return tryInterception(state, dico)
    if state.is_nearest_ball() or had_ball_control(state, rayReprise, angleReprise):
        #return goToBall(state)
        return tryInterception(state, dico)
    if must_advance(state, distMontee):#40 distMontee
        return pushUp(state, coeffPushUp)
    if state.is_nearest_ball_my_team() and state.distance_ball(state.my_goal) < distMontee:
        return tryInterception(state, dico)
        #return goToBall(state)
    return cutDownAngle(state, 40., 20.)

def loseMark(state, rayPressing, distDemar):
    """
    Doc
    """
    opp = state.nearest_opponent(rayPressing)
    if opp is None:
        #return goTo(state,state.opp_goal)
        return shiftAside(state, 10, 20)
    return shiftAsideMark(state, opp, distDemar)



def shiftAsideMark(state, opp, distDemar):
    """
    Se decale en s'eloignant
    de l'adversaire
    """
    dest = None
    while True:
        dest = Vector2D.create_random(low=-1, high=1)
        dest.norm = distDemar
        dest += opp.position
        if state.is_valid_position(dest):
            break
    return goTo(state, dest)

def goForwardsMF(state, angleDribble, powerDribble, rayDribble, coeffAD, powerControl):
    """
    Essaye d'avance sur le milieu de terrain
    avec la balle et dribble lorsqu'il y a
    un adversaire en face
    """
    oppDef = nearest_defender(state, state.opponents, rayDribble)
    if oppDef is None:
        return control(state, powerControl)
    return dribble(state, oppDef, angleDribble, powerDribble, coeffAD)

def goForwardsPA(strat, state, alpha, beta, angleDribble, powerDribble, rayDribble, angleGardien, coeffAD, powerControl, distShoot):
    """
    Dans la zone d'attaque, essaye de se
    rapprocher davantage de la surface de
    reparation pour frapper et dribble
    l'adversaire en face de lui
    """
    oppDef = nearest_defender(state, state.opponents, rayDribble)
    if oppDef is None or empty_goal(strat, state, oppDef, angleGardien):
        if is_close_goal(state, distShoot):
            return shoot(state, shootPower(state, alpha, beta))
        else:
            return control(state, powerControl)
    return dribble(state, oppDef, angleDribble, powerDribble, coeffAD)

def goForwardsPA_mod(state, alpha, beta, angleDribble, powerDribble, rayDribble, angleGardien, coeffAD, powerControl, distShoot, maxPowerPasse, thetaPass, rayPressing, distPasse, angleInter, coeffPushUp):
    """
    Dans la zone d'attaque, essaye de se
    rapprocher davantage de la surface de
    reparation pour frapper et dribble
    l'adversaire en face de lui
    """
    tm = free_teammate(state, rayPressing)
    if is_close_goal(state, distShoot):
        if tm is not None and must_assist(state, tm, distPasse, angleInter, coeffPushUp):
            return passBall(state, tm, maxPowerPasse, thetaPass, coeffPushUp/2.)+pushUp(state, coeffPushUp)
        return shoot(state, shootPower(state, alpha, beta))
    oppDef = nearest_defender(state, state.opponents, rayDribble)
    if oppDef is not None:
        if tm is not None and must_pass_ball(state, tm, distPasse, angleInter):
            return passBall(state, tm, maxPowerPasse, thetaPass, coeffPushUp)+pushUp(state, coeffPushUp)
        return dribble(state,oppDef,angleDribble, powerDribble, coeffAD)
    return control(state, powerControl)

def goForwardsMF_mod(state, angleDribble, powerDribble, rayDribble, coeffAD, powerControl, maxPowerPasse, thetaPass, rayPressing, distPasse, angleInter, coeffPushUp):
    """
    Essaye d'avance sur le milieu de terrain
    avec la balle et dribble lorsqu'il y a
    un adversaire en face
    """
    oppDef = nearest_defender(state, state.opponents, rayDribble)
    if oppDef is not None:
        tm = free_teammate(state, rayPressing)
        if tm is not None and must_pass_ball(state, tm, distPasse, angleInter):
            return passBall(state, tm, maxPowerPasse, thetaPass, coeffPushUp)+pushUp(state, coeffPushUp)
        return dribble(state, oppDef, angleDribble, powerDribble, coeffAD)
    return control(state, powerControl)

def clearSolo(state):
    """
    Degage la balle avec une profondeur
    profondeurDegagement et une largeur
    largeurDegagement
    """
    return shoot(state, maxPlayerShoot)
    ecart_x = profondeurDegagement
    if not state.is_team_left(): ecart_x = -ecart_x
    x = state.my_pos.x + ecart_x
    ecart_y = largeurDegagement
    if not is_upside(state.my_pos,state.nearest_opp.position):  ecart_y = -ecart_y
    y = state.my_pos.y + ecart_y
    return kickAt(state,Vector2D(x,y), maxPlayerShoot)

def clear(state, profondeur, largeur, powerDegage=maxPlayerShoot):
    """
    Degage la balle vers son premier
    coequipier
    """
    tm = state.teammates[0]
    ecart_x = profondeur
    if not state.is_team_left(): ecart_x = -ecart_x
    ecart_y = largeur
    if tm.position.y < state.center_spot.y:  ecart_y = -ecart_y
    dec = Vector2D(ecart_x, ecart_y)
    return kickAt(state,dec + state.center_spot, powerDegage)

def shiftAside(state, decalX, decalY):
    """
    Se decale lateralement pour avoir
    une meilleure reception de la balle
    """
    deccalY = 20.
    opp = nearest_ball(state, state.opponents)
    ecart_y = decalY
    if is_upside(opp,state.center_spot):  ecart_y = -ecart_y
    ecart_x = decalX
    if state.is_team_left(): ecart_x = -ecart_x
    dec = Vector2D(ecart_x,ecart_y)
    return goTo(state, dec + state.center_spot)

def pushUp(state, coeffPushUp):
    """
    Monte dans le terrain pour proposer
    des possibilites de passe aux
    coequipiers
    TODO: Quid des nombres magiques ?
    """
    tm = state.teammates[0]
    dest = Vector2D()
    dest.x = tm.position.x + state.my_speed.x*coeffPushUp
    dest.y = tm.position.y + 30.
    if dest.y > 75.:
        dest.y = tm.position.y - 30.
    return goTo(state, dest)

def cutDownAngle(state, raySortie, rayInter):
    """
    Sort de la cage pour reduire
    l'angle de frappe a l'attaquant
    adverse
    """
    position = state.my_goal
    diff = state.ball_pos - position
    diff.norm = max(raySortie, diff.norm - rayInter)
    position += diff
    return goTo(state,position)

def cutDownAngle_gk(state, raySortie):
    """
    Sort de la cage pour reduire
    l'angle de frappe a l'attaquant
    adverse
    """
    position = state.my_goal
    diff = state.ball_pos - position
    diff.norm = raySortie
    position += diff
    return goTo(state,position)

def tryInterception(state, dico):
    """
    Essaye d'intercepter la balle
    s'il lui reste de temps,
    reinitialise son compteur et
    rest immobile sinon
    """
    if dico['n'] == -1:
        dico['n'] = dico['tempsI']
    dico['n'] -= 1
    if dico['n'] <= 0 :
        dico['n'] = dico['tempsI']
        return goToBall(state)
    return interceptBall(state, dico['n'])

def interceptBall(state,n):
    """
    Se deplace en vue d'intercepter
    la balle pour une estimation
    de n instants de temps
    """
    # n = 10
    v = state.my_speed
    r = state.my_pos
    vb = state.ball_speed
    rb = state.ball_pos
    fb = ballBrakeConstant
    fj = playerBrackConstant
    coeffb = coeff_friction(n,fb)
    coeffj = coeff_friction(n,fj)
    ax = fj*(rb.x-r.x + vb.x*coeffb-v.x*coeffj)/(n-coeffj)
    ay = fj*(rb.y-r.y + vb.y*coeffb-v.y*coeffj)/(n-coeffj)
    return goWith(Vector2D(ax,ay))
