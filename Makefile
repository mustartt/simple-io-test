# Makefile for compiling project files
# place the Makefile and io-test.py in the individual question directory
# (make run) to run the built binary

# Compiler Configs
CC := clang
CFLAGS := -g -Wall -I../common/ -Wno-unused-command-line-argument -fsanitize=address

# CS136 LLVM LL stuff
LOCAL_LL := $(shell find ./*.ll)
LOCAL_OBJS := $(patsubst %.ll,%.o,$(LOCAL_LL))

COMMON_LL := $(shell find ../common/*.ll)
COMMON_OBJS := $(patsubst ../common/%.ll,%.o,$(COMMON_LL))

# Source files
OUTPUT := main
SRCS := $(shell find ./*.c)
OBJS := $(patsubst %.c,%.o,$(SRCS))

.PHONY: clean make-test test run

all: $(OUTPUT)

run: $(OUTPUT)
	./$(OUTPUT)

# Run IO Test
test: $(OUTPUT)
	python3 io-test.py

# Compile the object files 
$(OUTPUT): $(COMMON_OBJS) $(LOCAL_OBJS) $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

$(OBJS): $(SRCS)
	$(CC) $(CFLAGS) -c $^

$(COMMON_OBJS): $(COMMON_LL)
	$(CC) $(CFLAGS) -Wno-override-module -c $^

$(LOCAL_OBJS): $(LOCAL_LL)
	$(CC) $(CFLAGS) -Wno-override-module -c $^

# cleans up the object files
clean:
	rm -f *.o $(OUTPUT)

make-test:
	$(info ${SRCS})
	$(info ${OBJS})