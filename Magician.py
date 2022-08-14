class Magician:
    def __init__(self, iz):
        self.iswitch = iz
        self.wasVaccinated = False
        self.turnsVaccinated = 0
        self.isVaccinated = False
        self.halfCured = False
        self.wasCured = False
        self.isStunned = False

    def clone(self):
        ret = Magician(self.iswitch)
        ret.wasVaccinated = self.wasVaccinated
        ret.turnsVaccinated = self.turnsVaccinated
        ret.isVaccinated = self.isVaccinated
        ret.halfCured = self.halfCured
        ret.wasCured = self.wasCured
        ret.isStunned = self.isStunned
        return ret