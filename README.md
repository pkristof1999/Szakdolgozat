<div>
    <h1>Futtatáshoz szükséges csomagok:</h1>
    <li>Python 3.11 és újabb verziók (régebbivel nincs tesztelve)</li>
    <li>pyqt6; pyqt6-tools; bcrypt; pyinstaller (opcionális)</li>
    <h3>Alkalmazás (.exe) létrehozása Windowshoz:</h3>
    <li>pyinstaller --add-data ".\src;src" --add-data ".\userdata;userdata" --add-data ".\Game.py;." --icon "icon.ico" --noconsole Game.py</li>
</div>
<br>
<hr>
<br>
<div>
    <h1><u>Munkaterv</u></h1>
</div>
<br>
<div>
    <p>Hallgató neve: <i>Pankotai Kristóf Géza</i></p>
    <p>Neptun kód: <i>JN8PXT</i></p>
    <p>Témavezető neve: <i>Dr. Szeghalmy Szilvia</i></p>
    <p>Szakdolgozati téma: <i>Játékos oktatóprogram fejlesztése</i><p>
    <p>Szakdolgozat címe: <i>Ismerkedjünk a számítástechnikában ránk leselkedő veszélyekkel!</i></p>
</div>
<br>
<div style="text-align: justify;">
    <h3>Téma általános leírása</h3>
    <p>Egy olyan oktatóprogram fejlesztése a cél, amely játékos eszközökkel világít rá az interneten 
    leskelődő veszélyekre, vírusokra és egyéb kártevőkre. A célközönség elsődlegesen az általános 
    iskolás gyerekek, azonban a játék olyan módon lesz kivitelezve, hogy bármilyen korosztály 
    számára élvezhető legyen. A játékosnak lehetősége lesz pontok és kitűzők gyűjtésére is. A 
    program három játékmódból épül fel: 
    A fő játékmód megismerteti a felhasználót a kártevőtípusokkal. A program a figyelem 
    fenntartásának érdekében interaktív kérdéseket tesz fel (adott esetben a játékos szerint mi lenne 
    a legjobb megoldás a károk elkerülésére) az oktató anyag feldolgozása közben, ahol a jó 
    válaszokért pont szerezhető. Ha minden kérdésre jól válaszolunk, akkor egy különleges 
    kitűzőben részesülünk. 
    A második játékmód a fő játékmódban szerzett ismeretekre alapozva egy kvízjáték, ahol egy 
    adatbázisból véletlenszerű módon kapja a játékos a kérdéseket. Jó válaszra pont szerezhető, és 
    ha egy körben az összes kérdésre jó választ adunk, akkor egy kitűző a jutalom. 
    A harmadik játékmód egy E-mail megbízhatósági tesztjáték. A játékos kap egy véletlenszerű 
    e-mailt egy adatbázisból, majd eldöntheti, hogy szerinte megbízható-e. Az e-mail tartalmazhat 
    káros reklámokat és veszélyes hivatkozásokat, amelyekre rákattintva pont veszíthető. Sok 
    hibázás esetén a játékos kap egy „figyelmetlen” kitűzőt. 
    A játékban külön felületen van lehetősége a játékosnak megtekinteni az elért kitűzőit és 
    eredményeit, utóbbit alaphelyzetbe állítani, felhasználónevet váltani, profilképet feltölteni, 
    illetve megadott megjelenítési témák közül választani.</p>
</div>
<br>
<div>
    <h3>Elvégzendő munka</h3>
    <p>A terveim a szerint a programot Python3 nyelven valósítom meg, a kérdésbankhoz, illetve a 
    felhasználói adatok tárolásához pedig JSON fájlt fogok készíteni. A felhasználói felületeket 
    PyQt6 segítségével állítom majd össze, melyeket a szakirodalom, illetve hasonló munkák 
    áttekintése után tervezek meg. A megjelenítési témák közül egy-egy kimondottan a gyerekek, 
    illetve az idősebb korosztály számára készül. A szükséges grafikai elemeket GIMP segítségével 
    hozom majd létre. A tervezés után összegyűjtöm, hogy a különböző játékmódok – ügyelve a 
    játékos életkorához – milyen tartalommal, kérdésekkel rendelkezzenek. Ha minden 
    előkészületet elvégeztem, elkezdem a program fejlesztését, illetve a fejlesztés végeztével a 
    tesztelését. Ha sikeresen elkészült a program, akkor megírom hozzá a dolgozatom.</p>
</div>
<br>
<div>
    <h3>A téma relevanciája</h3>
    <p>Napjainkban az internetet szinte minden korosztály napi rendszerességgel használja, azonban 
    bárki könnyen belefuthat gyanútlanul egy átverésbe, vagy internetes kártevőbe. Az oktató 
    program célja az, hogy megtanítsa a felhasználókat az efféle veszélyek felismerésére, hogy 
    kisebb valószínűséggel váljanak áldozattá.</p>
</div>
<br>
<hr>