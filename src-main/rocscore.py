from __future__ import division
from pylab import * # https://stsievert.com/blog/2015/09/01/matlab-to-python/
from my_src import *
def rocscore(Yreal=None, YTrue=None, **kwargs):
   nargin, nargout = my_arg_reader(Yreal, YTrue, **kwargs)
   
   
   # Compute the ROC AUC (area under curve) score, the ROC EER (equal error rate)
   # and the ROC curve itself from given classifier data.
   #
   # Author: Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
   #
   # Input
   #   Yreal: (n,1) real numbered classification outputs (bias not important).
   #   YTrue: (n,1) ground truth (-1 and 1) labels.
   #
   # Output
   #   rocauc: Real positive ROC area under curve score (between 0 and 1).
   #   eer: Equal Error Rate (EER), TP at the point where TP==(1-FP).
   #   roccurve: (n,2) roc curve data, first column: FP, second row TP.
   
   [dsorted,idx]=my_sort(Yreal,1,'descend')   # Higher values first
   L_pos=find(YTrue==1)
   L_neg=find(YTrue==-1)
   
   roccurve=zeros(len(dsorted),2)
   fp_rate_last=0
   eer_res_min=Inf   # EER residue minimum
   eer_min_idx=-1      # ROC curve index realizing minimal tp==(1-fp)
   
   i=1
   c=1
   eer=-1
   while i <= len(dsorted):
      tr=dsorted(i)   # Obtain threshold
   
      # Check if there is more than one sample qualifying with the same value:
      similar=0
      for j in range((i+1), len(dsorted)+1):
         if abs(dsorted(i)-dsorted(j)) < 1e-9:
            similar=similar+1
         else:
            break
         #end
      #end
      if similar > 0:
         i=i+similar
      #end
   
      tp_count=len(intersect(idx(1-1):(i-1),L_pos))
      fp_count=len(intersect(idx(1-1):(i-1),L_neg))
      tp_rate = tp_count/len(L_pos)
      fp_rate = fp_count/len(L_neg)
   
      roccurve[c-1,:]=array([ fp_rate, tp_rate ])
   
      # Do linear interpolation on the previous line segment to find the EER
      if c > 1:
         alpha = (1-roccurve(c-1,1)-roccurve(c-1,2)) / (roccurve(c,2)-roccurve(c-1,2)+roccurve(c,1)-roccurve(c-1,1))
   
         if alpha >= 0 and alpha <= 1:
            eerpoint=array([[ roccurve(c-1,2) ],[ roccurve(c-1,1) ]]) + alpha @ array([[ roccurve(c,2)-roccurve(c-1,2) ],[ roccurve(c,1)-roccurve(c-1,1) ]])
   
            eer = eerpoint(1,1)
         #end
      #end
   
      c=c+1
      i=i+1
   #end
   
   # Remove last element.
   roccurve=roccurve[(1-1):(c-1-1),:]
   
   # Numerically integrate AUC score of roc curve by linear interpolation.
   rocauc=0
   for p in range(2, my_size(roccurve,1)+1):
      width=roccurve(p,1)-roccurve(p-1,1)
      rocauc=rocauc + width @ (roccurve(p-1,2) + ((roccurve(p,2)-roccurve(p-1,2))/2))
   #end
   return rocauc, eer, roccurve
   