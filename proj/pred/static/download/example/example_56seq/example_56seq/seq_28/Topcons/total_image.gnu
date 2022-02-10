set encoding iso_8859_1
set yrange [0:50]
set xrange [1:365]
set y2range [-2:31]
set autoscale xfix
set ter png enh interlace size 2400,1680 font 'Nimbus,40'
set y2label '{/Symbol D}G (kcal/mol)                                             ' tc lt 3
set ytics scale 1,0.5 nomirror ("0" 0, "5" 5, "10" 10, "15" 15, "20" 20, "25" 25, "SPOCTOPUS" 30.5 0, "SCAMPI" 33.5 0, "PolyPhobius" 36.5 0, "Philius" 39.5 0, "OCTOPUS" 42.5 0, "TOPCONS" 45.5 0)
set y2tics nomirror -5,2,15
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
set object 6 rect from 33.5,30 to 153.5,30.2 fc rgb "red" fs noborder
set object 7 rect from 184.5,30 to 193.5,30.2 fc rgb "red" fs noborder
set object 8 rect from 272.5,30 to 282.5,30.2 fc rgb "red" fs noborder
set object 9 rect from 353.5,30 to 365.5,30.2 fc rgb "red" fs noborder
set object 10 rect from 0.5,30.8 to 12.5,31 fc rgb "blue" fs noborder
set object 11 rect from 168.5,30.8 to 169.5,31 fc rgb "blue" fs noborder
set object 12 rect from 214.5,30.8 to 251.5,31 fc rgb "blue" fs noborder
set object 13 rect from 303.5,30.8 to 332.5,31 fc rgb "blue" fs noborder
set object 14 rect from 12.5,30 to 33.5,31 fc rgb "white"
set object 15 rect from 153.5,30 to 168.5,31 fc rgb "grey" fs noborder
set object 16 rect from 169.5,30 to 184.5,31 fc rgb "white"
set object 17 rect from 193.5,30 to 214.5,31 fc rgb "grey" fs noborder
set object 18 rect from 251.5,30 to 272.5,31 fc rgb "white"
set object 19 rect from 282.5,30 to 303.5,31 fc rgb "grey" fs noborder
set object 20 rect from 332.5,30 to 353.5,31 fc rgb "white"
set object 21 rect from 35.5,33 to 163.5,33.2 fc rgb "red" fs noborder
set object 22 rect from 216.5,33 to 256.5,33.2 fc rgb "red" fs noborder
set object 23 rect from 302.5,33 to 331.5,33.2 fc rgb "red" fs noborder
set object 24 rect from 0.5,33.8 to 14.5,34 fc rgb "blue" fs noborder
set object 25 rect from 184.5,33.8 to 195.5,34 fc rgb "blue" fs noborder
set object 26 rect from 277.5,33.8 to 281.5,34 fc rgb "blue" fs noborder
set object 27 rect from 352.5,33.8 to 365.5,34 fc rgb "blue" fs noborder
set object 28 rect from 14.5,33 to 35.5,34 fc rgb "white"
set object 29 rect from 163.5,33 to 184.5,34 fc rgb "grey" fs noborder
set object 30 rect from 195.5,33 to 216.5,34 fc rgb "white"
set object 31 rect from 256.5,33 to 277.5,34 fc rgb "grey" fs noborder
set object 32 rect from 281.5,33 to 302.5,34 fc rgb "white"
set object 33 rect from 331.5,33 to 352.5,34 fc rgb "grey" fs noborder
set object 34 rect from 0.5,36 to 11.5,36.2 fc rgb "red" fs noborder
set object 35 rect from 183.5,36 to 194.5,36.2 fc rgb "red" fs noborder
set object 36 rect from 274.5,36 to 281.5,36.2 fc rgb "red" fs noborder
set object 37 rect from 354.5,36 to 365.5,36.2 fc rgb "red" fs noborder
set object 38 rect from 33.5,36.8 to 154.5,37 fc rgb "blue" fs noborder
set object 39 rect from 217.5,36.8 to 248.5,37 fc rgb "blue" fs noborder
set object 40 rect from 302.5,36.8 to 331.5,37 fc rgb "blue" fs noborder
set object 41 rect from 11.5,36 to 33.5,37 fc rgb "grey" fs noborder
set object 42 rect from 154.5,36 to 183.5,37 fc rgb "white"
set object 43 rect from 194.5,36 to 217.5,37 fc rgb "grey" fs noborder
set object 44 rect from 248.5,36 to 274.5,37 fc rgb "white"
set object 45 rect from 281.5,36 to 302.5,37 fc rgb "grey" fs noborder
set object 46 rect from 331.5,36 to 354.5,37 fc rgb "white"
set object 47 rect from 0.5,39 to 12.5,39.2 fc rgb "red" fs noborder
set object 48 rect from 184.5,39 to 193.5,39.2 fc rgb "red" fs noborder
set object 49 rect from 272.5,39 to 281.5,39.2 fc rgb "red" fs noborder
set object 50 rect from 354.5,39 to 365.5,39.2 fc rgb "red" fs noborder
set object 51 rect from 33.5,39.8 to 163.5,40 fc rgb "blue" fs noborder
set object 52 rect from 216.5,39.8 to 251.5,40 fc rgb "blue" fs noborder
set object 53 rect from 302.5,39.8 to 331.5,40 fc rgb "blue" fs noborder
set object 54 rect from 12.5,39 to 33.5,40 fc rgb "grey" fs noborder
set object 55 rect from 163.5,39 to 184.5,40 fc rgb "white"
set object 56 rect from 193.5,39 to 216.5,40 fc rgb "grey" fs noborder
set object 57 rect from 251.5,39 to 272.5,40 fc rgb "white"
set object 58 rect from 281.5,39 to 302.5,40 fc rgb "grey" fs noborder
set object 59 rect from 331.5,39 to 354.5,40 fc rgb "white"
set object 60 rect from 33.5,42 to 153.5,42.2 fc rgb "red" fs noborder
set object 61 rect from 184.5,42 to 193.5,42.2 fc rgb "red" fs noborder
set object 62 rect from 272.5,42 to 282.5,42.2 fc rgb "red" fs noborder
set object 63 rect from 353.5,42 to 365.5,42.2 fc rgb "red" fs noborder
set object 64 rect from 0.5,42.8 to 12.5,43 fc rgb "blue" fs noborder
set object 65 rect from 168.5,42.8 to 169.5,43 fc rgb "blue" fs noborder
set object 66 rect from 214.5,42.8 to 251.5,43 fc rgb "blue" fs noborder
set object 67 rect from 303.5,42.8 to 332.5,43 fc rgb "blue" fs noborder
set object 68 rect from 12.5,42 to 33.5,43 fc rgb "white"
set object 69 rect from 153.5,42 to 168.5,43 fc rgb "grey" fs noborder
set object 70 rect from 169.5,42 to 184.5,43 fc rgb "white"
set object 71 rect from 193.5,42 to 214.5,43 fc rgb "grey" fs noborder
set object 72 rect from 251.5,42 to 272.5,43 fc rgb "white"
set object 73 rect from 282.5,42 to 303.5,43 fc rgb "grey" fs noborder
set object 74 rect from 332.5,42 to 353.5,43 fc rgb "white"
set object 75 rect from 33.5,45 to 141.5,45.2 fc rgb "red" fs noborder
set object 76 rect from 184.5,45 to 193.5,45.2 fc rgb "red" fs noborder
set object 77 rect from 272.5,45 to 281.5,45.2 fc rgb "red" fs noborder
set object 78 rect from 353.5,45 to 365.5,45.2 fc rgb "red" fs noborder
set object 79 rect from 0.5,45.8 to 12.5,46 fc rgb "blue" fs noborder
set object 80 rect from 162.5,45.8 to 163.5,46 fc rgb "blue" fs noborder
set object 81 rect from 214.5,45.8 to 251.5,46 fc rgb "blue" fs noborder
set object 82 rect from 302.5,45.8 to 332.5,46 fc rgb "blue" fs noborder
set object 83 rect from 12.5,45 to 33.5,46 fc rgb "white"
set object 84 rect from 141.5,45 to 162.5,46 fc rgb "grey" fs noborder
set object 85 rect from 163.5,45 to 184.5,46 fc rgb "white"
set object 86 rect from 193.5,45 to 214.5,46 fc rgb "grey" fs noborder
set object 87 rect from 251.5,45 to 272.5,46 fc rgb "white"
set object 88 rect from 281.5,45 to 302.5,46 fc rgb "grey" fs noborder
set object 89 rect from 332.5,45 to 353.5,46 fc rgb "white"
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//DG1.txt' axes x1y2 w l t '' lt 3 lw 4
exit
