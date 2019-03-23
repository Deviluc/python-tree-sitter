import setuptools

setuptools.setup(name="python-tree-sitter",
                 version="0.1",
                 packages=["tree_sitter_api", "tree_sitter_java"],
                 package_dir={'tree_sitter_api': 'modules/tree_sitter_api',
                              'tree_sitter_java': 'modules/tree_sitter_java'},
                 package_data={'tree_sitter_api': ['*.so'],
                               'tree_sitter_java': ['*so']})
