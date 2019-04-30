
all:
	if [[ ! -d ompc ]]; then hg clone https://bitbucket.org/vtad4f/ompc/ > /dev/null ; fi
	mkdir -p build ; cd build ; cmake .. > .log.txt ; make >> .log.txt
	cp build/src-graphmatch/*.dll src-main 2> /dev/null || true
	cp build/src-graphmatch/*.so  src-main 2> /dev/null || true
	cp build/src-gspan/*.dll      src-main 2> /dev/null || true
	cp build/src-gspan/*.so       src-main 2> /dev/null || true
	cd src-convert ; mkdir -p temp ; ./convert.sh > temp/.log.txt
	
clean:
	git clean -dfqX -- .