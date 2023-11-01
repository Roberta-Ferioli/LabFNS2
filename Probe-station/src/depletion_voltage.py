#!python3

'''
    Script to measure the depletion voltage from fits of a 1/C^2 vs V plot
    To run from the LabFNS2 folder:
        python3 -m Probe-station.src.depletion_voltage --input <input_file> --output <output_file>
        ./Probe-station/src/depletion_voltage.py --input INPUT_FILE --output OUTPUT_FILE

'''

import os
import argparse
import yaml

import numpy as np
import pandas as pd

#import uncertainties as unc

from ROOT import TFile, TGraphErrors, TF1, TCanvas, TLegend, gStyle, TText, TLatex
from ROOT import kGreen, kAzure

import os
import argparse
import numpy as np
import pandas as pd
from ROOT import TFile, TGraphErrors, TF1, TCanvas, TLegend, TText, TLatex, kGreen, kAzure


def yaml_load(file_path):
    """
    Load a YAML file and convert scientific notation values to float.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The YAML file contents as a dictionary.
    """
    with open(file_path, 'r') as f:
        yaml_data = yaml.safe_load(f)

    def convert_scientific_notation(value):
        try:
            return float(value)
        except ValueError:
            return value

    def recursive_convert_scientific_notation(data):
        if isinstance(data, dict):
            return {k: recursive_convert_scientific_notation(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [recursive_convert_scientific_notation(v) for v in data]
        else:
            return convert_scientific_notation(data)

    return recursive_convert_scientific_notation(yaml_data)

class DepletionAnalysis:

    def __init__(self, df: pd.DataFrame, args: argparse.Namespace):
        
        self.df = df
        self.sensor = args.sensor
        self.config = yaml_load(args.config)['detector'][args.sensor]

        self.outFile = TFile(args.output, 'recreate')

        output_path = os.path.splitext(args.output)[0] + '.pdf'
        self.iC2vV_outputPath = os.path.join(os.path.join(os.path.dirname(output_path), 'Figures'), f'1C2_{args.sensor}_vs_V.pdf')
        self.zoom_outputPath = os.path.join(os.path.join(os.path.dirname(output_path), 'Figures'), f'1C2_{args.sensor}_vs_V_zoom.pdf')
        self.dcon_outputPath = os.path.join(os.path.join(os.path.dirname(output_path), 'Figures'), f'doping_concentration_{args.sensor}.pdf')
        self.dpro_outputPath = os.path.join(os.path.join(os.path.dirname(output_path), 'Figures'), f'doping_profile_{args.sensor}.pdf')

        self.graph = None

        # standard texts for the plots
        gStyle.SetOptStat(0)
        gStyle.SetOptFit(0)

        self.text1 = 'Area = 1.0 #times 1.0 mm^{2}'
        self.text2 = f'{args.sensor} sensor'

    #####################
    # DATA PREPROCESSING

    def preprocess_data(self):
        ''''
            Preprocess the data to calculate the doping concentration and the depletion width
        '''
        print("Preprocessing data...")

        eSi = 11.7 * 8.854e-12                                      # F/m - dielectric constant of silicon
        A = 1e-6                                                    # m^2 - detector area
        q = 1.602e-19                                               # C - electron charge

        self.df['V_abs'] = np.abs(self.df['V'])
        self.df['1_C2'] = 1.0 / (self.df['C'] * self.df['C'])
        self.df['1_C2_err'] = 2.0 * self.df['C_err'] / (self.df['C'] * self.df['C'] * self.df['C'])

        self.df['1_C2_F'] = self.df['1_C2'] * 1e24                  # F^-2
        self.df['1_C2_err_F'] = self.df['1_C2_err'] * 1e24          # F^-2

        self.df['derivative'] = np.gradient(self.df['1_C2_F'], self.df['V_abs'])

        # error on the derivative
        self.df['derivative2_C'] = np.gradient(self.df['derivative'], self.df['1_C2_F'])
        self.df['derivative2_V'] = np.gradient(self.df['derivative'], self.df['V_abs'])
        self.df['derivative_err'] = np.sqrt((self.df['derivative2_C']*self.df['1_C2_err_F'])**2 + (self.df['derivative2_V']*self.df['V_err'])**2)

        # doping concentration
        self.df['NB'] = 2 / (eSi * A*A * q * self.df['derivative']) # m^-1
        self.df['NB_err'] = 2 / (eSi * A*A * q * self.df['derivative']**2) * self.df['derivative_err'] # m^-1

        # depletion width
        self.df['W'] = np.sqrt(2 * self.df['V_abs'] * eSi / (q * self.df['NB'])) # m
        self.df['W_err'] = np.sqrt((self.df['V_err']*self.df['W']/(2*self.df['V']))**2 + (self.df['NB_err']*self.df['W']/(2*self.df['NB']))**2)

    #####################
    # DATA ANALYSIS

    def print_zoom(self, xmin, xmax, ymin, ymax):
        '''
            Print the zoomed region of the plot

            Parameters
            ----------
            graph (TGraphErrors):   Graph with the data
            xmin (float):           Minimum x value
            xmax (float):           Maximum x value
            ymin (float):           Minimum y value
            ymax (float):           Maximum y value
            output_path (str):      Output path of the plot

            Returns
            -------
            None
        '''

        if self.graph is None:
            print('ERROR: graph is None')
            return

        self.graph.GetXaxis().SetRangeUser(xmin, xmax)
        self.graph.GetYaxis().SetRangeUser(ymin, ymax)

        canvas = TCanvas('1C2_zoom', 'canvas_zoom', 800, 600)
        self.graph.Draw('AP')    
        canvas.SetLeftMargin(0.15)

        legend = TLegend(0.45, 0.15, 0.65, 0.3)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.AddEntry(self.graph, 'LGAD Data', 'pe')
        legend.Draw()

        latex = TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.04)
        latex.SetNDC()
        #latex.DrawLatex(0.45, 0.35, '#splitline{Zoom of non-linearity in the}{  depletion of the gain layer}')

        canvas.SaveAs(self.zoom_outputPath)
        self.outFile.cd()
        canvas.Write()

    def inverseC2_vs_V(self):
        '''
            Create a plot with 1/C^2 vs bias voltage

            Returns
            -------
            None
        '''
        
        # Plot the data
        graph = TGraphErrors(len(self.df['V']), 
                             np.asarray(-self.df['V'], dtype=float), np.asarray(self.df['1_C2'], dtype=float), 
                             np.asarray(self.df['V_err'], dtype=float), np.asarray(self.df['1_C2_err'], dtype=float))
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        graph.SetMarkerColor(kAzure+1)
        graph.SetTitle('1/C^{2} vs V '+f'{args.sensor}'+'; Reverse bias [V]; 1/C^{2} [pF^{-2}]')

        self.graph = graph.Clone()
        
        # Fit the data
        
        # LGAD
        fit1 = TF1()
        if self.sensor == 'LGAD':   fit1 = self.fit(graph, self.config['fits'][0]['fit_range'][0], self.config[0]['fit_range'][1], 
                                                    init_fit_pars=[self.config['fits'][0]['parameters'][0]['value'], 
                                                                   self.config['fits'][0]['parameters'][0]['value']], line_color=797)
        fit2 = self.fit(graph, self.config['fits'][1]['fit_range'][0], self.config['fits'][1]['fit_range'][1], 
                        init_fit_pars=[self.config['fits'][1]['parameters'][0]['value'], 
                        self.config['fits'][1]['parameters'][0]['value']], line_color=862)
        fit3 = self.fit(graph, self.config['fits'][2]['fit_range'][0], self.config['fits'][2]['fit_range'][1], 
                        init_fit_pars=[self.config['fits'][2]['parameters'][0]['value'], 
                        self.config['fits'][2]['parameters'][0]['value']], line_color=kGreen+2)   

        if self.sensor == 'LGAD':   fit1.SetRange(self.config['fits'][0]['draw_range'][0], self.config['fits'][0]['draw_range'][1])
        fit2.SetRange(self.config['fits'][1]['draw_range'][0], self.config['fits'][1]['draw_range'][1])
        fit3.SetRange(self.config['fits'][2]['draw_range'][0], self.config['fits'][2]['draw_range'][1]) 

        # Find the intersection point
        intersection1 = 0.
        if self.sensor == 'LGAD':   intersection1 = self.find_intersection(fit2, fit1)
        intersection2 = self.find_intersection(fit3, fit2)

        canvas = TCanvas('1C2', 'canvas', 800, 600)
        canvas.DrawFrame(self.config['canvas_limits']['xmin'], self.config['canvas_limits']['ymin'],
                         self.config['canvas_limits']['xmax'], self.config['canvas_limits']['ymax'], '1/C^{2} vs V '+f'{args.sensor}'+'; Reverse bias [V]; 1/C^{2} [pF^{-2}]')
        #canvas.SetGrid()

        graph.Draw('P')
        if self.sensor == 'LGAD':   fit1.Draw('same')
        fit2.Draw('same')
        fit3.Draw('same')

        legend = TLegend(0.55, 0.15, 0.75, 0.35)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.AddEntry(graph, 'Data', 'pe')
        if self.sensor == 'LGAD':   legend.AddEntry(fit1, 'Gain layer depleted', 'l')
        legend.AddEntry(fit2, 'Bulk depletion', 'l')
        legend.AddEntry(fit3, 'Sensor fully depleted', 'l')
        legend.Draw()

        latex = TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.04)
        latex.SetNDC()
        if self.sensor == 'LGAD':
            latex.DrawLatex(0.15, 0.65, f'Sensor: {intersection2:.2f} V')
            latex.DrawLatex(0.15, 0.7, f'Gain layer: {intersection1:.2f} V')
            latex.DrawLatex(0.15, 0.75, 'Depletion voltage:')
        else:   latex.DrawLatex(0.55, 0.45, f'Sensor depletion: {intersection2:.2f} V')
        latex.DrawLatex(0.55, 0.5, self.text1)
        latex.DrawLatex(0.55, 0.55, self.text2)

        self.outFile.cd()
        canvas.Write()
        
        canvas.SaveAs(self.iC2vV_outputPath)

    # DOPING CONCENTRATION

    def doping_concentration(self):
        '''
            Plot the doping concentration vs bias voltage
        '''

        graph = TGraphErrors(len(self.df['V']), 
                             np.asarray(-self.df['V'], dtype=float), np.asarray(self.df['NB']*0.01, dtype=float), 
                             np.asarray(self.df['V_err'], dtype=float), np.asarray(self.df['NB_err']*0.01, dtype=float) )
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        graph.SetMarkerColor(kAzure+1)
        graph.SetTitle('Doping concentration '+f'{args.sensor}'+'; Reverse bias [V]; N_{B} [cm^{-1}]')

        canvas = TCanvas('doping_conc', 'canvas', 800, 600)
        canvas.DrawFrame(self.config['canvas_limits']['xmin'], self.config['canvas_limits']['conc_ymin'], 
                         self.config['canvas_limits']['xmax'], self.config['canvas_limits']['conc_ymax'], 
                         'Doping concentration '+f'{args.sensor}'+'; Reverse bias [V]; N_{B} [cm^{-1}]')
        canvas.SetLogy()

        graph.Draw('P')


        legend = TLegend(0.55, 0.15, 0.75, 0.35)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.AddEntry(graph, 'Data', 'pe')
        legend.Draw()

        latex = TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.04)
        latex.SetNDC()
        latex.DrawLatex(0.55, 0.4, self.text1)
        latex.DrawLatex(0.55, 0.45, self.text2)

        self.outFile.cd()
        canvas.Write()
        
        canvas.SaveAs(self.dcon_outputPath)

    def doping_profile(self):
        '''
            Plot the doping profile vs depth of the depleted region

        '''

        graph = TGraphErrors(len(self.df['W']), 
                             np.asarray(self.df['W']*1e6, dtype=float), np.asarray(self.df['NB']*0.01, dtype=float), 
                             np.asarray(self.df['W_err']*1e6, dtype=float), np.asarray(self.df['NB_err']*0.01, dtype=float) )
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1)
        graph.SetMarkerColor(kAzure+1)
        graph.SetTitle('Doping profile '+f'{args.sensor}'+'; Depth [#mum]; N_{B} [cm^{-1}]')
        graph.GetYaxis().SetRangeUser(-0.1, 0.24)

        canvas = TCanvas('doping_prof', 'canvas', 800, 600)
        canvas.DrawFrame(-1., self.config['canvas_limits']['conc_ymin'], 25., self.config['canvas_limits']['conc_ymax'], 'Doping profile '+f'{args.sensor}'+'; Depth [#mum]; N_{B} [cm^{-1}]')
        canvas.SetLogy()
        #canvas.SetGrid()

        graph.Draw('P')

        legend = TLegend(0.5, 0.55, 0.7, 0.75)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.AddEntry(graph, 'Data', 'pe')
        legend.Draw()

        latex = TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.04)
        latex.SetNDC()
        latex.DrawLatex(0.5, 0.8, self.text1)
        latex.DrawLatex(0.5, 0.85, self.text2)

        self.outFile.cd()
        canvas.Write()
        
        canvas.SaveAs(self.dpro_outputPath)

    def doping_concentration_cm3(self):
        '''
            Plot the doping concentration (cm^-3) vs bias voltage

            WORK IN PROGRESS
        '''

        graph = TGraphErrors(len(self.df['V_abs']), 
                             np.asarray(self.df['V_abs'], dtype=float), np.asarray(self.df['NB']*0.01, dtype=float), 
                             np.asarray(self.df['V_err'], dtype=float), np.asarray(self.df['NB_err']*0.01, dtype=float) )
        graph.SetMarkerStyle(20) 
        graph.SetMarkerSize(1)
        graph.SetMarkerColor(kAzure+1)
        graph.SetTitle('Doping concentration '+f'{args.sensor}'+'; Absolute reverse bias [V]; N_{B} [cm^{-1}]')
        graph.GetYaxis().SetRangeUser(-0.1, 0.24)

        canvas = TCanvas('doping_conc', 'canvas', 800, 600)
        canvas.DrawFrame(-1., 10**17, 25., 30*10**20, 'Doping concentration '+f'{args.sensor}'+'; Absolute reverse bias [V]; N_{B} [cm^{-1}]')
        canvas.SetLogy()
        #canvas.SetGrid()

        graph.Draw('P')


        legend = TLegend(0.15, 0.15, 0.35, 0.35)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        legend.AddEntry(graph, 'Data', 'pe')
        legend.Draw()

        #text1 = TText(0.55, 0.4, f'Sensor: {intersection2:.2f} V')
        #text1.SetNDC()
        #text1.SetTextFont(42)
        #text1.SetTextSize(0.04)
        #text1.Draw()
