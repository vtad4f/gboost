
all:
	if [[ ! -d ompc ]]; then hg clone https://bitbucket.org/vtad4f/ompc/ > /dev/null ; fi
	mkdir -p build ; cd build ; cmake .. > .log.txt ; make >> .log.txt
	cd src-convert ; mkdir -p temp ; ./convert.sh > temp/.log.txt
	
clean:
	git clean -dfqX -- .