import pandas as pd
from dataclasses import dataclass
from sympy import isprime


@dataclass(frozen=True, init=False)
class valReader():
    '''
    Provvede alla lettura e gestione di osservazioni effettuate sui k satelliti
    Le istanze di questa classe sono immutabili.
    Un valReader è rappresentato da k osservazioni. Una osservazione è
    '''

    values_file: str
    values: pd.core.frame.DataFrame

    def __init__(self, fileName: str):
        """
        Overview
        ------------
        Costruisce un'istanza della classe a partire dal fileName passato per
        parametro. fileName corrisponde al nome del file dove sono contenuti le
        osservazioni.

        Params
        ------------
            fileName (str): nome del file dove sono contenuti le osservazioni.


        """
        object.__setattr__(self, "values_file", fileName)
        with open(self.values_file, "r") as val:
            object.__setattr__(self, "values", pd.read_csv(val))

    def getNumValues(self) -> int:
        """
        Restituisce il numero di osservazioni raccolte.

        Returns
        --------------
            int - numero di osservazioni raccolte.
        """

        return len(self.values.index)

    def getNumSat(self) -> int:
        """
        Overview
        -------------------
        Restituisce il numero di satelliti osservati

        Returns
        -------------------
         int - numero di satelliti osservati

        """
        return int(len(self.values.columns) / 2)

    def getNthValue(self, n: int) -> pd.core.frame.DataFrame:
        """
        Overview
        -------------------
        Restituisce le osservazioni n-esime dei k satelliti.
        n deve essere compreso tra 0 e il numero di osservazioni raccolte.

        Params
        -------------------
        n (int) - Indice della osservazione da recuperare.

        Raises
        -------------------
        Exception - se n non è compreso tra 0 e il numero di osservazioni
                    raccolte.

        Returns
        -------------------
        pd.core.frame.DataFrame - Contiene i valori della n-esima osservazione

        """
        return pd.DataFrame(self.values.loc[n])

    def getRangeValues(self, start: int, end: int) -> pd.core.frame.DataFrame:
        """
        Overview
        -------------------
        Restituisce le osservazioni dall'indice start a end (escluso)
        start deve essere minore o uguale di end e sia start che end devono
        essere compresi tra 0 e il numero di osservazioni effettuate.

        Params
        -------------------
        start (int) - Indice di partenza della prima osservazione da recuperare
        end (int) - Indice della prima osservazione da escludere.

        Raises
        -------------------
        Exception - se non sono rispettate le precondizioni.

        Returns
        -------------------
        pd.core.frame.DataFrame - le osservazioni richieste.

        """
        return self.values.iloc[start:end]

    def translateSat(index: int) -> tuple:
        return (f"x{index}", f"y{index}")

    def getSatValues(self, dataframe: pd.core.frame.DataFrame,
                     index: int) -> pd.core.frame.DataFrame:
        return dataframe[[self.translateSat(index)[0],
                          self.translateSat(index)[1]]]

    def leafSize(n: int) -> int:
        if isprime(n):
            n -= 1
        max = 0
        for i in range(1, int(n) // 2 + 1):
            if n % i == 0 and max < i:
                max = i
        return max


if __name__ == '__main__':
    read = valReader("values.csv")
    print(f"numero di satelliti: {read.getNumSat()}")
    print(f"numero di osservazioni: {read.getNumValues()}")
    print(read.getNthValue(2))
    print(len(read.getNthValue(2).index))
    print(read.translateSat(0))
    print(read.getSatValues(read.getRangeValues(2, 4), 0))
