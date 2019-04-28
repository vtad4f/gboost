
all:
	mkdir -p build ; cd build ; cmake .. > .log.txt ; make >> .log.txt
	cd src-convert ; mkdir -p temp ; ./convert.sh > temp/.log.txt
   
clean:
	git clean -dfqX -- .