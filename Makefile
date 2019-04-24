
all:
	mkdir -p build
	cd build ; cmake .. ; make
	cd src-convert ; ./convert.sh
   
clean:
	git clean -dfqX -- .