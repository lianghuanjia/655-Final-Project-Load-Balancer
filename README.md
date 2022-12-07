1. Set up a geni node using rspec or create a node in GENI on your own. Remember to give the node a public IP to route to.
https://github.com/lianghuanjia/655-Final-Project-Load-Balancer/blob/main/Middle%20Server%20Rspec

2. Login to the geni node

3. Create a bash file and copy the script in the following bash file into the bash file you just created
https://github.com/lianghuanjia/655-Final-Project-Load-Balancer/blob/main/Middle%20Server%20Bash

4. Change the bash script file's permission:
chmod +x [bash file you created and put the bash script inside]

5. Run the bash file you just created and copied the code into:
./[bash fiel you created]

6. go into the file you just git clone:
cd 655-Final-Project-Load-Balancer/

7. open the load_balance.py:
vim load_balance.py

8. In the main function, go to the following line: 
server = WebsocketServer(host='192.41.233.54', port=12345), 
change the host into the public IP of the machine the code is running on

9. Run the code:
python3 load_balance.py
