from .interpolator import Interpolator
from .Models.model import Model
from .Models.GradientFree.cobylaMod import Cobyla


class CobylaCreator(Interpolator):

    def createModel(self, data, config) -> Model:
        return Cobyla(data, config)
