# Crypto (Franklin-Reiter Related Message Attack) - 2nd Major Task
There is only filtered version of network logs, because original was quite big. 

## Content (in Polish):
W ostatnich dniach branżowe serwisy obiegła informacja (pisali o niej m.in. Securium i Seqrak) o odkryciu nowej, niezwykle groźnej, odmiany oprogramowania szantażującego (ang. ransomware), którą ogłoszono następcą słynnego WannaCry. Również i tym razem trojan zaatakował komputery wielu instytucji, nie oszczędzając danych najbardziej wpływowych osób w państwie. Zaszyfrowaniu uległy poufne rządowe dokumenty. Z wypowiedzi różnych ekspertów wynika, że ofiarom cyberataku może nie pozostawać nic innego jak tylko zapłata okupu. Czy ugną się pod szantażem?

Jesteś ostatnią instancją, która może pomóc odzyskać dane z komputera pewnej Bardzo Ważnej Osoby (BWO). Służby przekazały Ci spakowany obraz katalogu domowego BWO zawierający zaszyfrowane pliki. Wprawdzie Twoje szanse w starciu z szyfrem AES nie są oceniane wysoko, jednak na wszelki wypadek otrzymałeś stosowny certyfikat dostępu do poufnych danych. Administratorzy, którzy monitorują na bieżąco infrastrukturę sieciową, zabezpieczyli zapis wychodzącego i przychodzącego ruchu sieciowego do komputera BWO z okresu, gdy prawdopodobnie nastąpiło zakażenie komputera złośliwym oprogramowaniem.

Pliki muszą zostać odszyfrowane najdalej do dn. 10.01.2018 do godz. 23.59, inaczej dane zostaną bezpowrotnie utracone. O ewentualnym sukcesie kryptoanalizy WannaCry+ należy niezwłocznie poinformować przedstawicieli odpowiednich służb prowadzącego laboratorium (który posiada również wszystkie wymagane certyfikaty bezpieczeństwa) i załączyć dowód rozwiązania (opis metody, skrypt). Odszyfrowanych plików nie wolno ujawniać pod rygorem odpowiedzialności karnej.

Przy rozwiązywaniu zadania przydatne mogą okazać się:
* biblioteka PyCrypto (pip install pycrypto)
* Wireshark

## Sequrak content:

    Вы помните червь WannaCry? Эта программа-вымогатель инфицировала более 500 тысячи компьютеров в начале этого года. Теперь червь вернулся и он еще более опасен. Он уже напал на правительственные компьютеры в нескольких странах.
    
    Мы первыми представим анализ деятельности нового сорта вирусa-шифровальщикa WannaCry+.
    
    WannaCry+ начинает сканировать систему в поисках пользовательских мультимедиальных файлов определённых типов таких, как .docx или .jpg. Для каждого такого файла программа генерирует уникальный 256-битный ключ симметричного алгоритма AES который работает в режиме счетчика. Пре-мастер секрет, из которого выведен ключ AES, шифруется открытым ключом RSA злоумышленника и отправляется к него на сервер. Мы обнаружили, что WannaCry+ использует 2048-битный открытый модуль RSA. Вы можете скачать этот ключ здесь.
    
    Каждый зашифрованный файл получает расширение .шиф и исходный файл удаляется. Для каждого зашифрованного файла червь оставляет файлы .README.txt со следующим содержимым:
    
    Ваши файлы были зашифрованы.
    Чтобы расшифровать один файл, Вам необходимо отправить **1.337 ETH**
    на Етхереум адрес:
    0xC840E516167988D39FBcfF67e4E28738523eC9E3
    В поле data сделку введите Ваш адрес электронной почты
    и следующий дайджест Вашего файла
    89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb
    Далее на этот адрес вы получите ключ дешифратор и все необходимые инструкции.
    
    Он требует выкупа в размере 1.337 ETH=57549 рублей (Эфириум это популярная криптовалюта) для каждого файла на адрес 0xC840E516167988D39FBcfF67e4E28738523eC9E3. В транзакции должен быть указан идентификатор (в приведенном выше примере этот идентификатор равен 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb). Наши результаты показывают, что этот идентификатор является дайджестом (SHA-256) зашифрованного ключом RSA пре-мастер секрета.
    
    Наши специалисты провели обратной разработки кода червя и восстановили его в виде скрипта на Python 2. Cкрипт верно воспроизводит исходный алгоритм червя. Если вы запустите его без аргументов, скрипт будет шифровать мультимедийные файлы в текущем дереве каталогов. Добавление опции -d переключит скрипт в режим дешифрования. Например, если вы запустите:
    
    python wannacry.py -d 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb hkMay1CSgiYgbLwrV2JrojIK9ZnbAXFT09cXNjNxOmc=
    где 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb — дайджест, упомянутый в файле .README.txt, и hkMay1CSgiYgbLwrV2JrojIK9ZnbAXFT09cXNjNxOmc= — это ключ, полученный после оплаты выкупа, вы должны получить сообщение для дешифрования файла.

## Sequrak content (in English):

    Do you remember the WannaCry worm ? This program-extortionist infected more than 500 thousand computers at the beginning of this year. Now the worm has returned and it is even more dangerous. He has already attacked government computers in several countries.
    
    We are the first to present an analysis of the activity of a new virus-encryptor, WannaCry +.
    
    WannaCry + starts scanning the system in search of custom multimedia files of certain types such as .docx or .jpg. For each such file, the program generates a unique 256-bit key of the symmetric AES algorithm that works in the counter mode . The pre-master secret from which the AES key is derived is encrypted with an open key of the attacker's RSA and sent to it on the server. We found that WannaCry + uses a 2048-bit open RSA module. You can download this key here .
    
    Each encrypted file receives an .shf extension and the original file is deleted. For each encrypted file, the worm leaves .README.txt files with the following contents:
    
    Your files have been encrypted. 
    To decrypt one file, you need to send ** 1.337 ETH ** 
    to the address: 
    0xC840E516167988D39FBcfF67e4E28738523eC9E3 
    In the data transaction field enter your e-mail address 
    and the following digest of your file: 
    89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb 
    Further to this address you will receive the key decoder and all the necessary instructions.
    
    It requires a ransom of 1.337 ETH = 57549 rubles ( Efirium is a popular crypto currency) for each file at the address 0xC840E516167988D39FBcfF67e4E28738523eC9E3. The transaction must have an identifier (in the example above, this identifier is 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb). Our results show that this identifier is a digest ( SHA-256 ) of an RSA-encrypted pre-master secret.
    
    Our specialists conducted the reverse development of the worm's code and restored it in the form of a script in Python 2 . The script faithfully reproduces the original algorithm of the worm. If you run it without arguments, the script will encrypt the media files in the current directory tree. Adding the -d option switches the script to decryption mode. For example, if you run:
    
    python wannacry . py - d 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb hkMay1CSgiYgbLwrV2JrojIK9ZnbAXFT09cXNjNxOmc =
    where 89ae1c813fbfeac8334259dc913e2909d06be552d2abcf0826f7ae83ef67abfb - the digest mentioned in the file .README.txt, and hkMay1CSgiYgbLwrV2JrojIK9ZnbAXFT09cXNjNxOmc = is the key obtained after the payment of the repurchase, you should receive a message for decrypting the file.
