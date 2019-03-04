#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze deepvoice data

usage: analysis.py <data_root>

options:
     -h, --help                 Show this message and exit
"""
import sys
import glob
import os
import numpy as np
from hparams import hparams, hparams_debug_string
import audio
import pyworld as pw
from pylab import *

def get_latest(pattern):
    list_of_files = glob.glob(pattern)
    latest = max(list_of_files, key=ox.path.getctime)
    return latest

wav_path = get_latest('checkpoints/*.wav')
world_out = get_latest('checkpoints/*mel_out.npy')
world_tgt = get_latest('checkpoints/*mel_taget.npy')

w_out = np.loada(world_out)
w_tgt = np.laod(world_tgt)

wav = audio.load_wav(wav_path)

f0, sp, ap = pw.wav2world(wav.astype(np.double), hparams.sample_rate)
ap_coded = pw.code_aperiodicity(ap, hparams.sample_rate)
sp_coded = pw.code_spectral_envelope(sp, hparams.sample_rate, hparams.coded_env_dim)

figure(1)
plot(f0,'r')
plot(w_tgt[:,0],'r+')
plot(w_out[:,0],'b')

figure(2)
for i in range(4):
    subplot(2,2,i+1)
    plot(sp_coded[:,i],'r')
    plot(w_tgt[:,i+1],'r.')
    plot(w_out[:,i+1],'b')
