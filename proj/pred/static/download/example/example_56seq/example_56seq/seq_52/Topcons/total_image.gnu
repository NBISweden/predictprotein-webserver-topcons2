set encoding iso_8859_1
set yrange [0:50]
set xrange [1:372]
set y2range [-2:28.8]
set autoscale xfix
set ter png enh interlace size 2400,1680 font 'Nimbus,40'
set y2label '{/Symbol D}G (kcal/mol)                                             ' tc lt 3
set ytics scale 1,0.5 nomirror ("0" 0, "5" 5, "10" 10, "15" 15, "20" 20, "25" 25, "SPOCTOPUS" 30.5 0, "SCAMPI" 33.5 0, "PolyPhobius" 36.5 0, "Philius" 39.5 0, "OCTOPUS" 42.5 0, "TOPCONS" 45.5 0)
set y2tics nomirror 0,2,16
set out '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//Topcons/total_image.large.png'
set lmargin 13.5
set rmargin 6.5
set tmargin 1.3
set object 1 rect from screen 0.19,0.986 to screen 0.21,0.992 fc rgb "red" fs noborder
set label 'Inside' font 'Nimbus,30' at screen 0.215,0.982
set object 2 rect from screen 0.28,0.986 to screen 0.30,0.992 fc rgb "blue" fs noborder
set label 'Outside' font 'Nimbus,30' at screen 0.305,0.982
set object 3 rect from screen 0.38,0.978 to screen 0.40,1 fc rgb "grey" fs noborder
set label 'TM-helix (IN->OUT)' font 'Nimbus,30' at screen 0.405,0.982
set object 4 rect from screen 0.57,0.978 to screen 0.59,1 fc rgb "white"
set label 'TM-helix (OUT->IN)' font 'Nimbus,30' at screen 0.595,0.982
set object 5 rect from screen 0.76,0.978 to screen 0.78,1 fc rgb "black"
set label 'Signal peptide' font 'Nimbus,30' at screen 0.785,0.982
set object 6 rect from 20.5,30.8 to 372.5,31 fc rgb "blue" fs noborder
set object 7 rect from 0.5,30 to 20.5,31 fc rgb "black" fs noborder
set object 8 rect from 0.5,33 to 3.5,33.2 fc rgb "red" fs noborder
set object 9 rect from 24.5,33.8 to 372.5,34 fc rgb "blue" fs noborder
set object 10 rect from 3.5,33 to 24.5,34 fc rgb "grey" fs noborder
set object 11 rect from 20.5,36.8 to 372.5,37 fc rgb "blue" fs noborder
set object 12 rect from 0.5,36 to 20.5,37 fc rgb "black" fs noborder
set object 13 rect from 20.5,39.8 to 372.5,40 fc rgb "blue" fs noborder
set object 14 rect from 0.5,39 to 20.5,40 fc rgb "black" fs noborder
set object 15 rect from 0.5,42 to 2.5,42.2 fc rgb "red" fs noborder
set object 16 rect from 23.5,42.8 to 372.5,43 fc rgb "blue" fs noborder
set object 17 rect from 2.5,42 to 23.5,43 fc rgb "grey" fs noborder
set object 18 rect from 21.5,45.8 to 372.5,46 fc rgb "blue" fs noborder
set object 19 rect from 0.5,45 to 21.5,46 fc rgb "black" fs noborder
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//DG1.txt' axes x1y2 w l t '' lt 3 lw 4
exit