#
        #text2 = TText(0.55, 0.45, f'Gain layer: {intersection1:.2f} V')
        #text2.SetNDC()
        #text2.SetTextFont(42)
        #text2.SetTextSize(0.04)
        #text2.Draw()
#
        #text3 = TText(0.55, 0.5, f'Depletion voltage:')
        #text3.SetNDC()
        #text3.SetTextFont(42)
        #text3.SetTextSize(0.04)
        #text3.Draw()

        self.outFile.cd()
        canvas.Write()
        
        canvas.SaveAs(self.dcon_outputPath)

    #####################
    # PRIVATE-LIKE METHODS

    def fit(self, graph, fit_min, fit_max, init_fit_pars=None, lim_fit_pars=None, line_color=None):
        '''
            Fit a linear function to the data and return the fitted function 

            Parameters
            ----------
            graph : TGraphErrors
                Graph with the data
            fit_min : float
                Minimum x value for the fit
            fit_max : float
                Maximum x value for the fit
            line_color : int
                Color of the fitted function    

            Returns
            -------
            fit : TF1
                Fitted function 
        ''' 

        # Fit the graph
        fit = TF1('fit', '[0] + [1]*x', fit_min, fit_max)
        if init_fit_pars is not None:   fit.SetParameters(init_fit_pars[0], init_fit_pars[1])
        if lim_fit_pars is not None:    
            fit.SetParLimits(0, lim_fit_pars[0][0], lim_fit_pars[0][1])
            fit.SetParLimits(1, lim_fit_pars[1][0], lim_fit_pars[1][1])
        fit.SetParNames('a', 'b')
        if line_color is not None:      fit.SetLineColor(line_color)
        fit.SetLineStyle(1)
        fit.SetLineWidth(2)
        fit.SetNpx(1000)
        graph.Fit(fit, 'rm+')
        print(f'Chi2/NDF: {fit.GetChisquare():.2f} / {fit.GetNDF():.2f}')
        return fit

    def find_intersection(self, fit1, fit2):
        '''
            Find the intersection of two linear functions

            Parameters
            ----------
            fit1 : TF1
                First linear function
            fit2 : TF1
                Second linear function

            Returns
            -------
            intersection : float
                Intersection point of the two linear functions
        '''
        # Set up a new function that is the difference between the two input functions
        diff_func = TF1("diff_func", "([0]+[1]*x)", fit1.GetXmin(), fit2.GetXmax())
        diff_func.SetParameters((fit1.GetParameter(0) - fit2.GetParameter(0)), (fit1.GetParameter(1) - fit2.GetParameter(1)))

        # Find the intersection point of the difference function
        intersection = diff_func.GetX(0)

        return intersection





if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='depletion_voltage.py', description='Script to measure the depletion voltage from fits of a 1/C^2 vs V plot')
    parser.add_argument('--input', type=str, help='Input file with the 1/C^2 vs V data', required=True)
    parser.add_argument('--output', type=str, help='Output file with the plot', required=True)
    parser.add_argument('--config', type=str, default='Probe-station/src/depletion_voltage_conf.yml', help='Configuration file with the sensor parameters')
    parser.add_argument('--sensor', type=str, help='Sensor name', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, comment='#')
    depletion_analysis = DepletionAnalysis(df=df, args=args)

    depletion_analysis.preprocess_data()
    depletion_analysis.inverseC2_vs_V()
    depletion_analysis.print_zoom(0., 33., -0.2e-4, 1.4e-4)

    depletion_analysis.doping_concentration()
    depletion_analysis.doping_profile()

    