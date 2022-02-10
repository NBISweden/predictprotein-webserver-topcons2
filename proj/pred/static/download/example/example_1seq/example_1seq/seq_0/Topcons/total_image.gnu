set encoding iso_8859_1
set yrange [0:50]
set xrange [1:250]
set y2range [-2:23.2]
set autoscale xfix
set ter png enh interlace size 2400,1680 font 'Nimbus,40'
set y2label '{/Symbol D}G (kcal/mol)                                             ' tc lt 3
set ytics scale 1,0.5 nomirror ("0" 0, "5" 5, "10" 10, "15" 15, "20" 20, "25" 25, "SPOCTOPUS" 30.5 0, "SCAMPI" 33.5 0, "PolyPhobius" 36.5 0, "Philius" 39.5 0, "OCTOPUS" 42.5 0, "TOPCONS" 45.5 0)
set y2tics nomirror -2,2,12
set out '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp__VTMQp/rst_qYdSyU//seq_0//Topcons/total_image.large.png'
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
set object 6 rect from 38.5,30 to 49.5,30.2 fc rgb "red" fs noborder
set object 7 rect from 110.5,30 to 115.5,30.2 fc rgb "red" fs noborder
set object 8 rect from 163.5,30 to 179.5,30.2 fc rgb "red" fs noborder
set object 9 rect from 231.5,30 to 250.5,30.2 fc rgb "red" fs noborder
set object 10 rect from 0.5,30.8 to 17.5,31 fc rgb "blue" fs noborder
set object 11 rect from 70.5,30.8 to 89.5,31 fc rgb "blue" fs noborder
set object 12 rect from 136.5,30.8 to 142.5,31 fc rgb "blue" fs noborder
set object 13 rect from 200.5,30.8 to 210.5,31 fc rgb "blue" fs noborder
set object 14 rect from 17.5,30 to 38.5,31 fc rgb "white"
set object 15 rect from 49.5,30 to 70.5,31 fc rgb "grey" fs noborder
set object 16 rect from 89.5,30 to 110.5,31 fc rgb "white"
set object 17 rect from 115.5,30 to 136.5,31 fc rgb "grey" fs noborder
set object 18 rect from 142.5,30 to 163.5,31 fc rgb "white"
set object 19 rect from 179.5,30 to 200.5,31 fc rgb "grey" fs noborder
set object 20 rect from 210.5,30 to 231.5,31 fc rgb "white"
set object 21 rect from 37.5,33 to 49.5,33.2 fc rgb "red" fs noborder
set object 22 rect from 109.5,33 to 115.5,33.2 fc rgb "red" fs noborder
set object 23 rect from 161.5,33 to 178.5,33.2 fc rgb "red" fs noborder
set object 24 rect from 234.5,33 to 250.5,33.2 fc rgb "red" fs noborder
set object 25 rect from 0.5,33.8 to 16.5,34 fc rgb "blue" fs noborder
set object 26 rect from 70.5,33.8 to 88.5,34 fc rgb "blue" fs noborder
set object 27 rect from 136.5,33.8 to 140.5,34 fc rgb "blue" fs noborder
set object 28 rect from 199.5,33.8 to 213.5,34 fc rgb "blue" fs noborder
set object 29 rect from 16.5,33 to 37.5,34 fc rgb "white"
set object 30 rect from 49.5,33 to 70.5,34 fc rgb "grey" fs noborder
set object 31 rect from 88.5,33 to 109.5,34 fc rgb "white"
set object 32 rect from 115.5,33 to 136.5,34 fc rgb "grey" fs noborder
set object 33 rect from 140.5,33 to 161.5,34 fc rgb "white"
set object 34 rect from 178.5,33 to 199.5,34 fc rgb "grey" fs noborder
set object 35 rect from 213.5,33 to 234.5,34 fc rgb "white"
set object 36 rect from 38.5,36 to 49.5,36.2 fc rgb "red" fs noborder
set object 37 rect from 109.5,36 to 115.5,36.2 fc rgb "red" fs noborder
set object 38 rect from 162.5,36 to 181.5,36.2 fc rgb "red" fs noborder
set object 39 rect from 233.5,36 to 250.5,36.2 fc rgb "red" fs noborder
set object 40 rect from 0.5,36.8 to 18.5,37 fc rgb "blue" fs noborder
set object 41 rect from 72.5,36.8 to 90.5,37 fc rgb "blue" fs noborder
set object 42 rect from 137.5,36.8 to 142.5,37 fc rgb "blue" fs noborder
set object 43 rect from 200.5,36.8 to 213.5,37 fc rgb "blue" fs noborder
set object 44 rect from 18.5,36 to 38.5,37 fc rgb "white"
set object 45 rect from 49.5,36 to 72.5,37 fc rgb "grey" fs noborder
set object 46 rect from 90.5,36 to 109.5,37 fc rgb "white"
set object 47 rect from 115.5,36 to 137.5,37 fc rgb "grey" fs noborder
set object 48 rect from 142.5,36 to 162.5,37 fc rgb "white"
set object 49 rect from 181.5,36 to 200.5,37 fc rgb "grey" fs noborder
set object 50 rect from 213.5,36 to 233.5,37 fc rgb "white"
set object 51 rect from 37.5,39 to 49.5,39.2 fc rgb "red" fs noborder
set object 52 rect from 108.5,39 to 115.5,39.2 fc rgb "red" fs noborder
set object 53 rect from 164.5,39 to 181.5,39.2 fc rgb "red" fs noborder
set object 54 rect from 233.5,39 to 250.5,39.2 fc rgb "red" fs noborder
set object 55 rect from 0.5,39.8 to 17.5,40 fc rgb "blue" fs noborder
set object 56 rect from 72.5,39.8 to 89.5,40 fc rgb "blue" fs noborder
set object 57 rect from 136.5,39.8 to 142.5,40 fc rgb "blue" fs noborder
set object 58 rect from 201.5,39.8 to 213.5,40 fc rgb "blue" fs noborder
set object 59 rect from 17.5,39 to 37.5,40 fc rgb "white"
set object 60 rect from 49.5,39 to 72.5,40 fc rgb "grey" fs noborder
set object 61 rect from 89.5,39 to 108.5,40 fc rgb "white"
set object 62 rect from 115.5,39 to 136.5,40 fc rgb "grey" fs noborder
set object 63 rect from 142.5,39 to 164.5,40 fc rgb "white"
set object 64 rect from 181.5,39 to 201.5,40 fc rgb "grey" fs noborder
set object 65 rect from 213.5,39 to 233.5,40 fc rgb "white"
set object 66 rect from 38.5,42 to 49.5,42.2 fc rgb "red" fs noborder
set object 67 rect from 110.5,42 to 115.5,42.2 fc rgb "red" fs noborder
set object 68 rect from 163.5,42 to 179.5,42.2 fc rgb "red" fs noborder
set object 69 rect from 231.5,42 to 250.5,42.2 fc rgb "red" fs noborder
set object 70 rect from 0.5,42.8 to 17.5,43 fc rgb "blue" fs noborder
set object 71 rect from 70.5,42.8 to 89.5,43 fc rgb "blue" fs noborder
set object 72 rect from 136.5,42.8 to 142.5,43 fc rgb "blue" fs noborder
set object 73 rect from 200.5,42.8 to 210.5,43 fc rgb "blue" fs noborder
set object 74 rect from 17.5,42 to 38.5,43 fc rgb "white"
set object 75 rect from 49.5,42 to 70.5,43 fc rgb "grey" fs noborder
set object 76 rect from 89.5,42 to 110.5,43 fc rgb "white"
set object 77 rect from 115.5,42 to 136.5,43 fc rgb "grey" fs noborder
set object 78 rect from 142.5,42 to 163.5,43 fc rgb "white"
set object 79 rect from 179.5,42 to 200.5,43 fc rgb "grey" fs noborder
set object 80 rect from 210.5,42 to 231.5,43 fc rgb "white"
set object 81 rect from 38.5,45 to 49.5,45.2 fc rgb "red" fs noborder
set object 82 rect from 110.5,45 to 115.5,45.2 fc rgb "red" fs noborder
set object 83 rect from 163.5,45 to 179.5,45.2 fc rgb "red" fs noborder
set object 84 rect from 233.5,45 to 250.5,45.2 fc rgb "red" fs noborder
set object 85 rect from 0.5,45.8 to 17.5,46 fc rgb "blue" fs noborder
set object 86 rect from 70.5,45.8 to 89.5,46 fc rgb "blue" fs noborder
set object 87 rect from 136.5,45.8 to 142.5,46 fc rgb "blue" fs noborder
set object 88 rect from 200.5,45.8 to 212.5,46 fc rgb "blue" fs noborder
set object 89 rect from 17.5,45 to 38.5,46 fc rgb "white"
set object 90 rect from 49.5,45 to 70.5,46 fc rgb "grey" fs noborder
set object 91 rect from 89.5,45 to 110.5,46 fc rgb "white"
set object 92 rect from 115.5,45 to 136.5,46 fc rgb "grey" fs noborder
set object 93 rect from 142.5,45 to 163.5,46 fc rgb "white"
set object 94 rect from 179.5,45 to 200.5,46 fc rgb "grey" fs noborder
set object 95 rect from 212.5,45 to 233.5,46 fc rgb "white"
plot '/big/server/web_topcons2/debug/proj/pred/static/tmp/tmp__VTMQp/rst_qYdSyU//seq_0//DG1.txt' axes x1y2 w l t '' lt 3 lw 4
exit
