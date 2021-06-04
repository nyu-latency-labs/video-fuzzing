# Sample code to run compositor with jpg background
```
gst-launch-1.0 \
    filesrc location="./resources/street.jpg" ! decodebin ! imagefreeze ! \
    compositor name=m ! autovideosink \
    filesrc location="./resources/cars/1.mov" ! decodebin ! m.
```