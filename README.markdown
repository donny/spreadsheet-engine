## spreadsheet-engine

A Google App Engine application written in Python that provides an API for data hosted by Google Spreadsheets. It utilizes the [Google Spreadsheets Data API](http://code.google.com/apis/spreadsheets/data/), specifically its [text_db](http://code.google.com/p/gdata-python-client/source/browse/trunk/src/gdata/spreadsheet/text_db.py) module. It uses [JSON](http://en.wikipedia.org/wiki/Json) for the data interchange format. The project allows a client application to access data hosted by Google Spreadsheets simply by making HTTP GET and POST calls. It provides [CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete) function calls (`insert`, `select`, `update`, `delete`).

### Example

Let's say, there is a spreadsheet named `test` that has a worksheet named `sheet`; and the worksheet contains the following data:

    |-------|---------|---------|
    |       |    A    |    B    |
    |-------|---------|---------|
    |   1   |  name   | number  |
    |-------|---------|---------|
    |   2   |  joe    |   11    |
    |-------|---------|---------|
    |   3   |  andy   |   22    |
    |-------|---------|---------|
    |   4   |  mike   |   33    |
    |-------|---------|---------|

Then these HTTP POST calls:

    $ curl 'http://example.appspot.com/test/sheet' --data 'op=select&row=2'
    {"name": "andy", "number": "22"}
    $ curl 'http://example.appspot.com/test/sheet' --data 'op=insert&data={"name": "susan", "number": "44"}'
    $ curl 'http://example.appspot.com/test/sheet' --data 'op=insert&data={"name": "rob", "number": "55"}'
    $ curl 'http://example.appspot.com/test/sheet' --data 'op=delete&row=3'

Modify the worksheet to contain the following data:

    |-------|---------|---------|
    |       |    A    |    B    |
    |-------|---------|---------|
    |   1   |  name   | number  |
    |-------|---------|---------|
    |   2   |  joe    |   11    |
    |-------|---------|---------|
    |   3   |  andy   |   22    |
    |-------|---------|---------|
    |   4   |  susan  |   44    |
    |-------|---------|---------|
    |   5   |  rob    |   55    |
    |-------|---------|---------|

Note that the numbering begins at 1, which refers to the second row in the worksheet since the first row is used for column names.

### Requirement

Download the [gdata-python-client](http://code.google.com/p/gdata-python-client/) package. Unzip the archive. Copy the directories `src/gdata` and `src/atom` to the top level directory of `spreadsheet-engine`.
