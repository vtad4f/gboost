
gboost - ~~Matlab~~ Python graph boosting package
======================================

**Forked from:** https://github.com/rkwitt/gboost/


Description
-----------
<a name="description"/>

See parent repository for original description. The original .m files have been preserved in the repo under src-convert/original-m. With the exception of a few indentation fixes (python is sensitive) they should be untouched.

This repo has become a matlab to python conversion utility more thatn anything. Once the original matlab code is fully converted I would recommend breaking out the conversion script(s) into a new repo (something like m2py). I believe this is worthwhile because at least for now there don't seem to be fully-implemented conversion scripts.

The two closest implementations I've seen of matlab to python conversion code are smop and ompc. I tried smop first once I realized how time consuming writing my own utility would be. It does pip install successfully and does an ok job of swapping out function definitions, but watch out for concat and a few other pitfalls. It becomes quickly apparent how many additional functions have to be defined in addition to what comes with the smoplib import.

Next I tried ompc. I went ahead and forked my own vtad4f version of it (see Makefile) because I thought the mex replacement code could be useful. The author spoke highly of it, and I thought it would be a better starting point than nothing. That being said, that last time I hooked it up I got a seg fault. 


Authors
-------
<a name="authors"/>

* Vincent Allen <vtad4f@mst.edu>
* Roland Kwitt <roland.kwitt@sbg.ac.at>
* Sebastian Nowozin <sebastian.nowozin@tuebingen.mpg.de>
  * Matlab wrappers, LPBoost, modifications to gSpan implementation
* Taku Kudo <taku@google.com>
 * C++ gSpan implementation
* Intelligent Systems and Artificial Vision Lab, SIVALab of the University of Naples ''Federico II''.
 * VFLib graph matching library


License
-------
<a name="lic"/>

The software is dual licensed under the GNU General Public License version 2
and the Mozilla Public License, version 1.1.  This means that you can choose
any of the two licenses.

The licenses are included as LICENSE.txt (GPL version 2) and MPL-1.1.txt
(Mozilla Public License, version 1.1).

```bash
GNU General Public License

Copyright (C) 2006 Sebastian Nowozin,
Copyright (C) 2004 Taku Kudo,
Copyright (C) 2001 Dipartimento di Informatica e Sistemistica, Universit
    degli studi di Napoli ``Federico II'',
All rights reserved.

This is free software with ABSOLUTELY NO WARRANTY.

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place - Suite 330, Boston, MA 02111-1307, USA
```

```
Mozilla Public License

``The contents of this distribution are subject to the Mozilla Public License
Version 1.1 (the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
the specific language governing rights and limitations under the License.

     The Original Code is "gboost Matlab toolbox".

     The Initial Developer of the Original Code is Sebastian Nowozin.
     Portions created by Taku Kudo are Copyright (C) 2007.
     Portions created by Dipartimento di Informatica e Sistemistica,
        Universit degli studi di Napoli ``Federico II'' are
        Copyright (C) 2001.
     All Rights Reserved.

Alternatively, the contents of this distribution may be used under the terms
of the GNU General Public License, version 2 (the  "GPL 2 License"), in which
case the provisions of GNU General Public License are applicable instead of
those above.  If you wish to allow use of your version of this file only under
the terms of the GNU General Public License and not to allow others to use
your version of this file under the MPL, indicate your decision by deleting
the provisions above and replace  them with the notice and other provisions
required by the GNU General Public License.  If you do not delete the
provisions above, a recipient may use your version of this file under either
the MPL or the GNU General Public License, version 2.''
```

Installation
============
<a name="install"/>

Run setup.sh
* Pip installs for smop, matplotlib, and pycvx will happen first
* Linux  seems to be necessary for the pycvx pip install
* Python 3 is currently a requirement as well (I went with the @ matrix multiplication operator)


Documentation
-------------
<a name="doc"/>

The source code is well documented, but here is a list of the most important
parts.

`gspan.m` is the Matlab side interface of Taku's gSpan code.  It can perform
both frequent subgraph mining as well as weighted subgraph mining.  The first
is useful for data mining purposes, while the second is used in graph
boosting.

`findhypothesis_graph.m` is the interface between LPBoost and the weighted graph
mining algorithm (gSpan).  The duty of `findhypothesis_graph` is to create
decision stumps which correspond to the most violated constraint in the LP
dual (column-generation).  In fact, you can use the included `lpboost1d5.m` with
any other decision stump, you only need to write a suitable `findhypothesis_*.m`
function.

`lpboost.m` is an implementation of 1-class, 2-class and "1.5-class"
nu-LPBoosting.  The 1-class and 2-class formulations are explained in
[\[Demiriz2002\]](#ref), the 1.5-class formulation learns a 1-class classifier but also
takes into account negative samples.

`graphmatch.mex*` is a wrapper around VFLib to perform subgraph-graph
isomorphism matching.  It can output all matches and is used for the testing
on unlabeled samples.  It can match both directed and undirected graphs.

`mexgspan.mex*` is the gSpan Matlab wrapper.

`rocscore.m` is a simple function calculating the ROC AUC and ROC EER score as
well as the ROC curve itself.

Demonstration
-------------
<a name="demo"/>

Start Matlab and go to the bin/ directory.  Running the example.m script will
guide you through the training of a graph boosting classifier for a small
molecule example set. Assuming that your CVX install is at `/Software/cvx/`,
and you checked out gboost at `/Software/gboost`, run

```matlab
cd '/Software/cxv'
cvx_setup
cd '/Software/gboost'
example
```

If you have any questions, please feel free to email the first author.

References
----------
<a name="ref"/>

[Demiriz2002], Ayhan Demiriz, Kristin P. Bennett and John Shawe-Taylor,
   "Linear Programming Boosting via Column Generation", 2002, Journal of
   Machine Learning, Vol. 46, pages 225-254,
   http://www.rpi.edu/~bennek/rev_mlj6.ps

[Kudo2004], Taku Kudo, Eisaku Maeda and Yuji Matsumoto,
   "An Application of Boosting to Graph Classification", NIPS 2004,
   http://books.nips.cc/papers/files/nips17/NIPS2004_0369.pdf

[Yan2002], Xifeng Yan and Jiawei Han,
   "gSpan: Graph-Based Substructure Pattern Mining", ICDM 2002,
   http://computer.org/proceedings/icdm/1754/17540721abs.htm"

