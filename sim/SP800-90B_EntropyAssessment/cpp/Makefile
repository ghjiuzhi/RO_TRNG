ARCH ?= x86
CXX ?= $(CROSS_COMPILE)g++

CXXFLAGS = -std=c++11 -fopenmp -O2 -ffloat-store
ifeq ($(ARCH),x86)
CXXFLAGS += -march=native
endif

LIBS = -lbz2 -lpthread -ldivsufsort -ldivsufsort64
COND_LIBS = -lmpfr -lgmp
SHARED_LIBS = -ljsoncpp -lcrypto

INC = -I/usr/include/  # 这里设置正确include路径
LDFLAGS = $(LIBS) $(SHARED_LIBS)

# 目标文件
OBJECTS = iid_main.o non_iid_main.o restart_main.o conditioning_main.o transpose_main.o

all: ea_iid ea_non_iid ea_restart ea_conditioning ea_transpose

ea_iid: iid_main.o
	$(CXX) $^ -o $@ $(LDFLAGS)

ea_non_iid: non_iid_main.o
	$(CXX) $^ -o $@ $(LDFLAGS)

ea_restart: restart_main.o
	$(CXX) $^ -o $@ $(LDFLAGS)

ea_conditioning: conditioning_main.o
	$(CXX) $^ -o $@ $(LIBS) $(COND_LIBS) $(SHARED_LIBS)

ea_transpose: transpose_main.o
	$(CXX) $^ -o $@ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INC) -c $< -o $@

clean:
	rm -f *.o ea_iid ea_non_iid ea_restart ea_conditioning ea_transpose selftest/*.res
