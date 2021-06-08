# Facebook Python Business Sdk Parser

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Parse the Facebook Python Business SDK and output in a local neo4j database

## Run

    docker compose up

## Explore Nodes

Navigate to `http://localhost:7474/browser/`

![index](https://github.com/Just1B/facebook-python-business-sdk-parser/raw/master/images/neo4j_nodes.png)

## GET AdObject and AdObjectFields

```
MATCH (ao:AdObject)<-[is_field:IS_FIELD]-(af:AdObjectField)
RETURN ao,is_field,af
LIMIT 25
```

# Licence

The MIT License

Copyright (c) 2021 JUST1B

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
