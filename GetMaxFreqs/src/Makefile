all:
	(cd build.linux; cmake ..; make)
	(cd build.windows; /opt/mxe/usr/bin/i686-w64-mingw32.static-cmake ..; make)

clean:
	rm -rf build.linux build.windows ../bin
	mkdir build.linux build.windows ../bin
