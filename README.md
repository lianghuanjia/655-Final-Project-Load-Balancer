1. Set up a geni node using rspec
https://github.com/lianghuanjia/655-Final-Project-Load-Balancer/blob/main/Middle%20Server%20Rspec

2. Login to the geni node

3.Copy the bash script in the following file
https://github.com/lianghuanjia/655-Final-Project-Load-Balancer/blob/main/Middle%20Server%20Bash

4.change the bash script file's permission:
chmod +x [bash file you created and put the bash script inside]

5. open the load_balance.py:
vim load_balance.py

6. In the main function, go to the following line: 
server = WebsocketServer(host='192.41.233.54', port=12345), 
change the host into the public IP of the machine the code runs on

7. Run the code:
python3 load_balance.py
