#
# build and push docker container
#

# mvn macro - run mvn inside docker container
# to reduce local dependencies
mvn = docker run --rm -ti -v ${PWD}:/data -w /data \
	-v maven-repo:/root/.m2 \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v ${PWD}/.m2/settings.xml:/root/.m2/settings.xml:ro \
	maven:3.6.3-openjdk-14 mvn 

repo: 
	@docker volume create --name maven-repo >/dev/null

# compile java sources
compile: repo src
	@$(mvn) compile

# create executable jar
package: compile
	@$(mvn) package

# compile java app, build and push docker image
build: compile
	@$(mvn) jib:build

# run previously pushed docker image locally
start: stop
	@$(mvn) docker:start
stop:
	@$(mvn) docker:stop
logs:
	@$(mvn) docker:logs -Ddocker.follow 

clean: 
	@-docker volume rm maven-repo
	@$(mvn) clean