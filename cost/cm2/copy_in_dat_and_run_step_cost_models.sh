#!/bin/bash

cp /home/jg6173/easyVVUQ-process/cost/cm2/sol_IN.DAT .

step_cost_models -i sol_IN.DAT -c cost_conf.toml -s process_internal_solvers.legacy_vmcon
