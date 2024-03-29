import cherrypy
import sys
import time
import utilsQuixo
class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        body = cherrypy.request.json
        ACTIONS = self.Action(body,body["game"],body["you"],body["players"],body["moves"])
        return ACTIONS
    def Action(self,body,game,you,players,moves):
        direction = ""
        Myself = 0
        ennemyName = ""
        if players[0] == you:
            Myself = 0
            ennemyName = players[1]
        else:
            Myself = 1
            ennemyName = players[0]
        myButtonList = self.convertListButtons(game,Myself)
        iaCmd = utilsQuixo.startIA(myButtonList)
        if iaCmd[1] == True and iaCmd[2] == True:
            direction = "E"
        elif iaCmd[1] == True and iaCmd[2] == False:
            direction = "W"
        elif iaCmd[1] == False and iaCmd[2] == True:
            direction = "S"
        elif iaCmd[1] == False and iaCmd[2] == False:
            direction = "N"
        return {"move" : {"cube" : int(iaCmd[3]), "direction" : str(direction)} , "message": self.returnMessage(ennemyName,iaCmd[0])}
    def convertListButtons(self,moves,myself):
        listbutton = []
        for i in range(25):
            if moves[i] == None:
                btn = Button()
                btn.background_normal = "case2.png"
                btn.background_down = "case2.png"
                btn.guid = str(i)
                listbutton.append(btn)
            elif moves[i] == myself:
                btn = Button()
                btn.background_normal = "casevide2.png"
                btn.background_down = "casevide2.png"
                btn.guid = str(i)
                listbutton.append(btn)
            else:
                btn = Button()
                btn.background_normal = "casevide.png"
                btn.background_down = "casevide.png"
                btn.guid = str(i)
                listbutton.append(btn)
        return listbutton
    beforeWeight = 0
    def returnMessage(self,ennemy,weight):
        if self.beforeWeight == 0: # on debute la partie
            self.beforeWeight = weight
            return "Debut de la partie, bonjour " + str(ennemy)
        elif weight == 1000000000: # on a gagné
            self.beforeWeight = weight
            return "Woow on a gagne la partie (ﾉ◕ヮ◕)ﾉ" 
        elif weight == -1000000000: # on a perdu
            self.beforeWeight = weight
            return "Bon bah on a perdu :("
        elif self.beforeWeight > weight: # on est en position de faiblesse
            self.beforeWeight = weight
            return "Bien joué, " + str(ennemy) + " ლ(ಠ_ಠლ)"
        elif self.beforeWeight < weight: # on est en position de force
            self.beforeWeight = weight
            return "KABOOM on te dégomme " + str(ennemy) + " (ง •̀_•́)ง"
class Button:
    background_normal = ""
    background_down = ""
    guid = ""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())