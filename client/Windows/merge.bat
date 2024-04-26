echo off
ren cira-rammb-slider_himawari_full-disk_cira*.png "geo.png"
ren cira-rammb-slider_himawari_full-disk_*.png "storm.png"

convert storm.png ( -clone 0 -colorspace CMYK -channel CMY -separate -evaluate-sequence add ) ( -clone 0,1 -alpha off -compose copyopacity -composite ) ( -clone 0 -fuzz 15% +transparent white -blur 0x1.5 ) -delete 0,1 -compose over -composite storm.png

ren latest.png %date:~10,4%%date:~7,2%%date:~4,2%_%time:~1,1%%time:~3,2%_previous.png

composite -compose over storm.png geo.png latest.png
del storm.png 
del geo.png