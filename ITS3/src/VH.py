'''script to study linearity versus VH for inner pixel for baseline, falltime and amplitude
    and for outer pixels for baseline and amplitude
    for a better use of the script comment the part you don't need'''
import pandas as pd
import numpy as np
import glob
import re
import uproot
#import seaborn as sns

import sys
sys.path.append('utils')

from ROOT import TGraphErrors, TFile, TCanvas, kRed, kAzure, kOrange, kFullCircle, gROOT, TLatex, gStyle, TLegend, kBlack, kFullSquare,kFullTriangleUp, kFullTriangleDown, TH1D, kGreen, kViolet
from StyleFormatter import SetObjectStyle, SetGlobalStyle

def SetGraph(graph, name, title, color, marker):
    graph.SetName(name)
    graph.SetTitle(title)
    graph.SetMarkerStyle(marker)
    graph.SetMarkerSize(1.5)
    graph.SetMarkerColor(color)
    graph.SetLineColor(color)

if __name__=='__main__':
    #inner pixels if you have txt file with one data per pixel

    #dir_path='ITS3/Data/VH'
    #txt_files=glob.glob(dir_path+'/*.txt')
    #VHvalue=np.array([])
    #baseline=np.array([])
    #baseline_err=np.array([])
    #amplitude=np.array([])
    #amplitude_err=np.array([])
    #falltime=np.array([])
    #falltime_err=np.array([])

    #for file_name in txt_files:
        #parts=file_name.split('_')
        #VH=parts[2]
        #match= re.search(r'(\d+\.\d+)(?=V)',VH)
        #VHvalue=np.append(VHvalue, float(match.group()))

        #with open(file_name,'r') as file:
            #for line in file:
                #data=line.split()
                #baseline=np.append(baseline,float(data[0])*1000)
                #baseline_err=np.append(baseline_err,float(data[1])*1000)
                #amplitude=np.append(amplitude,float(data[2])*1000)
                #amplitude_err=np.append(amplitude_err,float(data[3])*1000)
                #falltime=np.append(falltime,float(data[4])*1.e9)
                #falltime_err=np.append(falltime_err,float(data[5])*1.e9)
  
    #gBaseline=TGraphErrors(len(VHvalue), np.asarray(VHvalue, dtype=float), np.asarray(baseline, dtype=float), np.zeros(len(VHvalue)), np.asarray(baseline_err, dtype=float))
    #SetGraph(gBaseline, "gBaseline", ";VH (V); Baseline (mV)", kRed+1, kFullCircle)
    #gAmplitude=TGraphErrors(len(VHvalue), np.asarray(VHvalue, dtype=float), np.asarray(amplitude, dtype=float), np.zeros(len(VHvalue)), np.asarray(amplitude_err, dtype=float))
    #SetGraph(gAmplitude, "gAmplitude", ";VH (V); Amplitude (mV)", kAzure+3, kFullCircle)
    #gFalltime=TGraphErrors(len(VHvalue), np.asarray(VHvalue, dtype=float), np.asarray(falltime, dtype=float), np.zeros(len(VHvalue)), np.asarray(falltime_err, dtype=float))
    #SetGraph(gFalltime, "gFalltime", ";VH (V); Falltime (ns)", kOrange+1, kFullCircle)

    #canvas = TCanvas("canvas","canvas",2200,600)
    #canvas.Divide(3,1)
    #canvas.cd(1)
    #hFrame = canvas.cd(1).DrawFrame(0,210,1.3,240,"Baseline vs VH; VH (V); Baseline (mV)")
    #gBaseline.Draw("p,same")
    #text =TLatex(0.15, 0.8,"APTS_AO10P_B6, Pixel 5")
    #text.SetNDC()
    #text.SetTextSize(gStyle.GetTextSize())
    #text.SetTextFont(42)
    #text.Draw()

    #canvas.cd(2)
    #hFrame = canvas.cd(2).DrawFrame(0,0,1.3,50,"Amplitude vs VH; VH (V); Amplitude (mV)")
    #gAmplitude.Draw("p,same")
    #text2 =TLatex(0.15, 0.80,"APTS_AO10P_B6, Pixel 5")
    #text2.SetNDC()
    #text2.SetTextSize(gStyle.GetTextSize())
    #text2.SetTextFont(42)
    #text2.Draw()
    #canvas.SaveAs('ITS3/data/output/Base_Ampli_VH.pdf')

    #canvas.cd(3)
    #hFrame = canvas.cd(3).DrawFrame(0,0,1.3,7,"Falltime vs VH; VH (V); Falltime (ns)")
    #gFalltime.Draw("p,same")
    #text3 =TLatex(0.4, 0.80,"APTS_AO10P_B6, Pixel 5")
    #text3.SetNDC()
    #text3.SetTextSize(gStyle.GetTextSize())
    #text3.SetTextFont(42)
    #text3.Draw()
    #canvas.SaveAs('ITS3/data/output/VH.pdf')

    #inner pixel2 if you have txt file with dato of all pixel, one txt file for VH value
    '''
    colorArr = [kRed , kAzure, kBlack, kOrange-3]
    markerArr = [kFullCircle, kFullSquare, kFullTriangleUp, kFullTriangleDown]
    pixelArr=np.array([])
    VH2=np.array([])
    dir_path2='ITS3/Data/VH2'
    txt_files2=glob.glob(dir_path2+'/*.txt')
    BasgraphArray=np.array([], dtype=TGraphErrors)
    AmgraphArray=np.array([], dtype=TGraphErrors)
    FallgraphArray=np.array([], dtype=TGraphErrors)
    for file_name2 in txt_files2:
        baseline=np.array([])
        baseline_err=np.array([])
        amplitude=np.array([])
        amplitude_err=np.array([])
        falltime=np.array([])
        falltime_err=np.array([])
        VH2=np.array([])
        parts=file_name2.split('j')
        pixel=parts[1]
        print(pixel)
        match= re.search(r'(\d+)(?=.txt)',pixel)
        print(match.group())
        pixelArr=np.append(pixelArr, int(match.group()))
        index=0
        with open(file_name2,'r') as file:
            for line in file:
                data=line.split()
                if index==0:
                    print(data[0])
                baseline=np.append(baseline,float(data[0])*1000)
                baseline_err=np.append(baseline_err,float(data[1])*1000)
                amplitude=np.append(amplitude,float(data[2])*1000)
                amplitude_err=np.append(amplitude_err,float(data[3])*1000)
                falltime=np.append(falltime,float(data[4])*1.e9)
                falltime_err=np.append(falltime_err,float(data[5])*1.e9)
                VH2=np.append(VH2,0.4 + index*0.1)
                index+=1
        BasgraphArray=np.append(BasgraphArray,TGraphErrors(len(VH2), np.asarray(VH2, dtype=float), np.asarray(baseline, dtype=float), np.zeros(len(VH2)), np.asarray(baseline_err, dtype=float)))
        AmgraphArray=np.append(AmgraphArray,TGraphErrors(len(VH2), np.asarray(VH2, dtype=float), np.asarray(amplitude, dtype=float), np.zeros(len(VH2)), np.asarray(amplitude_err, dtype=float)))
        FallgraphArray=np.append(FallgraphArray,TGraphErrors(len(VH2), np.asarray(VH2, dtype=float), np.asarray(falltime, dtype=float), np.zeros(len(VH2)), np.asarray(falltime_err, dtype=float)))
    
    canvas2 = TCanvas("canvas2","canvas2",2200,600)
    canvas2.Divide(3,1)
    canvas2.cd(1)
    hFrame = canvas2.cd(1).DrawFrame(0.3,200,1.3,280,"Baseline vs VH; VH (V); Baseline (mV)")
    legend = TLegend(0.15,0.7,0.4,0.9)
    for i in range(len(pixelArr)):
        SetGraph(BasgraphArray[i], "gBaseline" +str(i), ";VH (V); Baseline (mV)", colorArr[i], markerArr[i])
        BasgraphArray[i].Draw("p,same")
        legend.AddEntry(BasgraphArray[i], "Pixel "+str(int(pixelArr[i])))
    legend.Draw()
    canvas2.cd(2)
    hFrame = canvas2.cd(2).DrawFrame(0.3,0,1.3,80,"Amplitude vs VH; VH (V); Amplitude (mV)")
    legend2 = TLegend(0.15,0.7,0.4,0.9)
    for i in range(len(pixelArr)):
        SetGraph(AmgraphArray[i], "gAmplitude"+str(i), ";VH (V); Amplitude (mV)", colorArr[i], markerArr[i])
        AmgraphArray[i].Draw("p,same")
        legend2.AddEntry(AmgraphArray[i], "Pixel "+str(int(pixelArr[i])))
    legend2.Draw()
    canvas2.cd(3)
    hFrame = canvas2.cd(3).DrawFrame(0.3,0.06,1.3,0.13,"Falltime vs VH; VH (V); Falltime (ns)")
    legend3 = TLegend(0.6,0.2,0.8,0.4)
    for i in range(len(pixelArr)):
        SetGraph(FallgraphArray[i], "gFalltime"+str(i), ";VH (V); Falltime (ns)", colorArr[i], markerArr[i])
        FallgraphArray[i].Draw("p,same")
        legend3.AddEntry(FallgraphArray[i], "Pixel "+str(int(pixelArr[i])))
    legend3.Draw()
    canvas2.SaveAs('ITS3/data/output/VH2.pdf')
    '''
    #outer pixels
    colorArr =[kGreen+1,kViolet,kViolet+1,kGreen+4,kViolet-1,kAzure,kOrange -3,kViolet -4,kViolet +3,kBlack,kRed,kViolet-9,kGreen -2,kViolet -6,kViolet +7,kGreen -7]
    markerArr = 4*[kFullCircle, kFullSquare, kFullTriangleUp, kFullTriangleDown]
    VHex=np.array([])
    AmpliPx=[]
    BasePx=[]
    AmpliErrPx=[]
    BaseErrPx=[]
    AmpliPx = [[] for _ in range(9)]
    BasePx = [[] for _ in range(9)]
    AmpliErrPx = [[] for _ in range(9)]
    BaseErrPx = [[] for _ in range(9)]
    BasgraphArray = []
    AmgraphArray = []
    adc_unit=0.03881
    indexFile=0
    dir_path='ITS3/Data/VH_external_pixel'
    root_files=glob.glob(dir_path+'/*.root')
    for indexFile, file_name in enumerate(root_files):
        parts=file_name.split('{')
        VHpart=parts[1]
        match= re.search(r'(\d+)(?=})',VHpart)
        VHex=np.append(VHex, 0.001*int(match.group()))
        df=uproot.open(file_name)['PreprocessedData;1']
        ArrHistoAmp=[]
        ArrHistoBase=[]
        nPixels = 16 
        dfs = {}

        for i in range(nPixels):
            dfs[i] = df[f"pixel{i}"].arrays(library="pd")
        dfs
        for j in range(nPixels):
            ha=TH1D("Amplitude"+str(j),"Amplitude"+str(j),10,0,100)
            ArrHistoAmp.append(ha)
            hb=TH1D("Baseline"+str(j),"Baseline"+str(j),10,0,1000)
            ArrHistoBase.append(hb)
            for i in range(len(dfs[j])):
                ArrHistoAmp[j].Fill(dfs[j].loc[i]["amplitude"]*adc_unit)
                ArrHistoBase[j].Fill(dfs[j].loc[i]["baseline"]*adc_unit)
            AmpliPx[indexFile].append(ArrHistoAmp[j].GetMean())
            BasePx[indexFile].append(ArrHistoBase[j].GetMean())
            if(j==0):
                print(indexFile)
            AmpliErrPx[indexFile].append(ArrHistoAmp[j].GetRMS())
            BaseErrPx[indexFile].append(ArrHistoBase[j].GetRMS())
        indexFile+=1
    print(len(BasePx))
    for i in range(len(AmpliPx[0])):
        base_px_values = [row[i] for row in BasePx]
        print(base_px_values)
        base_err_px_values = [row[i] for row in BaseErrPx]
        ampli_px_values = [row[i] for row in AmpliPx]
        ampli_err_px_values = [row[i] for row in AmpliErrPx]

        BasgraphArray.append(TGraphErrors(len(VHex), np.asarray(VHex, dtype=float), np.asarray(base_px_values, dtype=float), np.zeros(len(VHex)), np.asarray(base_err_px_values, dtype=float)))
        AmgraphArray.append(TGraphErrors(len(VHex), np.asarray(VHex), np.asarray(ampli_px_values, dtype=float), np.zeros(len(VHex)), np.asarray(ampli_err_px_values, dtype=float)))
        SetGraph(BasgraphArray[i], "gBaseline" + str(i), ";VH (V); Baseline (mV)", colorArr[i], markerArr[i])
        SetGraph(AmgraphArray[i], "gAmplitude" + str(i), ";VH (V); Amplitude (mV)", colorArr[i], markerArr[i])
    canvas3 = TCanvas("canvas3","canvas3",2200,600)
    canvas3.Divide(2,1)
    canvas3.cd(1)
    hFrame = canvas3.cd(1).DrawFrame(0.3,200,1.300,330,"Baseline vs VH; VH (V); Baseline (mV)")
    legend = TLegend(0.15,0.65,0.35,0.9)
    for i in range(len(AmpliPx[0])):
        if(i==0 or i==15 or i==7 or i==8):
            BasgraphArray[i].Draw("p,same")
            legend.AddEntry(BasgraphArray[i], "Pixel "+str(int(i)))
    legend.Draw()
    text =TLatex(0.6, 0.8,"APTS_AO10P_B6")
    text2 =TLatex(0.6, 0.73,"External Pixels")
    text1 =TLatex(0.6, 0.4,"APTS_AO10P_B6")
    text3 =TLatex(0.6, 0.33,"External Pixels")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.Draw()
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize())
    text2.SetTextFont(42)
    text2.Draw()
    canvas3.cd(2)
    hFrame = canvas3.cd(2).DrawFrame(0.3,0,1.300,80,"Amplitude vs VH; VH (V); Amplitude (mV)")
    legend2 = TLegend(0.15,0.65,0.35,0.9)
    for i in range(len(AmpliPx[0])):
        if(i==0 or i==15 or i==7 or i==8):
            AmgraphArray[i].Draw("p,same")
            legend2.AddEntry(AmgraphArray[i], "Pixel "+str(int(i)))
    legend2.Draw()
    text1.SetNDC()
    text1.SetTextSize(gStyle.GetTextSize())
    text3.SetTextFont(42)
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize())
    text1.Draw()
    text3.Draw()
    canvas3.SaveAs('ITS3/data/output/VH_external_pixel.pdf')