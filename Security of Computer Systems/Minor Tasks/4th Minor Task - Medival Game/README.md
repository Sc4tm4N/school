# 4th Minor Task - Medival Game

## Solution
ASLR was disabled, same canary. 
* get address of boss generator function
* prepare nickname as follows: suitable lenght of nickname where last signs are address of this functions
* when choosing character role pick '-1' -> it will read function address of our boss generator instead of typical heal / attack so we can become boss every round

