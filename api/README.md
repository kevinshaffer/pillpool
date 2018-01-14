# Building the API for Dev Usage
1. copy `pillpool/config/config.default.json` to `pillpool/config/config.json`
    - Update credentials in new config file for your environment.
    - See [Database Tunneling](#database-tunneling) if you wish to work without IP whitelisting.
2. `$ docker-compose up`

# Building the API in Production Mode (Still for local usage.)
1. copy `pillpool/config/config.default.json` to `pillpool/config/config.json`
    - Update credentials in new config file for your environment.
    - See [Database Tunneling](#database-tunneling) if you wish to work without IP whitelisting.
2. `$ docker-compose -f docker-compose.prod.yml up`

# Database Tunneling:
1. Depending on your operating system and ssh method this may change:
    - OS X
        1.  Edit your `~/.ssh/config` file and add the following:
            - `IP-TO-TUNNEL-THROUGH`: is the IP address of the server you wish to tunnel through (this server must have access to the database in question)
            - `USERNAME-FOR-SERVER`: Username for the server from above
            - `TUNNEL-PORT-NUMBER`: Port you want to setup your tunnel under.
            - `DATABASE-URL`: URL of the database you wish to connect to
            - `DATABASE-PORT`: Port of the database to connect to (PostgreSQL: 5432, Redshift: 5439)
            ```
            Host db-tunnel
                Hostname <IP-TO-TUNNEL-THROUGH>
                User <USERNAME-FOR-SERVER>
                LocalForward <TUNNEL-PORT-NUMBER> <DATABASE-URL>:<DATABASE-PORT>
                GatewayPorts yes
            ```
        2. In Terminal, run:
            - `$ ssh -f -N db-tunnel`
    - Windows
        - If you are using putty follow these directions: https://www.akadia.com/services/ssh_putty.html

2. In `<pillpool API Repo Directory>/pillpool/config/config.json`, modify the "scada" block of the file as below. Replace `<LOCAL-MACHINE-IP>` with `docker.for.mac.localhost` or `docker.for.win.localhost` and `<TUNNEL-PORT-NUMBER>` with the same number you used in the ssh config file.
     ```
     "scada": {
            "username": "<DB-USERNAME>",
            "host": "<LOCAL-MACHINE-IP>",
            "password": "<SCADA-SERVER-PASSWORD>",
            "port": "<TUNNEL-PORT-NUMBER>",
            "database": "<DB-NAME>"
        }
     ```

## Other information unrelated to running this API, but instead how it was built
### Steps for locally creating a pyramid API from scratch:
1. `sudo pip3 install cookiecutter`
2. `cookiecutter gh:Pylons/pyramid-cookiecutter-starter`
    1. `pillpool`
    2. `pillpool`
    3. `jinja2`
3. `cd pillpool`
4. `python3 -m venv env`
5. `env/bin/pip install --upgrade pip setuptools`
6. `env/bin/pip install -e ".[testing]"`
7. `env/bin/pip install wsgicors`
8. `env/bin/pytest`
9. `env/bin/pserve development.ini`
