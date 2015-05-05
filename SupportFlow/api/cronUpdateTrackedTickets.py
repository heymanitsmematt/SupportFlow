from api.NetsuiteUpdate import MassNetsuiteGet

m = MassNetsuiteGet('all', True)
m.post()
m.save()
m.updateTrackedStatus()


