/*
    This is the header file for the preprocessor class.
    This class is used to read waveforms in input from a .root file and to process them.
    The waveforms are given as TGraph objects, one for each pixel.
    The preprocessor class is used to extract the following information from the waveforms:
        - baseline
        - minimum level
        - time of arrival at 10% of the amplitude
        - time of arrival at 90% of the amplitude
        - time of arrival at 50% of the amplitude
        - fall time
        - amplitude
        - RMS

    The preprocessor class is also used to build a new .root file containing the processed waveforms.
    The new .root file contains a TTree object with one entry for each pixel.
    The TTree object contains the following branches:
        nPixel PixelData object
        where PixelData is a struct containing the following information:
        - pixel: pixel number
        - baseline: baseline value
        - minLevel: minimum level of the waveform (basically baseline after the signal)
        - t10: time of arrival at 10% of the amplitude
        - t90: time of arrival at 90% of the amplitude
        - t50: time of arrival at 50% of the amplitude
        - fallTime: fall time of the waveform
        - amplitude: amplitude of the waveform
        - RMS: RMS of the waveform

    NOTE: The names of the TGraph in the input file are used to extract infomation from the file itself.
    In previous versions the name was "grEvXXXChanCYYYsampZZZ", where XXX is the event number, YYY is 
    the channel number and ZZZ is the sampling period in ps. This class is currently expecting 
    "grEvXXXPxYYYsampZZZ", where XXX is the event number, YYY is the pixel number and ZZZ is the
    sampling period in ps. For further changes in the TGraph input name please modifify the functions
    ReadInput() and ProcessEvent().
*/

#ifndef PREPROCESS_HH
#define PREPROCESS_HH

#include <TString.h>
#include <TFile.h>

#include "pixelData.hh"

class Preprocessor
{
    public:
        Preprocessor(const char * inFilePath, const double threshold = 10);
        ~Preprocessor();

        // parameters for the preprocessing. Fine tuning related to the waveform shape

        void SetIgnorePoints(const int ignorePoints) { fIgnorePoints = ignorePoints; }
        void SetChecks(const int checks) { fChecks = checks; }
        void SetNSample(const int nSample) { fNSample = nSample; }
        void SetNDerivativePoints(const int nDerivativePoints) { fNDerivativePoints = nDerivativePoints; }
        void SetNSmoothingPoints(const int nSmoothingPoints) { fNSmoothingPoints = nSmoothingPoints; }
        
        TString GetInFilePath() const { return fInFilePath; }
        int GetNPixels() const { return fNPixels; }
        int GetNEvents() const { return fNEvents; }
        int GetSamplingPeriod(const int pixel) const { return fSamplingPeriodDictionary[pixel]; }

        void UploadConversionValues(double (* mvToElectrons)[2]);


        void BuildTree(const char * outFilePath = "default");
        void BuildSeedAndClusterTree(const char * inFilePath = "default", const char * outFilePath = "default");

        void DrawPixel(const int event, const int pixel, const char * outFilePath = "default");
        void DrawEvent(const int event, const char * outFilePath = "default");

        

    protected:
        void ReadInput();
        void GenerateSamplingDictionary();

        bool ProcessEventScope(const int event, const int pixel, PixelData & pixelData, TFile * inFile);
        bool ProcessEventADC(const int event, const int pixel, PixelData & pixelData, TFile * inFile);
        bool GenerateSeedAndCluster(int & clusterSize, PixelData & seedData, PixelData & clusterData, PixelData * pixelData);


    private:

        TString fInFilePath;

        int fNPixels;
        int fNEvents;

        int * fSamplingPeriodDictionary;    // in ps
        double ** fmVToElectrons;           // dictionary to convert mV to electrons

        double fThreshold;                  // in mV
        int fIgnorePoints;                  // number of points to ignore at the beginning and at the end of the waveform
        int fChecks;                        // number of points to check to find the change in the derivative 
        int fNSample;                       // number of points to consider to calculate the mean and the RMS of both signal and derivative
        int fNDerivativePoints;             // number of points to consider to calculate the derivative
        int fNSmoothingPoints;              // number of points to consider to calculate the smoothing of the waveform for the derivative
        double fClusterThreshold;           // in mV - minimum amlitude to be counted for te cluster size of the event
};

#endif 