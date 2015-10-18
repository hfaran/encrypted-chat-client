import chatclient
import os


Alice = chatclient.ChatClientClient("0.0.0.0", 8051)
raw_input()
Alice.set_shared_key('12345678901234567890123456789012')
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()
Alice.mutauth_step()
raw_input()

