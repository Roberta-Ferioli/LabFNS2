import pandas as pd
import numpy as np

import sys
sys.path.append('utils')

from ROOT import TGraphErrors, TFile, TCanvas, TLegend, kRed, kAzure, kOrange, kFullCircle, kFullSquare, gROOT
from DfUtils import GetGraphErrorsFromCSV
from StyleFormatter import SetObjectStyle, SetGlobalStyle

if __name__=='__main__':
    
    gROOT.SetBatch()
    SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

    infileLGAD = 'Probe-station/data/input/C_vs_f_LGAD.csv'
    infilePin = 'Probe-station/data/input/C_vs_f_pin.csv'
    infileStrip = 'Probe-station/data/input/C_vs_f_strip.csv'
    outfilename = 'Probe-station/data/output/C_vs_f.root'
    
    gLGAD = GetGraphErrorsFromCSV(infileLGAD)
    gLGAD.SetName("gLGAD")
    gLGAD.SetTitle("LGAD; Frequency (kHz); Capacitance (pF)")
    gLGAD.SetMarkerStyle(kFullCircle)
    gLGAD.SetMarkerSize(1)
    gLGAD.SetMarkerColor(kRed+1)
    gLGAD.SetLineColor(kRed+1)
    
    gPin = GetGraphErrorsFromCSV(infilePin)
    gPin.SetName("gPin")
    gPin.SetTitle("Pin; Frequency (kHz); Capacitance (pF)")
    gPin.SetMarkerStyle(kFullSquare)
    gPin.SetMarkerSize(1)
    gPin.SetMarkerColor(kAzure + 3)
    gPin.SetLineColor(kAzure + 3)

    gStrip = GetGraphErrorsFromCSV(infileStrip)
    gStrip.SetName("gStrip")
    gStrip.SetTitle("Strip; Frequency (kHz); Capacitance (pF)")
    gStrip.SetMarkerStyle(kFullSquare)
    gStrip.SetMarkerSize(1)
    gStrip.SetMarkerColor(kOrange - 3)
    gStrip.SetLineColor(kOrange - 3)
    
    canvas = TCanvas("canvas","canvas",1000,1000)
    hFrame = canvas.cd().DrawFrame(0,1,600,350,"; Frequency [kHz]; Capacitance (pF)")
    canvas.SetLogx()
    #canvas.SetLogy()
    gPin.Scale(10)
    gPin.Draw("p,same")
    gLGAD.Draw("p,same")
    gStrip.Draw("p,same")

    legend = TLegend(0.6, 0.7, 0.8, 0.85)
    legend.SetTextSize(0.03)
    legend.AddEntry(gLGAD,'LGAD, V = 1V','p')
    legend.AddEntry(gPin,'10 #times PIN, V = 0V','p')
    legend.AddEntry(gStrip,'Strip, V = 25V','p')
    legend.Draw("same")

    canvas.Modified()
    canvas.Update()
    
    canvas.SaveAs('Probe-station/data/output/C_vs_f.pdf')

    outfile = TFile(outfilename, 'recreate')
    gLGAD.Write()
    gPin.Write()
    canvas.Write()
    outfile.Close()
