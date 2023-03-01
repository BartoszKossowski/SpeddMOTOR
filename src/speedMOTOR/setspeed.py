"""
Prędkości obrotowe:
- RPM (obr/min)
- Hz
- m/s
- km/h
- mph

mila [m] = 1.609344 [km]

1 [km/h] = 0.28 [m/s]
10 [m/s] = 36 [km/h]

Wartości silnikowe

Obliczamy głównie:
- RPM
- Hz

Dodatkowo z dodatkowymi danymi:
- średnica wału (d):
 - prędkość (m/s i km/h i mph)

"""

import time
from datetime import datetime
from typing import Literal, get_args


class nfs:
    """
    nfs = https://pl.wikipedia.org/wiki/Need_for_Speed
    """
    _DURATION = Literal["infinity", "seconds", "minutes", "hours"]

    def __init__(self, value, RPM=None, Hz=None):

        self.duration = None
        self.set_time = None
        if isinstance(value, float):
            self.value = value
        else:
            if "," in str(value):
                value_comma = value.replace(',', '.')
                self.value = float(value_comma)
            else:
                self.value = float(value)

        if RPM:
            self.mode = "RPM"
        if Hz:
            self.mode = "Hz"

        if RPM is None and Hz is None:
            raise ValueError("You must select one of the units to be 'True' in the class arguments, example: Hz=True.")

    def show(self):
        print(f"Wartość: {self.value} | Jednostka: {self.mode}")

    def turnover(self, duration: _DURATION = "infinity", duration_time=None, _DURATION=_DURATION):
        """
        Przeliczamy wartość na ilość impulsów.

        Dodajemy tutaj również opcje: czas trwania [jako jednostka] oraz liczba

        Teraz tak:
            - przy RPM nie może być użyte 'seconds' mniejsze (<) 60, ;_;
            - minuty muszą być jako int,
            - godziny muszą być float,
        :return:
        """

        self.duration = duration
        exist_list = get_args(_DURATION)
        # sprawdzimy, czy zgadza się nam opcja w opcji | prosta asercja
        assert self.duration in exist_list, f"'{duration}' is not in {exist_list}"

        # ustalamy typy danych dla duration_time

        if self.mode == "RPM":
            """
            | RPM MAX 30 000 |
                No to mamy obroty na minutę.
                Trzeba ustalić ile to jest obrotów na sekundę.
                I ile trwa jeden impuls.
                
                RPS = obroty na sekundę.
                
                Jak mamy wszystko to teraz tak:
                    - wykonujemy impulsy dla jednej sekundy
                    - liczymy czas aktualny (sekundy, milisekundy)
                    - gdy minie sekunda, dodajemy do naszej zmiennej sekundowej
                    - wszystko będzie w pętli while, wyjściem będzie warunek: zmienna sekundowa == duration_time
            """

            RPS = float(self.value / 60)
            time_RPS = float(1/RPS)
            print(f"To jest ilość obrotów na sekundę: {RPS} | To jest czas jednego obrotu: {time_RPS}")

            if self.duration == "seconds":
                if duration_time < time_RPS:  # jeżeli czas trwania jest krótszy niż czas dla jednego obrotu
                    raise ValueError(f"The duration cannot be shorter than the duration of one spin | There is a duration: {duration_time} seconds for the time it takes to make one rotation: {time_RPS} seconds")
                self.set_time = duration_time

            if self.duration == "minutes":
                if isinstance(duration_time, float):
                    raise TypeError("For the duration in minutes, you need to specify a value as int()")
                self.set_time = duration_time * 60

            if self.duration == "hours":
                if isinstance(duration_time, float):
                    raise TypeError("For the duration in hours, you need to specify a value as int()")
                self.set_time = duration_time * 60 * 60

            if float(time_RPS) <= 1.0:

                """
                Trzeba napisać własny stoper
                Problem w tym, że wykorzystując biblioteki time i datetime liczą do 60 (dla sekund)
                """
                sekundy = 0  # tu liczymy ile sekund upłynęło
                actual_second = datetime.now().second  # czas startowy zostaje zwiększony razem z upływem current_second
                actual_microsecond = round(datetime.now().microsecond / 1000)  # startowy czas w milisekundach, będzie zwiększany wraz z różnicą current_microseconds
                time_RPS = time_RPS * 1000
                R = 0
                # print(f"Od tego zaczynamy: {actual_microsecond}")
                while True:
                    # aktualny czas
                    current_second = datetime.now().second
                    current_microseconds = round(datetime.now().microsecond / 1000)

                    # time.sleep(0.1)

                    # Czasem dochodzimy do prędkości około 30 tys. RPM, to nam daje 0,0002 sekundy na jeden obrót,
                    # trzeba zatem wykonać stoper dla milisekund (do trzech miejsc po przecinku),
                    # mikrosekundy podzielić przez 1000
                    # tysięczna sekundy jest całkiem stabilna, na niej będziemy opierać licznik
                    # print(f"To są nasze mikrosekundy przerobione na milisekundy: \n"
                    #       f"Dziesiętna sekundy: {round(current_microseconds / 100000)} \n"
                    #       f"Setna sekundy: {round(current_microseconds / 10000)} \n"
                    #       f"Tysięczna sekundy: {round(current_microseconds / 1000)}")

                    # licznik mikrosekund jest nam potrzebny do wydawania sygnałów w odpowiednim przedziale czasowym
                    # za dane wejściowe o tym, co ile ma zostać wykonany obrót daje nam: time_RPS
                    # dla przykładu z 600 RPM, jest to 10 obrotów na sekundę, czyli 1 obrót na 1 dziesiątą sekundy,
                    # żeby liczyć time_RPS pomnożymy go razy 1000 co da nam 0,1 * 1000 = 100
                    # w takim przypadku mamy obrót co 100 milisekund

                    # print(f"To jest current: {current_microseconds} | to jest actual: {actual_microsecond} | to jest time RPS: {time_RPS}")
                    if current_microseconds < 50 and current_microseconds < actual_microsecond:
                        while True:
                            current_microseconds = round(datetime.now().microsecond / 1000)
                            score = time_RPS - abs(actual_microsecond - 1000)
                            # print(f"To jest current: {current_microseconds} | A to jest różnica: {score}")
                            # print("asd")
                            if current_microseconds > score:
                                # print(f"Różnica: {score} | curent: {current_microseconds} | Aktualny: {actual_microsecond}")
                                actual_microsecond = current_microseconds
                                R += 1
                                # print(f"To jest current: {current_microseconds} | to jest actual: {actual_microsecond} | W zerowaniu")
                                break

                    # print(float(current_microseconds - actual_microsecond))
                    # print(time_RPS)
                    if float(current_microseconds - actual_microsecond) > time_RPS:
                        # print("Zwiększamy")
                        # print(90*"=")
                        actual_microsecond += time_RPS
                        R += 1
                        # print(f"To jest current: {current_microseconds} | to jest actual: {actual_microsecond} | zwykły przeskok 400")

                    """
                    Poniżej wykonany stoper dla sekund
                    """

                    # print(f"Aktualna sekunda: {current_second} | Goniąca sekunda: {actual_second} | Licznik sekund: {sekundy}")
                    # trzeba stworzyć licznik sekundowy
                    # i licznik podążający za aktualnym stanem sekundnika
                    if current_second > actual_second:
                        actual_second += 1
                        sekundy += 1  # to tutaj liczymy sekundy, które upłynęły (licznik nie resetuje się 60 - 0)
                    if current_second == 0 and current_second != actual_second:  # przy naszym opóźnieniu 0,1 sekundy 10 razy się dodaje więc trzeba było dać warunek logiczny
                        actual_second = 0
                        sekundy += 1  # to również jest interpretowane jako +1 sekunda

                    # to musi być na końcu
                    if duration_time == sekundy:  # gdy zadany czas pracy zostanie osiągnięty
                        print(f"Minęło {sekundy} sekund")
                        print(f"Wykonało się {R} obrotów")
                        break

            if float(time_RPS) > 1.0:
                # print("zaczynamy teraz co innego")
                pass


list = [60, 100, 150, 200, 400, 600, 1000, 1500, 2000, 5000, 8000, 10000]
for rpm in list:
    print(90 * "=")
    print(f"Powinno być: {(rpm/60) * 10}")
    a = nfs(value=rpm, RPM=True)
    for x in range(3):
        a.turnover("seconds", duration_time=10)

