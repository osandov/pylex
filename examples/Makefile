ALL_CFLAGS := -Wall -g $(CFLAGS)
BUILD ?= build

dir_guard = @mkdir -p $(@D)

$(BUILD)/cpylex: $(BUILD)/cpylex.o $(BUILD)/pylex.o
	$(dir_guard)
	$(CC) $(ALL_CFLAGS) -o $@ $^

$(BUILD)/%.o: %.c
	$(dir_guard)
	$(CC) $(ALL_CFLAGS) -o $@ -c $<

pylex.c:
	$(error "Generate pylex.c with pylex.py")

clean:
	rm -rf $(BUILD)

.PHONY: clean
