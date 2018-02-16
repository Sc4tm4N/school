# Web Security - 3rd Major Task

Site was a django app, most security systems were turned on. The bug was simply by design. Messages was purely inserted from db and it was possible to run custom script if you uploaded avatar .png and then used it as .js. 
Steps:
* write .js with code you want to execute
* change it's name to .png
* upload it as your avatar
* send message to someone containg: <script src="<link to your avatar>"></script>
* wait for flague


## Content (in Polish):

    W tym zadaniu znowu chcemy zdobyć flagę. Tym razem jednak celem naszego ataku nie jest serwer - flagę zna tylko tajemniczy użytkownik o pseudonimie "admin". Ponieważ admin bardzo ceni sobie bezpieczeństwo, jedyną metodą komunikacji elektronicznej jakiej używa jest Bezpieczny System Komunikacji (https://h4x.0x04.net/).
    
    Zadanie nie wygląda na trudne - wystarczy poprosić admina o flagę: https://www.youtube.com/watch?v=QZIOe0o--jc . Niestety okazuje się, że admin nie rozmawia z nieznajomymi...
    
    Rozwiązania zadań (wysłane wiadomości, użyte skrypty, itp) należy wysłać prowadzącemu grupę laboratoryjną drogą mailową lub zaprezentować na zajęciach w terminie do dn. 31.01.2018 (godz. 23:59).
    
    W razie problemów z działaniem serwera (lub symulowanych użytkowników serwisu) prosimy o kontakt na adres mwk (at) mimuw.edu.pl.
