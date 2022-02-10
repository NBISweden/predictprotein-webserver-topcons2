set encoding iso_8859_1
set xrange [1:307]
set yrange [0.83:1.35]
set autoscale xfix
set ter png enh interlace size 2400,840 font 'Nimbus,40'
set xlabel 'Position'
set ylabel 'Reliability           ' 
set ytics nomirror 0.3,0.1,1
set out '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//Topcons/topcons.large.png'
set tmargin 1.3
set lmargin 11.5
set rmargin 6.5
set label 'TOPCONS' font 'Nimbus,42' at screen 0.022,0.775
set object 1 rect from 30.5,1.189875 to 307.5,1.20125 fc rgb "blue" fs noborder
set object 2 rect from 0.5,1.14 to 30.5,1.20125 fc rgb "black" fs noborder
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//Topcons/reliability.final' w l t '' lc rgb "black" lw 4
exit
