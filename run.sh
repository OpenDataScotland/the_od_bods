#!/bin/bash

exec python ./main.py &
exec python ./merge_data.py &
exec python ./export2jkan.py