# python-tree-sitter
A wrapper around the c-api of tree-sitter using swig

## Building and installing
Requires python 3.7m

### Building api

```./build.sh```

### Building java parser
```./build_java.sh```

### Install
*Warning*: currently both the api and java part must have been built first!
```sudo python setup.py install```


## Usage
```
from tree_sitter_api import Parser
from tree_sitter_java import tree_sitter_java
javalang = tree_sitter_java()
parser = api.Parser()
parser.set_language(javalang)
tree = parser.parse_string("package com.example; public class Main { public static void main(final String[] args) { return; } }")
root_node = tree.root_node()
for node in root_node:
    print(node.string())
```

