set encoding iso_8859_1
set xrange [1:365]
set yrange [0.83:1.4]
set autoscale xfix
set ter png enh interlace size 2400,840 font 'Nimbus,40'
set xlabel 'Position'
set ylabel 'Reliability           ' 
set ytics nomirror 0.2,0.1,1
set out '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//Topcons/topcons.large.png'
set tmargin 1.3
set lmargin 11.5
set rmargin 6.5
set label 'TOPCONS' font 'Nimbus,42' at screen 0.022,0.775
set object 1 rect from 33.5,1.16 to 141.5,1.173 fc rgb "red" fs noborder
set object 2 rect from 184.5,1.16 to 193.5,1.173 fc rgb "red" fs noborder
set object 3 rect from 272.5,1.16 to 281.5,1.173 fc rgb "red" fs noborder
set object 4 rect from 353.5,1.16 to 365.5,1.173 fc rgb "red" fs noborder
set object 5 rect from 0.5,1.217 to 12.5,1.23 fc rgb "blue" fs noborder
set object 6 rect from 162.5,1.217 to 163.5,1.23 fc rgb "blue" fs noborder
set object 7 rect from 214.5,1.217 to 251.5,1.23 fc rgb "blue" fs noborder
set object 8 rect from 302.5,1.217 to 332.5,1.23 fc rgb "blue" fs noborder
set object 9 rect from 12.5,1.16 to 33.5,1.23 fc rgb "white"
set object 10 rect from 141.5,1.16 to 162.5,1.23 fc rgb "grey" fs noborder
set object 11 rect from 163.5,1.16 to 184.5,1.23 fc rgb "white"
set object 12 rect from 193.5,1.16 to 214.5,1.23 fc rgb "grey" fs noborder
set object 13 rect from 251.5,1.16 to 272.5,1.23 fc rgb "white"
set object 14 rect from 281.5,1.16 to 302.5,1.23 fc rgb "grey" fs noborder
set object 15 rect from 332.5,1.16 to 353.5,1.23 fc rgb "white"
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//Topcons/reliability.final' w l t '' lc rgb "black" lw 4
exit
