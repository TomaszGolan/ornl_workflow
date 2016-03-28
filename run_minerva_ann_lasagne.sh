#!/bin/bash

NEPOCHS=1
LRATE=0.0025
L2REG=0.0001

TAG="lasagne_first_test_small_betaprime"

DATAFILENAME="minosmatch_fuel_me1Bmc_small.hdf5"
SAVEMODELNAME="$MEMBERWORK/hep105/output/$TAG/$TAG.npz"
PYTHONPROG="./minerva_triamese_betaprime.py"

COMMAND="$PYTHONPROG -l \
         -n $NEPOCHS \
         -r $LRATE \
         -g $L2REG \
         -s $SAVEMODELNAME \
         -d $PROJWORK/hep105/data/$DATAFILENAME"

./generate_workflow.py \
  --framework theano \
  --input_data "theano/$DATAFILENAME" \
  --tag $TAG \
  --command "$COMMAND"
