import numpy as np
import numpy.random as rd

#Liste erstellen, in der die Wörter aus der txt Datei eingefügt werden
wordList = []
tempWordList = [] # wird benötigt um ein Wiederholen der Wörter zu verhindern

#Wörter werden aus der txt Datei ausgelesen und in die liste übergeben
readTxt = open("hangman.txt")
for x in readTxt:
    wordList.append(x.replace("\n",""))
readTxt.close()

# übergibt die Wörter aus der txt datei, in eine neue txt-Datei, die während dem Spiel bearbeitet wird,
# um eine Speicherung der Veränderung während des spielens zu gewährleisten
writeTxt = open("temphangman.txt", "w")
for x in wordList:
    writeTxt.write(f"{x}\n")
writeTxt.close()
readTxt = open("temphangman.txt")
for x in readTxt:
    tempWordList.append(x.replace("\n",""))
readTxt.close()


# Funktion zum Wiederholen des Spiels nach beendigung
def wordGameRepeat():
    while True:
        again = input("Möchtest du nochmal Spielen? (Ja/Nein)")
        again = again.upper()
        if again == "JA":
            print("Alles klar :)")
            # erzeugt leere Zeilen beim Neustarten des Spiels um ggf. das vorangehende Spiel in der Konsole vom neuen zu trennen
            for x in range(20):
                print("\n")
            break
        elif again == "NEIN":
            print("Ciao")
            return "No"
        else:
            print("bitte Ja oder Nein eingeben")



# Schleife die das gesamte Spiel wiederholt
while True:

    # initialisieren des Spiels Auswählen des Worts und Erstellen der nötigen Variablen
    # um ein Spielen ohne Wiederholten wörtern zu gewährleisten wird die temporäre txt Datei in jeder Runde abgeändert,
    # sodass nur nicht verwendete Wörter gespielt werden
    try:
        # txt datei wird gelesen und in liste übernommen
        readTxt = open("temphangman.txt")
        for x in readTxt:
            np.append(tempWordList, (x).replace("\n", ""))
        readTxt.close()
        # Wort fürs Spiel wird ausgewählt
        gameWord = rd.choice(tempWordList, replace=False)
        # Wort wird für die zukünftigen Spiele entfernt
        tempWordList = np.setdiff1d(tempWordList, gameWord)
        writeTxt = open("temphangman.txt", "w")
        for x in tempWordList:
            writeTxt.write(f"{x}\n")
        writeTxt.close()
        gameWord = gameWord.upper()
    # falls die liste Leer ist, weißt das spiel darauf hin
    except ValueError:
        print("Es gibt keine neuen Wörter mehr. Du kannst mit den alten aber nochmal spielen")
        if wordGameRepeat() == "No":
            break
        else:
            readTxt = open("hangman.txt")
            for x in readTxt:
                np.append(tempWordList, (x).replace("\n", ""))
            readTxt.close()
    gameWordSplit = [*gameWord]
    gameWordShown = list(())
    lettersGuessed = list(())

    # füllt das Wort mit den vorerst leeren Feldern in Form von _
    for x in gameWordSplit:
        gameWordShown.append("_")

    # gibt das noch Leere Wort aus
    print("ich denke an folgendes Wort."\
          "\nAchtung: Ä,Ö und Ü sind im Wort AE, OE und UE")
    for x in gameWordShown:
        print(x, end=" ")
    print("")

    # Counter der die möglichen Fehler zählt
    counter = 10

    # Schleife um die Spielrunden zu erzeugen
    while True:

        # überprüfung ob ggf. bereits Gewonnen wurde
        if "_" in gameWordShown:

            # Abfrage des Buchstaben
            guessLetter = input("rate welcher Buchstabe im Wort ist.\n")
            guessLetterUp = guessLetter.upper() # buchstabe wird zur einfacheren Handhabung zu einem Großbuchstaben gemacht

            # Prüfung ob ein Buchstabe eingegeben wurde
            if len(guessLetter) > 1 or len(guessLetter) == 0 or guessLetter.isalpha() == False:
                print("bitte gib einen Buchstaben ein")

            # Prüfung ob der eingegebene Buchstabe bereits in vorheriger Runde gewählt wurde
            elif guessLetterUp in lettersGuessed:
                print("Du hast diesen Buchstaben schon geraten.\
                 \nHier sind das bisher gelöste Wort und die bereits geratenen Buchstaben")
                for x in gameWordShown:
                    print(x, end = "")
                print("")
                for x in lettersGuessed:
                    print(f"{x}, ", end="")
                print("")

            # Nach Durchlaufen der Prüfung der Eingabe wird hier das Spiel ausgeführt
            else:
                # Der Buchstabe wird zu den bisher geratenen Hinzugefügt
                lettersGuessed.append(guessLetterUp)
                lettersGuessed.sort()

                # Prüfung ob Buchstabe korrekt
                if guessLetterUp in gameWord:
                    # korrekter Buchstabe wird in die entsprechenden Lücken eingefüllt
                    tempList = np.array(gameWordSplit)
                    gameWordIndex = np.where(tempList == guessLetterUp)[0]
                    for x in gameWordIndex:
                        gameWordShown[x] = guessLetterUp
                    for x in gameWordShown:
                        print(x, end=" ")
                    print("")
                else:

                    # falscher Buchstabe verringert den Counter der weiters bekanntgegeben wird
                    counter -= 1
                    if counter > 1:
                        print(f"Leider nicht dabei, du hast noch {counter} Versuche")
                    elif counter == 1:
                        print(f"Leider nicht dabei. "
                              f"\nAchtung: du hast nur noch einen Versuch!")
                    else:
                        print("Du hast Verloren :(")
                        break

        #Auflösung der ersten Überprüfung, falls Gewinn festgestellt wird
        else:
            print("Du hast Gewonnen!")
            break

    # Abfrage zum nochmal spielen, hierzu wird Funktion verwendet
    if wordGameRepeat() == "No":
        writeTxt = open("temphangman.txt", "w")
        writeTxt.write("")
        writeTxt.close()
        break

print("lass uns spielen!")








