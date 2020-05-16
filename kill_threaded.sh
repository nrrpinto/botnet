#!/bin/bash

kill -9 $(ps aux | grep threaded.py | awk '{print $2}' | head -n1)
