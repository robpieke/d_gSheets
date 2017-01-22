# d_gSheets

Google Sheets display driver for PRMan

When rendered, the included **test.rib** file should generate a result similar to [this](https://docs.google.com/spreadsheets/d/1FA1GADPNNjoPwtmtB5LgU7PvJPA6BhY2k_T1vgudpIs).

## Motivation & Caveats

In November 2016, [this video](https://www.youtube.com/watch?v=86q5TMzvRqo) showed up in my Twitter feed. It was impossible to avoid Wesley's enthusiasm, so I thought I'd give the new Google Sheets formatting API a try. Changing the background colour of a cell seems akin to changing the colour of a pixel on the screen, so trying to render from Pixar's RenderMan directly to a Google Sheets document seemed like an interesting challenge.

Interfacing with the Google APIs was most easily done in Python, but the display driver API for RenderMan needed to be written in C/C++. I made no effort in this experiment to be efficient in invoking Python from C++, or in sharing buffers of data in memory, instead focusing on achieving functionality as quickly as possible. I would love to improve my knowledge of Python's C library at some point, but this was not the project to do so.

## Pre-requisites

To build the code, you'll need to first [download Pixar's RenderMan](https://renderman.pixar.com/view/get-renderman). Any version later than 20.0 should be fine.

To use the Google APIs, you'll need to follow the instructions in the [quick-start guide](https://developers.google.com/sheets/api/quickstart/python). If you can run the example there, you should be fine for this project.

