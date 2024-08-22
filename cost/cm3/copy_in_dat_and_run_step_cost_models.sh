#!/bin/bash

cp /home/jg6173/easyVVUQ-process/cost/cm3/sol_IN.DAT .

step_cost_models -i sol_IN.DAT -c cost_conf.toml
