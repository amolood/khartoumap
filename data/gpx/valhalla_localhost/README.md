# Running Valhalla using Docker Compose

This is a far more efficient alternative to building a Valhalla server using cmake.

## Steps:
- Create a new folder. This will also host the custom tiles.
- Create a <docker-compose.yml> file (attached).
	* The file gets the latest Valhalla image and defines geography boundaries.
	* You should also specify the port for localhost. Currently set to <http://localhost:8002>
- Run <docker-compose up -d> to run a container in the background.
	* You might need to login to Docker Hub using <docker login>.
- Run <docker ps -a> to ensure the container is running.
	* Run <docker logs [containerID]> to view download and tile building process. 
	* The time this will take depends on the size and complexity of the ROI defined in the compose file. All tiles and graphs must be built first before being able to run any processes.
	* The log will contain the message **INFO: Found config file. Starting valhalla service!** which may be followed by some additional warning and info logs.
- Once done, you should be able route Valhalla requests via the localhost.
- Run <docker-compose down> to close the localhost after finishing.
	
## Test: 
curl http://localhost:8002/route --data '{"locations":[{"lat":15.683362,"lon":32.462027},{"lat":15.544130,"lon":32.581544}],"costing":"auto","directions_options":{"units":"kilometers"}}' | jq '.'

### Documentation <https://valhalla.github.io/valhalla/api/>