set encoding iso_8859_1
set yrange [0:50]
set xrange [1:336]
set y2range [-2:27.6]
set autoscale xfix
set ter png enh interlace size 2400,1680 font 'Nimbus,40'
set y2label '{/Symbol D}G (kcal/mol)                                             ' tc lt 3
set ytics scale 1,0.5 nomirror ("0" 0, "5" 5, "10" 10, "15" 15, "20" 20, "25" 25, "SPOCTOPUS" 30.5 0, "SCAMPI" 33.5 0, "PolyPhobius" 36.5 0, "Philius" 39.5 0, "OCTOPUS" 42.5 0, "TOPCONS" 45.5 0)
set y2tics nomirror -3,2,14
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
set object 6 rect from 33.5,30 to 148.5,30.2 fc rgb "red" fs noborder
set object 7 rect from 179.5,30 to 188.5,30.2 fc rgb "red" fs noborder
set object 8 rect from 267.5,30 to 277.5,30.2 fc rgb "red" fs noborder
set object 9 rect from 0.5,30.8 to 12.5,31 fc rgb "blue" fs noborder
set object 10 rect from 163.5,30.8 to 164.5,31 fc rgb "blue" fs noborder
set object 11 rect from 209.5,30.8 to 246.5,31 fc rgb "blue" fs noborder
set object 12 rect from 298.5,30.8 to 336.5,31 fc rgb "blue" fs noborder
set object 13 rect from 12.5,30 to 33.5,31 fc rgb "white"
set object 14 rect from 148.5,30 to 163.5,31 fc rgb "grey" fs noborder
set object 15 rect from 164.5,30 to 179.5,31 fc rgb "white"
set object 16 rect from 188.5,30 to 209.5,31 fc rgb "grey" fs noborder
set object 17 rect from 246.5,30 to 267.5,31 fc rgb "white"
set object 18 rect from 277.5,30 to 298.5,31 fc rgb "grey" fs noborder
set object 19 rect from 35.5,33 to 158.5,33.2 fc rgb "red" fs noborder
set object 20 rect from 211.5,33 to 251.5,33.2 fc rgb "red" fs noborder
set object 21 rect from 297.5,33 to 336.5,33.2 fc rgb "red" fs noborder
set object 22 rect from 0.5,33.8 to 14.5,34 fc rgb "blue" fs noborder
set object 23 rect from 179.5,33.8 to 190.5,34 fc rgb "blue" fs noborder
set object 24 rect from 272.5,33.8 to 276.5,34 fc rgb "blue" fs noborder
set object 25 rect from 14.5,33 to 35.5,34 fc rgb "white"
set object 26 rect from 158.5,33 to 179.5,34 fc rgb "grey" fs noborder
set object 27 rect from 190.5,33 to 211.5,34 fc rgb "white"
set object 28 rect from 251.5,33 to 272.5,34 fc rgb "grey" fs noborder
set object 29 rect from 276.5,33 to 297.5,34 fc rgb "white"
set object 30 rect from 0.5,36 to 11.5,36.2 fc rgb "red" fs noborder
set object 31 rect from 178.5,36 to 189.5,36.2 fc rgb "red" fs noborder
set object 32 rect from 267.5,36 to 276.5,36.2 fc rgb "red" fs noborder
set object 33 rect from 35.5,36.8 to 149.5,37 fc rgb "blue" fs noborder
set object 34 rect from 212.5,36.8 to 243.5,37 fc rgb "blue" fs noborder
set object 35 rect from 298.5,36.8 to 336.5,37 fc rgb "blue" fs noborder
set object 36 rect from 11.5,36 to 35.5,37 fc rgb "grey" fs noborder
set object 37 rect from 149.5,36 to 178.5,37 fc rgb "white"
set object 38 rect from 189.5,36 to 212.5,37 fc rgb "grey" fs noborder
set object 39 rect from 243.5,36 to 267.5,37 fc rgb "white"
set object 40 rect from 276.5,36 to 298.5,37 fc rgb "grey" fs noborder
set object 41 rect from 0.5,39 to 10.5,39.2 fc rgb "red" fs noborder
set object 42 rect from 178.5,39 to 188.5,39.2 fc rgb "red" fs noborder
set object 43 rect from 267.5,39 to 276.5,39.2 fc rgb "red" fs noborder
set object 44 rect from 33.5,39.8 to 158.5,40 fc rgb "blue" fs noborder
set object 45 rect from 211.5,39.8 to 244.5,40 fc rgb "blue" fs noborder
set object 46 rect from 296.5,39.8 to 336.5,40 fc rgb "blue" fs noborder
set object 47 rect from 10.5,39 to 33.5,40 fc rgb "grey" fs noborder
set object 48 rect from 158.5,39 to 178.5,40 fc rgb "white"
set object 49 rect from 188.5,39 to 211.5,40 fc rgb "grey" fs noborder
set object 50 rect from 244.5,39 to 267.5,40 fc rgb "white"
set object 51 rect from 276.5,39 to 296.5,40 fc rgb "grey" fs noborder
set object 52 rect from 33.5,42 to 148.5,42.2 fc rgb "red" fs noborder
set object 53 rect from 179.5,42 to 188.5,42.2 fc rgb "red" fs noborder
set object 54 rect from 267.5,42 to 277.5,42.2 fc rgb "red" fs noborder
set object 55 rect from 0.5,42.8 to 12.5,43 fc rgb "blue" fs noborder
set object 56 rect from 163.5,42.8 to 164.5,43 fc rgb "blue" fs noborder
set object 57 rect from 209.5,42.8 to 246.5,43 fc rgb "blue" fs noborder
set object 58 rect from 298.5,42.8 to 336.5,43 fc rgb "blue" fs noborder
set object 59 rect from 12.5,42 to 33.5,43 fc rgb "white"
set object 60 rect from 148.5,42 to 163.5,43 fc rgb "grey" fs noborder
set object 61 rect from 164.5,42 to 179.5,43 fc rgb "white"
set object 62 rect from 188.5,42 to 209.5,43 fc rgb "grey" fs noborder
set object 63 rect from 246.5,42 to 267.5,43 fc rgb "white"
set object 64 rect from 277.5,42 to 298.5,43 fc rgb "grey" fs noborder
set object 65 rect from 33.5,45 to 136.5,45.2 fc rgb "red" fs noborder
set object 66 rect from 179.5,45 to 188.5,45.2 fc rgb "red" fs noborder
set object 67 rect from 267.5,45 to 277.5,45.2 fc rgb "red" fs noborder
set object 68 rect from 0.5,45.8 to 12.5,46 fc rgb "blue" fs noborder
set object 69 rect from 157.5,45.8 to 158.5,46 fc rgb "blue" fs noborder
set object 70 rect from 209.5,45.8 to 246.5,46 fc rgb "blue" fs noborder
set object 71 rect from 298.5,45.8 to 336.5,46 fc rgb "blue" fs noborder
set object 72 rect from 12.5,45 to 33.5,46 fc rgb "white"
set object 73 rect from 136.5,45 to 157.5,46 fc rgb "grey" fs noborder
set object 74 rect from 158.5,45 to 179.5,46 fc rgb "white"
set object 75 rect from 188.5,45 to 209.5,46 fc rgb "grey" fs noborder
set object 76 rect from 246.5,45 to 267.5,46 fc rgb "white"
set object 77 rect from 277.5,45 to 298.5,46 fc rgb "grey" fs noborder
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//DG1.txt' axes x1y2 w l t '' lt 3 lw 4
exit
