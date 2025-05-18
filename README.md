# HSL-departure

Get information about the next rides departing from a specified HSL stop using the command line.

Results inclure transportation line, headsign, minutes until departure, departure time, prediction type, and possible alerts on the route.

## Usage

1. Clone the repository.

        git clone https://github.com/lassihi/HSL-departure.git

2. Get your digitransit API key from https://portal-api.digitransit.fi and add it to line 1 of HSL.py.

3. Install Python Requests module, https://requests.readthedocs.io/en/latest/.

4. Run the script.
   
        python3 HSL.py <stop_id> <number_of_departures>

   Easiest way to find the stop id is navigating to the stop in hsl.fi, and looking at the last part of the URL. It should look something like `HSL%3A1020454`. `%3A` decoded is `:`.

   <img width="707" alt="Näyttökuva 2025-05-18 kello 23 33 49" src="https://github.com/user-attachments/assets/67ad58bb-551c-45d9-80d5-2bbc0d14fc46" />

6. Make it a command. (optional)

   <img width="707" alt="Näyttökuva 2025-05-18 kello 23 32 56" src="https://github.com/user-attachments/assets/271da052-b136-43af-a0db-7ea611704506" />

   I used a bash script that activates virtual environment, runs the python script, and deactivates virtual environment. Lastly I added the bash script to `/usr/local/bin/`.
