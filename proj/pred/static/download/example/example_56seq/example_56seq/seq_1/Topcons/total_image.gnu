set encoding iso_8859_1
set yrange [0:50]
set xrange [1:372]
set y2range [-2:31.4]
set autoscale xfix
set ter png enh interlace size 2400,1680 font 'Nimbus,40'
set y2label '{/Symbol D}G (kcal/mol)                                             ' tc lt 3
set ytics scale 1,0.5 nomirror ("0" 0, "5" 5, "10" 10, "15" 15, "20" 20, "25" 25, "SPOCTOPUS" 30.5 0, "SCAMPI" 33.5 0, "PolyPhobius" 36.5 0, "Philius" 39.5 0, "OCTOPUS" 42.5 0, "TOPCONS" 45.5 0)
set y2tics nomirror -1,2,17
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
set object 6 rect from 0.5,30 to 180.5,30.2 fc rgb "red" fs noborder
set object 7 rect from 255.5,30 to 260.5,30.2 fc rgb "red" fs noborder
set object 8 rect from 310.5,30 to 317.5,30.2 fc rgb "red" fs noborder
set object 9 rect from 365.5,30 to 372.5,30.2 fc rgb "red" fs noborder
set object 10 rect from 201.5,30.8 to 224.5,31 fc rgb "blue" fs noborder
set object 11 rect from 281.5,30.8 to 289.5,31 fc rgb "blue" fs noborder
set object 12 rect from 338.5,30.8 to 344.5,31 fc rgb "blue" fs noborder
set object 13 rect from 180.5,30 to 201.5,31 fc rgb "grey" fs noborder
set object 14 rect from 224.5,30 to 255.5,31 fc rgb "white"
set object 15 rect from 260.5,30 to 281.5,31 fc rgb "grey" fs noborder
set object 16 rect from 289.5,30 to 310.5,31 fc rgb "white"
set object 17 rect from 317.5,30 to 338.5,31 fc rgb "grey" fs noborder
set object 18 rect from 344.5,30 to 365.5,31 fc rgb "white"
set object 19 rect from 0.5,33 to 180.5,33.2 fc rgb "red" fs noborder
set object 20 rect from 245.5,33 to 263.5,33.2 fc rgb "red" fs noborder
set object 21 rect from 311.5,33 to 319.5,33.2 fc rgb "red" fs noborder
set object 22 rect from 364.5,33 to 372.5,33.2 fc rgb "red" fs noborder
set object 23 rect from 201.5,33.8 to 224.5,34 fc rgb "blue" fs noborder
set object 24 rect from 284.5,33.8 to 290.5,34 fc rgb "blue" fs noborder
set object 25 rect from 340.5,33.8 to 343.5,34 fc rgb "blue" fs noborder
set object 26 rect from 180.5,33 to 201.5,34 fc rgb "grey" fs noborder
set object 27 rect from 224.5,33 to 245.5,34 fc rgb "white"
set object 28 rect from 263.5,33 to 284.5,34 fc rgb "grey" fs noborder
set object 29 rect from 290.5,33 to 311.5,34 fc rgb "white"
set object 30 rect from 319.5,33 to 340.5,34 fc rgb "grey" fs noborder
set object 31 rect from 343.5,33 to 364.5,34 fc rgb "white"
set object 32 rect from 0.5,36 to 176.5,36.2 fc rgb "red" fs noborder
set object 33 rect from 252.5,36 to 263.5,36.2 fc rgb "red" fs noborder
set object 34 rect from 311.5,36 to 319.5,36.2 fc rgb "red" fs noborder
set object 35 rect from 363.5,36 to 372.5,36.2 fc rgb "red" fs noborder
set object 36 rect from 202.5,36.8 to 225.5,37 fc rgb "blue" fs noborder
set object 37 rect from 283.5,36.8 to 288.5,37 fc rgb "blue" fs noborder
set object 38 rect from 339.5,36.8 to 344.5,37 fc rgb "blue" fs noborder
set object 39 rect from 176.5,36 to 202.5,37 fc rgb "grey" fs noborder
set object 40 rect from 225.5,36 to 252.5,37 fc rgb "white"
set object 41 rect from 263.5,36 to 283.5,37 fc rgb "grey" fs noborder
set object 42 rect from 288.5,36 to 311.5,37 fc rgb "white"
set object 43 rect from 319.5,36 to 339.5,37 fc rgb "grey" fs noborder
set object 44 rect from 344.5,36 to 363.5,37 fc rgb "white"
set object 45 rect from 0.5,39 to 175.5,39.2 fc rgb "red" fs noborder
set object 46 rect from 255.5,39 to 263.5,39.2 fc rgb "red" fs noborder
set object 47 rect from 312.5,39 to 319.5,39.2 fc rgb "red" fs noborder
set object 48 rect from 362.5,39 to 372.5,39.2 fc rgb "red" fs noborder
set object 49 rect from 198.5,39.8 to 232.5,40 fc rgb "blue" fs noborder
set object 50 rect from 285.5,39.8 to 291.5,40 fc rgb "blue" fs noborder
set object 51 rect from 338.5,39.8 to 344.5,40 fc rgb "blue" fs noborder
set object 52 rect from 175.5,39 to 198.5,40 fc rgb "grey" fs noborder
set object 53 rect from 232.5,39 to 255.5,40 fc rgb "white"
set object 54 rect from 263.5,39 to 285.5,40 fc rgb "grey" fs noborder
set object 55 rect from 291.5,39 to 312.5,40 fc rgb "white"
set object 56 rect from 319.5,39 to 338.5,40 fc rgb "grey" fs noborder
set object 57 rect from 344.5,39 to 362.5,40 fc rgb "white"
set object 58 rect from 0.5,42 to 180.5,42.2 fc rgb "red" fs noborder
set object 59 rect from 254.5,42 to 260.5,42.2 fc rgb "red" fs noborder
set object 60 rect from 310.5,42 to 317.5,42.2 fc rgb "red" fs noborder
set object 61 rect from 365.5,42 to 372.5,42.2 fc rgb "red" fs noborder
set object 62 rect from 201.5,42.8 to 223.5,43 fc rgb "blue" fs noborder
set object 63 rect from 281.5,42.8 to 289.5,43 fc rgb "blue" fs noborder
set object 64 rect from 338.5,42.8 to 344.5,43 fc rgb "blue" fs noborder
set object 65 rect from 180.5,42 to 201.5,43 fc rgb "grey" fs noborder
set object 66 rect from 223.5,42 to 254.5,43 fc rgb "white"
set object 67 rect from 260.5,42 to 281.5,43 fc rgb "grey" fs noborder
set object 68 rect from 289.5,42 to 310.5,43 fc rgb "white"
set object 69 rect from 317.5,42 to 338.5,43 fc rgb "grey" fs noborder
set object 70 rect from 344.5,42 to 365.5,43 fc rgb "white"
set object 71 rect from 0.5,45 to 180.5,45.2 fc rgb "red" fs noborder
set object 72 rect from 252.5,45 to 262.5,45.2 fc rgb "red" fs noborder
set object 73 rect from 310.5,45 to 317.5,45.2 fc rgb "red" fs noborder
set object 74 rect from 365.5,45 to 372.5,45.2 fc rgb "red" fs noborder
set object 75 rect from 201.5,45.8 to 231.5,46 fc rgb "blue" fs noborder
set object 76 rect from 283.5,45.8 to 289.5,46 fc rgb "blue" fs noborder
set object 77 rect from 338.5,45.8 to 344.5,46 fc rgb "blue" fs noborder
set object 78 rect from 180.5,45 to 201.5,46 fc rgb "grey" fs noborder
set object 79 rect from 231.5,45 to 252.5,46 fc rgb "white"
set object 80 rect from 262.5,45 to 283.5,46 fc rgb "grey" fs noborder
set object 81 rect from 289.5,45 to 310.5,46 fc rgb "white"
set object 82 rect from 317.5,45 to 338.5,46 fc rgb "grey" fs noborder
set object 83 rect from 344.5,45 to 365.5,46 fc rgb "white"
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp_LUCOtf/rst_KQXgCM//seq_0//DG1.txt' axes x1y2 w l t '' lt 3 lw 4
exit
